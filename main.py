
import re
import string
from pathlib import Path
from regulars import is_digit_inside

stopwords = []

def tokenize(line):
    global stopwords
    result = []

    line1 = re.sub('[!?.;,:]', "><", line)
    sentences = [x.strip().lower() for x in line1.split("><") if x !='']

    for i, item in enumerate(sentences):
        
        sentences[i] = [x.strip() for x in item.split(" ") if (x != '')]

        work_sentence = []
        for w in sentences[i]:
            w = w.strip(string.punctuation)
            if ((w != '') and (w not in stopwords) and not w.isdigit() and len(w) > 1):
                work_sentence.append(w)

        #if (len(work_sentence) > 0):
        #    print("<< ", ' '.join(work_sentence))
        if work_sentence:
            result.append(work_sentence)
    ###################################
    return result
#######################################

def analyze(filePath):
    global stopwords

    path = Path(filePath)
    if path.exists() == False: return

    newName = path.stem + ".utf8"

    stopwords = [line.replace('\n', '') for line in open("stopwords.txt", 'r', encoding='utf-8').readlines()]
    s = set()
    s.update(stopwords)
    stopwords = sorted(s)
    ##########################################
    fh = open(filePath, 'r', encoding='utf-8')
    fw = open(newName,  'w', encoding='utf-8')
    
    punct = "-%$!?:,;.\'\" "
    
    count = 0
    while True:
        line = fh.readline()
        if not line:
            break

        if count > 23:

            # remove html-blocks
            line = line.replace('&amp;' , '&')
            line = line.replace('&lt;'  , '<')
            line = line.replace('&gt;'  , '>')
            line = line.replace('&quot;', '"')
            line = line.replace('&#124;', '|')
            line = line.replace('&#39;', '\'')


            line = line.replace('&amp;' , '&')
            line = line.replace('&#39;', '\'')
            line = line.replace('&nbsp;', ' ')

            # normalize apostrophs
            translation = {
                0x201c: 0x0020, 0x201d: 0x0020, 0x021f: 0x0020, 0x0022: 0x0020,
                0x2019: 0x0027, 0x2018: 0x0027, 0x201b: 0x0027, 0x0060: 0x0027, 
                0x00ab: 0x0020, 0x00bb: 0x0020, 0x2026: 0x002e, 0x2014: 0x0020 }
            line = line.translate(translation)

            # remove cyrillic
            line = re.sub(r'[А-їЁІЇҐґ№]', "", line)
            line = re.sub(r'[_\(\)<>]', " ", line)
            line = re.sub("\|", " ! ", line).strip()

            # L' ', L',', L'!', L';', L'\"', L'|'

            text = [item for item in re.split('[\ ]', line) if len(item.strip()) > 0 and not re.search(r'http|www|href|rel=|url=|noopener|noreferrer|class=', item, re.IGNORECASE)]
            
            word_it = "IT"

            for id, word in enumerate(text):

                word = re.sub(r'\b{}\b'.format(re.escape(word_it)), "I-T", word)

                cword = word.strip(punct)

                if is_digit_inside(cword.lower()):
                    #print(">>", word)
                    #word = re.sub(r'[-+$]*(?:\d+[%]*(?:\.\,\:\d*[%]*)?|\.\,\:\d+[%]*)', "", word)
                    word =  re.sub(r'[-+\$]*(?:\d+(?:\.\d*)?|(?::\d*)?|\.\d+)[%]*', "", word, flags=re.I)
                    cword = word.lower()
                    #print("<<", word)
                else:
                    cword = cword.lower()

                if cword in stopwords:
                    text[id] = re.sub(cword, "", word, flags=re.I)
                else:
                    text[id] = word

            line = ' '.join([w for w in text if len(w.strip()) > 0])
            #print(line)


            ###########################
            #sentences = tokenize(line)
            #bigrams=[]
            #trigrams=[]
            #for content in sentences:
            #    print(content)
            #    bigrams.extend(ngrams(content, 2))
            #    trigrams.extend(ngrams(content, 3))
            #print(sentences)
            ############################
            #if bigrams: print(bigrams)

            if len(line) > 0:
                fw.write(line + "\n")

            print(count)
            #if count > 26:
            #    break

        count += 1

    fh.close()
    fw.close()
    return

###############################################

#analyze("E:/jeweler_content.txt")
analyze("jeweler-content.txt")
