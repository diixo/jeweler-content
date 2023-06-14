
import re
import string
from operator import itemgetter

class Sentencizer: #from NLPTools

    def __init__(self, split_characters=['.', '?', '!', ':', ';', ','], delimiter_token='<split>'):
        self.sentences = []
        self._split_characters = split_characters
        self._delimiter_token = delimiter_token
        self._index = 0
        self._stopwords = [line.replace('\n', '') for line in open("stopwords.txt", 'r', encoding='utf-8').readlines()]
        self.vocab = set()
        self.vocab_freq = {}
        self.vocab_freq_sorted = {}

    def sentencize(self, input_line):
        work_sentence = input_line.strip()
        sentences = []

        if (work_sentence == ""):
            return

        for character in self._split_characters:
            work_sentence = work_sentence.replace("\n",  " ")
            work_sentence = work_sentence.replace(character, character + "" + self._delimiter_token)

        sentences = [x.strip().lower() for x in work_sentence.split(self._delimiter_token) if x !='']

        token_boundaries = [' ', ',', '.']

        for i in range(len(sentences)):
            work_sentence = sentences[i]

            for delimiter in token_boundaries:
                work_sentence = work_sentence.replace(delimiter, self._delimiter_token)

            sentences[i] = [x.strip() for x in work_sentence.split(self._delimiter_token) if (x != '')]

            work_sentence = []
            for w in sentences[i]:
                w = w.strip(string.punctuation)
                if ((w != '') and (w not in self._stopwords) and not w.isdigit()):
                    work_sentence.append(w)

                    if w in self.vocab_freq:
                        self.vocab_freq[w] += 1
                        continue
                        # print (word, vocab[word])
                    self.vocab_freq[w] = 1

            if (len(work_sentence) > 0):
                #print(' '.join(sentences[i]))
                #print(' '.join(work_sentence))
                self.sentences.append(work_sentence)
                self.vocab.update(set(work_sentence))
        #print(self.vocab)

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
