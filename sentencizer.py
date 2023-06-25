# Analytics Vidhya: Building Language Models in NLP

import re
import string
from operator import itemgetter
from tokenizer import tokenize
from collections import Counter
from pathlib import Path

########################################################################
# nltk.ngrams
def ngrams(content, n):
    ngramList = [tuple(content[i:i+n]) for i in range(len(content)-n+1)]
    return ngramList
########################################################################
def predict_next_word_smoothed(last_word, probDist):
    next_word = {}
    for k in probDist:
        if k[0] == last_word[0]:
            next_word[k[1]] = probDist[k]
    k = Counter(next_word)
    high = k.most_common(1) 
    return high[0]
########################################################################
def predict_next_3_words_smoothed(token, probDist):
    pred1 = []
    pred2 = []
    next_word = {}
    for i in probDist:
        if i[0] == token:
            next_word[i[1]] = probDist[i]
    k = Counter(next_word)
    high = k.most_common(2) 
    w1a = high[0]
    w1b = high[1]
    w2a = predict_next_word_smoothed(w1a, probDist)
    w3a = predict_next_word_smoothed(w2a, probDist)
    w2b = predict_next_word_smoothed(w1b, probDist)
    w3b = predict_next_word_smoothed(w2b, probDist)
    pred1.append(w1a)
    pred1.append(w2a)
    pred1.append(w3a)
    pred2.append(w1b)
    pred2.append(w2b)
    pred2.append(w3b)
    return pred1, pred2
########################################################################
def predict_next_word(last_word, probDist):
    next_word = {}
    for k in probDist:
        if k[0:2] == last_word:
            next_word[k[2]] = probDist[k]
    k = Counter(next_word)
    high = k.most_common(1) 
    return high[0]
########################################################################
def predict_next_3_words(token, probDist):
    pred = []
    next_word = {}
    for i in probDist:
        if list(i[0:2]) == token:
            next_word[i[2]] = probDist[i]
    k = Counter(next_word)
    high = k.most_common(10)
    if len(high) > 0:
        w1a = high[0]
        print("<< high:", [ item[0] for item in high ])
        tup = (token[1], w1a[0])
        w2a = predict_next_word(tup, probDist)
        tup = (w1a[0], w2a[0])
        w3a = predict_next_word(tup, probDist)
        pred.append(w1a)
        pred.append(w2a)
        pred.append(w3a)
    return pred
########################################################################

class Sentencizer:

    def __init__(self, stopwordsPath="stopwords.txt"):
        self.sentences = []
        self._index = 0
        self.stopwords = set()
        self.vocab = set()
        self.vocab_freq = {}
        self.unigrams = set()
        self.bigrams = set()
        self.trigrams = set()
        s = set()
        s.update([line.replace('\n', '') for line in open(stopwordsPath, 'r', encoding='utf-8').readlines()])
        self.stopwords = sorted(s)
        
        self.tms = set()
        self.ignore = set()

        self.unigrams_freq_dict = {}  # freq_dict for unigrams
        self.bigrams_freq_dict  = {}  # freq_dict for bigrams
        self.trigrams_freq_dict = {}  # freq_dict for trigrams
        self.dictionary         = set()
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
        punctuation = "©®-%$!?:,;.\'\" @~&()=*"

        line1 = re.sub('[!?.;,:]', "><", line)
        sentences = [x.strip().lower() for x in line1.split("><") if x !='']
        # x.strip().lower() - used as kayer point for tokenize.case_sensitive switching.

        for i, item in enumerate(sentences):
        #{
            word_sentence = [x.strip(string.punctuation) for x in item.split(" ") if (x != '')]
            #sentences[i] = word_sentence

            tokens = []
            skip = False
            for w in word_sentence:
            #{
                #w = re.search("[\[\]\}\{=@\*]")
                if re.sub("[A-Za-z0-9#\'\./_&+-]", "", w) == "":
                    if ((w not in self.stopwords) and not w.isdigit() and len(w) > 1):

                        #if (w not in self.tms) and (w not in self.ignore):
                        if w in self.dictionary or self.isConstructed(w):
                            tokens.append(w)
                            self.vocab.add(w)
                            self.vocab_freq[w] = self.vocab_freq.get(w, 0) + 1
            #}
            sentences[i] = tokens
            if buildPredict:
            #
                ngrams_1 = ngrams(tokens, 1)
                ngrams_2 = ngrams(tokens, 2)
                ngrams_3 = ngrams(tokens, 3)

                self.add_ngrams_freqDict(self.unigrams_freq_dict, ngrams_1)
                self.add_ngrams_freqDict(self.bigrams_freq_dict,  ngrams_2)
                self.add_ngrams_freqDict(self.trigrams_freq_dict, ngrams_3)

                self.unigrams.update(ngrams_1)  # unique inserting
                self.bigrams.update(ngrams_2)   # unique inserting
                self.trigrams.update(ngrams_3)  # unique inserting
            #
        #}
        return sentences
    ##########################################################
    def readDictionary(self):
        diix = Path("./dict/diixonary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open("./dict/diixonary.txt", 'r', encoding='utf-8').readlines()])
            #print("diixonary.sz=", len(self.dictionary))

        diix = Path("./dict/dictionary.txt")
        if diix.exists():
            self.dictionary.update([line.replace('\n', '') for line in open("./dict/dictionary.txt", 'r', encoding='utf-8').readlines()])
            #print("dictionary.sz=", len(self.dictionary))

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

        if len(self.unigrams) > 0:
        #{
            self.unigrams = sorted(self.unigrams)
            self.bigrams  = sorted(self.bigrams)
            self.trigrams = sorted(self.trigrams)

            print("<< unigrams, bigrams, trigrams: ({}), ({}), ({})".format(len(self.unigrams), len(self.bigrams), len(self.trigrams)))

            print("<< unigrams_fr_dict, bigrams_fr_dict, trigrams_fr_dict: ({}), ({}), ({})".format(
                len(self.unigrams_freq_dict), len(self.bigrams_freq_dict), len(self.trigrams_freq_dict)))

            f = open("unigrams.utf8", 'w', encoding='utf-8')
            for w in self.unigrams:
                if w[0] not in self.dictionary:
                    f.write(w[0] + "\n")
            f.close()
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
    def predict(self, line):
        work_line = tokenize(line, self.stopwords)
        tokenList = self.word_tokenize(work_line)
        
        ngram = {1:[], 2:[]}

        for i in range(2):
            ngram[i+1] = list(ngrams(tokenList, i+1))[-1]

        return
    ##########################################################
    def predict_next(self, line):
        work_line = tokenize(line, self.stopwords)
        tokenList = self.word_tokenize(work_line)

        sz = len(tokenList)

        bigrams_probDist = {}
        V = len(self.bigrams)
        for i in self.bigrams_freq_dict:

            bigrams_probDist[i] = (self.bigrams_freq_dict[i] + 1) / (self.unigrams_freq_dict[tuple([i[0]])] + V)

        trigrams_probDist = {}
        for i in self.trigrams_freq_dict:
            trigrams_probDist[i] = (self.trigrams_freq_dict[i] + 1) / (self.bigrams_freq_dict[i[0:2]] + V)

        if (sz == 1):
            token = tokenList[0]
            pred1, pred2 = predict_next_3_words_smoothed(token, bigrams_probDist)
            return (work_line, [[item1[0] for item1 in pred1], [item2[0] for item2 in pred2]])

        if (sz == 2):
            pair = [tokenList[0], tokenList[1]]
            pred_3 = predict_next_3_words(pair, trigrams_probDist)
            return (work_line, [item[0] for item in pred_3])
        return []
    ##########################################################
