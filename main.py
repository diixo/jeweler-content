
from pathlib import Path
from sentencizer import Sentencizer
from tokenizer import tokenize
import re
###############################################################
sentencizer = Sentencizer()

def analyze(filePath, lines_indent = -1, buildPredict = False):
    global sentencizer

    path = Path(filePath)
    if path.exists() == False: return

    newName = path.stem + "-cyr.utf8"

    fh = open(filePath, 'r', encoding='utf-8')
    fw = open(newName,  'w', encoding='utf-8')

    count = 1
    while True:
    #{
        line = fh.readline()
        if not line:
            print(count)
            break

        if count >= lines_indent:
        #{
            line = tokenize(line, sentencizer.stopwords)

            result = sentencizer.update(line, buildPredict)

            if len(line) > 0:
            #
                if True:
                    fw.write(line + " ;" + str(count) + "\n")
                else:
                    for sent in result:
                    #
                        fw.write(" ".join([w for w in sent]))
                    #
                    fw.write(";" + str(count) + '\n')
            #
            if count % 100 == 0: print(count)
        #}
        count += 1
    #}
    fh.close()
    fw.close()
    sentencizer.finalize()
    return

###############################################################

def main():
    #print(re.findall(r'[А-Яа-яЁё]+', 'Привет, мир!'))

    #analyze("data/jeweler-content.txt", 23)

    #analyze("data/train-nn.txt")
    analyze("E:/jeweler_content-2569456.txt")
    #phrase, result = sentencizer.predict_next("text clustering")

    #analyze("data/dataset.txt")
    #phrase, result = sentencizer.predict_next("data science")

###############################################################
if __name__ == "__main__":
    main()
