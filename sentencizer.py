
import re
import string
from operator import itemgetter

####################################################################################################
# nltk.ngrams
def ngrams(content, n):
    ngramList = [tuple(content[i:i+n]) for i in range(len(content)-n+1)]
    #print(ngramList)
    return ngramList
####################################################################################################

# unigrams_freqDist = get_ngrams_freqDist(unigrams, 1)
# unigrams_Processed_freqDist = get_ngrams_freqDist(unigrams_Processed, 1)  # cleared of stopwords
# bigrams_freqDist = get_ngrams_freqDist(bigrams, 2)
# bigrams_Processed_freqDist = get_ngrams_freqDist(bigrams_Processed, 2)    # cleared of stopwords
# trigrams_freqDist = get_ngrams_freqDist(trigrams, 3)
# trigrams_Processed_freqDist = get_ngrams_freqDist(trigrams_Processed, 3)  # cleared of stopwords

def get_ngrams_freqDist(ngramList, n):
    ngram_freq_dict = {}
    for ngram in ngramList:
        if ngram in ngram_freq_dict:
            ngram_freq_dict[ngram] += 1
        else:
            ngram_freq_dict[ngram] = 1
    return ngram_freq_dict
####################################################################################################

class Sentencizer:

    def __init__(self, stopwordsPath="stopwords.txt"):
        self.sentences = []
        self._index = 0
        self.stopwords = [line.replace('\n', '') for line in open(stopwordsPath, 'r', encoding='utf-8').readlines()]
        self.vocab = set()
        self.vocab_freq = {}
        self.vocab_freq_sorted = {}
        self.unigrams = set()
        self.bigrams = set()
        self.trigrams = set()

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
    ################################################
    def tokenize(self, line):
        result = []

        line1 = re.sub('[!?.;,:]', "><", line)
        sentences = [x.strip().lower() for x in line1.split("><") if x !='']

        for i, item in enumerate(sentences):
        #{    
            sentences[i] = [x.strip() for x in item.split(" ") if (x != '')]

            work_sentence = []
            for w in sentences[i]:
                w = w.strip(string.punctuation)
                if ((w != '') and (w not in self.stopwords) and not w.isdigit() and len(w) > 1):
                    work_sentence.append(w)

            #if (len(work_sentence) > 0):
            #    print("<< ", ' '.join(work_sentence))
            #if work_sentence:
            #    result.append(work_sentence)
            
            self.unigrams.update(ngrams(work_sentence, 1))  # unique inserting
            self.bigrams.update(ngrams(work_sentence, 2))   # unique inserting
            self.trigrams.update(ngrams(work_sentence, 3))  # unique inserting
        #}
        return
    ################################################
    def finalize(self):
        if len(self.unigrams) > 0:
        #{
            self.unigrams = sorted(self.unigrams)
            self.bigrams = sorted(self.bigrams)
            self.trigrams = sorted(self.trigrams)

            print("<< unigrams, bigrams, trigrams: ({}), ({}), ({})".format(len(self.unigrams), len(self.bigrams), len(self.trigrams)))

            f = open("unigrams.utf8", 'w', encoding='utf-8')
            for w in self.unigrams:
                f.write(str(w[0]) + "\n")
            f.close()
        #}
        return
    ################################################
