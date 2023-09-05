import re
from collections import Counter
from tokenizer import tokenize

########################################################################
# nltk.ngrams
def ngrams(content, n):
   ngramList = [tuple(content[i:i+n]) for i in range(len(content)-n+1)]
   return ngramList
########################################################################
def word_tokenize(str_line: str, stopwords = None):
   word_list = re.findall("(\w[\w'\./&-]*\w|\w)", str_line)
   if word_list:
      if stopwords:
         return [w for w in word_list if w not in stopwords]
      else:
         return word_list
   return []
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

class Prediction:
   
   def __init__(self, stopwordsPath="stopwords.txt"):
      self.unigrams = set()
      self.bigrams = set()
      self.trigrams = set()
      self.unigrams_freq_dict = {}  # freq_dict for unigrams
      self.bigrams_freq_dict  = {}  # freq_dict for bigrams
      self.trigrams_freq_dict = {}  # freq_dict for trigrams

   ##########################################################
   def predict(self, line):
      work_line = tokenize(line, self.stopwords)
      tokenList = word_tokenize(work_line)
        
      ngram = {1:[], 2:[]}

      for i in range(2):
         ngram[i+1] = list(ngrams(tokenList, i+1))[-1]
   ##########################################################

   def predict_next(self, str_line):
      tokenList = word_tokenize(str_line)
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
         return (str_line, [[item1[0] for item1 in pred1], [item2[0] for item2 in pred2]])

      if (sz == 2):
         pair = [tokenList[0], tokenList[1]]
         pred_3 = predict_next_3_words(pair, trigrams_probDist)
         return (str_line, [item[0] for item in pred_3])
      return []
   ##########################################################
   def size(self):
      return len(self.unigrams)
   ##########################################################
   
   def add_tokens(self, tokens: list):
      ngrams_1 = ngrams(tokens, 1)
      ngrams_2 = ngrams(tokens, 2)
      ngrams_3 = ngrams(tokens, 3)

      self.add_ngrams_freqDict(self.unigrams_freq_dict, ngrams_1)
      self.add_ngrams_freqDict(self.bigrams_freq_dict,  ngrams_2)
      self.add_ngrams_freqDict(self.trigrams_freq_dict, ngrams_3)

      self.unigrams.update(ngrams_1)  # unique inserting
      self.bigrams.update(ngrams_2)   # unique inserting
      self.trigrams.update(ngrams_3)  # unique inserting

   def finalize(self):
      self.unigrams = sorted(self.unigrams)
      self.bigrams  = sorted(self.bigrams)
      self.trigrams = sorted(self.trigrams)

      print(">> unigrams, bigrams, trigrams: ({}), ({}), ({})".format(len(self.unigrams), len(self.bigrams), len(self.trigrams)))

      f = open("unigrams.utf8", 'w', encoding='utf-8')
      for w in self.unigrams:
         if w[0] not in self.dictionary:
            f.write(w[0] + "\n")
      f.close()

      f = open("bigrams.utf8", 'w', encoding='utf-8')
      for w in self.bigrams:
         f.write(w[0] + "; " + w[1] + "\n")
      f.close()

      print("<< unigrams_fr_dict, bigrams_fr_dict, trigrams_fr_dict: ({}), ({}), ({})".format(
         len(self.unigrams_freq_dict), len(self.bigrams_freq_dict), len(self.trigrams_freq_dict)))
