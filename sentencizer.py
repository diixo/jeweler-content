
import re
import string
from operator import itemgetter

class Sentencizer: #from NLPTools

    def __init__(self, split_characters=['.', '?', '!', ':', ';', ',', '|'], delimiter_token='<split>'):
        self.sentences = []
        self._index = 0
        self._stopwords = [line.replace('\n', '') for line in open("stopwords.txt", 'r', encoding='utf-8').readlines()]
        self.vocab = set()
        self.vocab_freq = {}
        self.vocab_freq_sorted = {}

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
