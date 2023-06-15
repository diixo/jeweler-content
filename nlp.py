
def ngrams(content, n):
    ngramList = [tuple(content[i:i+n]) for i in range(len(content)-n+1)]
    return ngramList
#######################

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
