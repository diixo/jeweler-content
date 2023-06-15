
import re
import string
from pathlib import Path
from sentencizer import Sentencizer
from tokenizer import tokenize

def analyze(filePath):
    path = Path(filePath)
    if path.exists() == False: return

    sentencizer = Sentencizer()

    newName = path.stem + ".utf8"

    fh = open(filePath, 'r', encoding='utf-8')
    fw = open(newName,  'w', encoding='utf-8')
       
    count = 0
    while True:
        line = fh.readline()
        if not line:
            break

        if count > 23:

            line = tokenize(line, sentencizer.stopwords)
            #print(line)

            sentencizer.update(line)

            if len(line) > 0:
                fw.write(line + "\n")

            print(count)
            #if count > 26:
            #    break

        count += 1

    fh.close()
    fw.close()
    sentencizer.finalize()
    return

###############################################

#analyze("E:/jeweler_content.txt")
analyze("jeweler-content.txt")
