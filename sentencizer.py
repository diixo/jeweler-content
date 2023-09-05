# Analytics Vidhya: Building Language Models in NLP
import re
import string
from operator import itemgetter
from tokenizer import tokenize
from collections import Counter
from pathlib import Path
from prediction import Prediction


class Sentencizer:

    def __init__(self, stopwordsPath="stopwords.txt"):
        self.sentences = []
        self._index = 0
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
        self.readDictionary()

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.sentences):
            result = self.sentences[self._index]
            self._index += 1
            return result
        raise StopIteration

    ##########################################################
    def update(self, line, buildPredict=False):
        punctuation = "©®-%$!?:,;\'\" @~&()=*_<=>{|}[/]^\\"

        line1 = line.replace(". ", "!")
        line1 = re.sub('[!?;,:\[\]\(\)]', "><", line1)
        sentences = [x.strip().lower() for x in line1.split("><") if x !='']
        # x.strip().lower() - used as kayer point for tokenize.case_sensitive switching.

        for i, item in enumerate(sentences):
        #{
            #word_sentence = [x.strip(string.punctuation) if x not in self.dictionary else x for x in item.split(" ") if (x != '')]
            
            word_sentence = [x.strip(punctuation) if x.strip(punctuation) in self.dictionary else x.strip(string.punctuation) 
                                for x in item.split(" ") if (x != '')]

            #sentences[i] = word_sentence

            tokens = []
            skip = False
            for w in word_sentence:
            #{
                #w = re.search("[\[\]\}\{=@\*]")
                if re.sub("[A-Za-z0-9#\'\./_&+-]", "", w) == "":
                    if ((w not in self.stopwords) and not w.isdigit() and len(w) > 1):

                        if (w in self.dictionary) or self.isConstructed(w):
                            tokens.append(w)
                            self.vocab.add(w)
                            self.vocab_freq[w] = self.vocab_freq.get(w, 0) + 1
                        elif w in self.tms:
                            if not buildPredict:
                                tokens.append(w) 
                        else:
                            if (w not in self.tms) and (w not in self.ignore):
                                self.u_vocab_freq[w] = self.u_vocab_freq.get(w, 0) + 1
            #}
            if buildPredict:
                self.prediction.add_tokens(tokens)

            tokens.append(";")
            sentences[i] = tokens
        #}
        return sentences
    ##########################################################
    def readDictionary(self):
        diix = Path("./dict/diixonary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open("./dict/diixonary.txt", 'r', encoding='utf-8').readlines()])

        diix = Path("./dict/dictionary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open("./dict/dictionary.txt", 'r', encoding='utf-8').readlines()])

        self.dictionary.update(self.stopwords)
        self.dictionary = set(sorted(self.dictionary))

        # read additional dictionaries

        path = Path("./dict/trademarks.txt")
        if path.exists():
            self.tms.update([line.replace('\n', '').lower() for line in open("./dict/trademarks.txt", 'r', encoding='utf-8').readlines()])
            self.tms = set(sorted(self.tms))

        path = Path("./dict/ignore.txt")
        if path.exists():
            self.ignore.update([line.replace('\n', '').lower() for line in open("./dict/ignore.txt", 'r', encoding='utf-8').readlines()])
            self.ignore = set(sorted(self.ignore))
    ##########################################################
    def isConstructed(self, word: string) -> bool:
        ws = re.split('[/-]', word)
        sz = len(ws)
        if (sz > 1) and (sz <= 3):
        #
            cntr = 0
            for w in ws:
            #
                if ((w not in self.stopwords) and (w not in self.dictionary)) or (w in self.tms):
                    break
                cntr += 1
            #
            return (len(ws) == cntr)
        #
        return False
    ##########################################################
    def finalize(self):
        print("finalizing >>")

        if len(self.u_vocab_freq) > 0:
        #
            print(">> u_vocab-freq")
            self.u_vocab_freq = sorted(self.u_vocab_freq.items(), key=itemgetter(1), reverse=True)

            f = open("un-vocab-sort.utf8", 'w', encoding='utf-8')
            for kv in self.u_vocab_freq:
            #
                word = kv[0]
                ws = re.split('[_/-]', word)
                sz = len(ws)
                if (sz == 1) and (kv[1] >= 20):
                    f.write(word + " ; " + str(kv[1]) + "\n")
            #
            f.close()
            print("<< u_vocab-freq")
        #

        if self.prediction.size() > 0:
        #{
            self.prediction.finalize()
        #}
        else:
        #{
            print(">> vocab")
            self.vocab = sorted(self.vocab)

            f = open("vocab.utf8", 'w', encoding='utf-8')
            for w in self.vocab:
                if w in self.dictionary:
                    continue

                f.write(w + " ; " + str(self.vocab_freq[w]) + "\n")

            f.close()
            print("<< vocab")

            self.vocab_freq = sorted(self.vocab_freq.items(), key=itemgetter(1), reverse=True)

            f = open("vocab-sort.utf8", 'w', encoding='utf-8')
            for kv in self.vocab_freq:
            #
                if kv[0] in self.dictionary:
                    continue

                f.write(kv[0] + " ; " + str(kv[1]) + "\n")
            #
            f.close()
            print("<< vocab-freq")
        #}
        print("<< finalizing")
        return
    ##########################################################
    def add_ngrams_freqDict(self, ngram_freq_dict, ngramList):
        for tpl in ngramList:
            if tpl in ngram_freq_dict:
                ngram_freq_dict[tpl] += 1
            else:
                ngram_freq_dict[tpl] = 1
        return
    ##########################################################
    def word_tokenize(self, in_str, stopwords = None):
        word_list = re.findall("(\w[\w'\./&-]*\w|\w)", in_str)
        if word_list:
            if stopwords:
                return [w for w in word_list if w not in stopwords]
            else:
                return word_list
        return []
    ##########################################################
    def predict_next(self, line):
        work_line = tokenize(line, self.stopwords)
        tokenList = self.word_tokenize(work_line)
        return self.prediction.predict_next(tokenList)
