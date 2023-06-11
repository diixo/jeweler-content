
import re
import string
from pathlib import Path

def analyze(filePath):

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
                0x201c: 0x0022, 0x201d: 0x0022, 0x021f: 0x0022, 
                0x2019: 0x0027, 0x2018: 0x0027, 0x201b: 0x0027, 0x0060: 0x0027, 
                0x00ab: 0x0020, 0x00bb: 0x0020, 0x2026: 0x002e }
            line = line.translate(translation)

            # remove cyrillic
            line = re.sub(r'[А-їЁІЇҐґ]', " ", line).strip()

            text = [item for item in re.split('[\ ]', line) if len(item.strip()) > 0 and not re.search(r'http|www|href', item, re.IGNORECASE)]
            
            word_it = "IT"
            punct = "$|!?:,;.\'\""
            for id, word in enumerate(text):
                word = re.sub(r'\b{}\b'.format(re.escape(word_it)), "I-T", word)

                word = re.sub("\|", "| ", word)

                cword = word.strip(punct).lower()

                if cword.isdigit():
                    text[id] = re.sub(cword, " ", word)
                elif cword in stopwords:
                    text[id] = re.sub(cword, "_", word, flags=re.I)
                else:
                    text[id] = word

            line = ' '.join([w for w in text if len(w.strip()) > 0])

            #print(line)

            if len(line) > 0:
                fw.write(line + "\n")

            print(count)

        count += 1

    fh.close()
    fw.close()
    return

###############################################

analyze("jeweler-content.txt")
