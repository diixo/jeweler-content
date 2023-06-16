
from pathlib import Path
from sentencizer import Sentencizer
from tokenizer import tokenize

sentencizer = Sentencizer()

def analyze(filePath, lines_indent = -1):
    global sentencizer

    path = Path(filePath)
    if path.exists() == False: return

    newName = path.stem + ".utf8"

    fh = open(filePath, 'r', encoding='utf-8')
    fw = open(newName,  'w', encoding='utf-8')
       
    count = 0
    while True:
        line = fh.readline()
        if not line:
            break

        if count > lines_indent:

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

#analyze("E:/jeweler_content.txt", 23)
analyze("jeweler-content.txt", 23)
