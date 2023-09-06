# Analytics Vidhya: Building Language Models in NLP
import re
import string
from operator import itemgetter
from tokenizer import tokenize
from collections import Counter
from pathlib import Path
from prediction import Prediction

def is_word(word: str, stopwords=set()):
    #word = re.search("[\[\]\}\{=@\*]")
    if (re.sub("[A-Za-z0-9#\'\./_&+-]", "", word) == "") and len(word) > 1:
        if ((word not in stopwords) and not word.isdigit()):
            return True
    return False


class Sentencizer:

    def __init__(self, stopwordsPath="stopwords.txt"):
        self.sentences = []
        self.stopwords = set()
        self.vocab = set()
        self.vocab_freq = {}
        self.u_vocab_freq = {}
        self.prediction = Prediction()
        s = set()
        s.update([line.replace('\n', '') for line in open(stopwordsPath, 'r', encoding='utf-8').readlines()])
        self.stopwords = sorted(s)
        
        self.tms        = set()
        self.ignore     = set()
        self.dictionary = set()
        self.load_dictionaries()


    def load_dictionaries(self):
        rel = "./dict/"
        diix = Path(rel + "diixonary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open(rel + diix.name, 'r', encoding='utf-8').readlines()])

        diix = Path(rel + "dictionary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open(rel + diix.name, 'r', encoding='utf-8').readlines()])

        diix = Path(rel + "mistakes-db.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open(rel + diix.name, 'r', encoding='utf-8').readlines()])

        self.dictionary.update(self.stopwords)
        self.dictionary = set(sorted(self.dictionary))

        # read additional dictionaries
        path = Path("./dict/trademarks.txt")
        if path.exists():
            self.tms.update([line.replace('\n', '').lower() for line in open(rel + diix.name, 'r', encoding='utf-8').readlines()])
            self.tms = set(sorted(self.tms))

        path = Path("./dict/ignore.txt")
        if path.exists():
            self.ignore.update([line.replace('\n', '').lower() for line in open(rel + diix.name, 'r', encoding='utf-8').readlines()])
            self.ignore = set(sorted(self.ignore))
    ##########################################################
    def slice_to_sentences(self, str_line: str):

        line1 = str_line.replace(". ", "!")
        line1 = re.sub('[!?;,:\[\]\(\)]', "><", line1)
        return [x.strip().lower() for x in line1.split("><") if x !='']
        # x.strip().lower() - used as kayer point for tokenize.case_sensitive switching.

    def update(self, str_line: str, buildPredict=False):
        punctuation = "©®-%$!?:,;\'\" @~&()=*_<=>{|}[/]^\\"

        sentences = self.slice_to_sentences(str_line)

        for i, item in enumerate(sentences):
        #{
            #words_list = [x.strip(string.punctuation) if x not in self.dictionary else x for x in item.split(" ") if (x != '')]
            
            words_list = [x.strip(punctuation) if x.strip(punctuation) in self.dictionary else x.strip(string.punctuation) 
                                for x in item.split(" ") if (x != '')]

            #sentences[i] = words_list
            tokens = []
            for w in words_list:
            #{
                if is_word(w, self.stopwords):
                    if buildPredict:
                        self.prediction.add_token(w, self.stopwords, self.dictionary, self.tms)
                    ###########################################################
                    if (w in self.dictionary) or (self.constructedSize(w) > 0):
                        tokens.append(w)
                        self.vocab.add(w)
                        self.vocab_freq[w] = self.vocab_freq.get(w, 0) + 1
                    else:
                        if w in self.tms:
                            if not buildPredict: tokens.append(w) 
                        else:
                            if (w not in self.ignore):
                                self.u_vocab_freq[w] = self.u_vocab_freq.get(w, 0) + 1
            #}
            if buildPredict:
                self.prediction.add_tokens(tokens)

            tokens.append(";")
            sentences[i] = tokens
        #}
        return sentences
    ##########################################################

    def constructedSize(self, word: str) -> int:
        if word in self.dictionary : return 0

        ws = re.split('[/-]', word)
        sz = len(ws)
        if (sz > 1) and (sz <= 3):
            cntr = 0
            for w in ws:
                if ((w in self.stopwords) or (w in self.dictionary)) and (w not in self.tms):
                    cntr += 1
                else: break
            if (sz == cntr): return sz
        return 0
    ##########################################################
    def finalize(self):
        str_path = "./__build/"
        with Path(str_path) as path:
            if not path.exists(): path.mkdir()

        print("finalizing -->>")
        if len(self.u_vocab_freq) > 0:
        #{
            print(">> u_vocab-freq")
            self.u_vocab_freq = sorted(self.u_vocab_freq.items(), key=itemgetter(1), reverse=True)

            f1 = open(str_path + "un-vocab-sort-1.utf8", 'w', encoding='utf-8')
            f2 = open(str_path + "un-vocab-sort-2.utf8", 'w', encoding='utf-8')
            for kv in self.u_vocab_freq:
                word = kv[0]
                ws = re.split('[_/-]', word)
                sz = len(ws)
                if (sz == 1):
                    f1.write(word + " ; " + str(kv[1]) + "\n")
                if (sz == 2):
                    f2.write(word + " ; " + str(kv[1]) + "\n")
            f1.close()
            f2.close()
            print("<< u_vocab-freq")
        #}

        if self.prediction.size() > 0:
            self.prediction.finalize(self.dictionary)
        else:
        #{
            print(">> vocab...")
            self.vocab = sorted(self.vocab)

            f = open(str_path + "vocab-new.utf8", 'w', encoding='utf-8')
            for w in self.vocab:
                if w in self.dictionary:
                    continue
                f.write(w + " ; " + str(self.vocab_freq[w]) + "\n")
            f.close()
            print("<< vocab")
            ##################################################################################
            print(">> vocab-freq...")
            self.vocab_freq = sorted(self.vocab_freq.items(), key=itemgetter(1), reverse=True)

            f = open(str_path + "vocab-new-sort.utf8", 'w', encoding='utf-8')
            for kv in self.vocab_freq:
                if kv[0] in self.dictionary:
                    continue
                f.write(kv[0] + " ; " + str(kv[1]) + "\n")
            f.close()
            print("<< vocab-freq")
        #}
        print(f"<<-- finalizing [dictionary.sz={len(self.dictionary)}, stopwords.sz={len(self.stopwords)}]")
    ##########################################################

    def predict_next(self, line: str):
        str_line = tokenize(line, self.stopwords)
        return self.prediction.predict_next(str_line)
