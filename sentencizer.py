# Analytics Vidhya: Building Language Models in NLP

import re
import string
from operator import itemgetter
from tokenizer import tokenize
from collections import Counter

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
        if i[0:2] == token:
            next_word[i[2]] = probDist[i]
    k = Counter(next_word)
    high = k.most_common(2)
    w1a = high[0]
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
        self.vocab_freq_sorted = {}
        self.unigrams = set()
        self.bigrams = set()
        self.trigrams = set()
        s = set()
        s.update([line.replace('\n', '') for line in open(stopwordsPath, 'r', encoding='utf-8').readlines()])
        self.stopwords = sorted(s)

        self.unigrams_freq_dict = {}  # freq_dict for unigrams
        self.bigrams_freq_dict  = {}  # freq_dict for bigrams
        self.trigrams_freq_dict = {}  # freq_dict for trigrams

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.sentences):
            result = self.sentences[self._index]
            self._index += 1
            return result
        raise StopIteration

    def readFile(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        count = 0;
        while True:
            line = f.readline()
            if not line:
                break;

            count+=1
            self.sentencize(line)

        f.close()
        self.vocab = sorted(self.vocab)
        self.vocab_freq_sorted = sorted(self.vocab_freq.items(), key=itemgetter(1), reverse=True)
        return
    ##########################################################
    def update(self, line):
        result = []

        line1 = re.sub('[!?.;,:]', "><", line)
        sentences = [x.strip().lower() for x in line1.split("><") if x !='']

        for i, item in enumerate(sentences):
        #{    
            sentences = [x.strip() for x in item.split(" ") if (x != '')]

            work_sentence = []
            for w in sentences:
                w = w.strip(string.punctuation)
                if ((w != '') and (w not in self.stopwords) and not w.isdigit() and len(w) > 1):
                    work_sentence.append(w)

            ngrams_1 = ngrams(work_sentence, 1)
            ngrams_2 = ngrams(work_sentence, 2)
            ngrams_3 = ngrams(work_sentence, 3)

            self.add_ngrams_freqDict(self.unigrams_freq_dict, ngrams_1)
            self.add_ngrams_freqDict(self.bigrams_freq_dict,  ngrams_2)
            self.add_ngrams_freqDict(self.trigrams_freq_dict, ngrams_3)

            self.unigrams.update(ngrams_1)  # unique inserting
            self.bigrams.update(ngrams_2)   # unique inserting
            self.trigrams.update(ngrams_3)  # unique inserting
        #}
        self.unigrams = set(sorted(self.unigrams))
        self.bigrams  = set(sorted(self.bigrams))
        self.trigrams = set(sorted(self.trigrams))

        #self.add_ngrams_freqDict = OrderedDict(sorted(self.unigrams_freq_dict.items()))
        #self.add_ngrams_freqDict = OrderedDict(sorted(self.bigrams_freq_dict.items()))
        #self.add_ngrams_freqDict = OrderedDict(sorted(self.trigrams_freq_dict.items()))
        
        return
    ##########################################################
    def finalize(self):
        if len(self.unigrams) > 0:
        #{
            self.unigrams = sorted(self.unigrams)
            self.bigrams = sorted(self.bigrams)
            self.trigrams = sorted(self.trigrams)

            print("<< unigrams, bigrams, trigrams: ({}), ({}), ({})".format(len(self.unigrams), len(self.bigrams), len(self.trigrams)))

            print("<< unigrams_fr_dict, bigrams_fr_dict, trigrams_fr_dict: ({}), ({}), ({})".format(
                len(self.unigrams_freq_dict), len(self.bigrams_freq_dict), len(self.trigrams_freq_dict)))   

            f = open("unigrams.utf8", 'w', encoding='utf-8')
            for w in self.unigrams:
                f.write(str(w[0]) + "\n")
            f.close()
        #}
        return
    ##########################################################
    def add_ngrams_freqDict(self, ngram_freq_dict, ngramList):
        for ngram in ngramList:
            if ngram in ngram_freq_dict:
                ngram_freq_dict[ngram] += 1
            else:
                ngram_freq_dict[ngram] = 1
        return
    ##########################################################
    def word_tokenize(self, in_str, stopwords = None):
        word_list = re.findall("(\w[\w'\.&\-]*\w|\w)", in_str)
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
        V = 1000 #len(self.unigrams_freq_dict)
        for i in self.bigrams_freq_dict:

            bigrams_probDist[i] = (self.bigrams_freq_dict[i] + 1) / (self.unigrams_freq_dict[tuple([i[0]])] + V)

        trigrams_probDist = {}
        for i in self.trigrams_freq_dict:
            trigrams_probDist[i] = (self.trigrams_freq_dict[i] + 1) / (self.bigrams_freq_dict[i[0:2]] + V)

        if (sz == 1):
            token = tokenList[0]

            pred1, pred2 = predict_next_3_words_smoothed(token, bigrams_probDist)
            print(pred1, pred2)

        if (sz == 2):
            pair = [tokenList[0], tokenList[1]]

            pred1, pred2 = predict_next_3_words(pair, trigrams_probDist)
            print(pred1, pred2)
        return
    ##########################################################
