
from pathlib import Path
from sentencizer import Sentencizer
from tokenizer import tokenize

###############################################################
sentencizer = Sentencizer()

def analyze(filePath, lines_indent = -1, buildPredict = False):
    global sentencizer

    path = Path(filePath)
    if path.exists() == False: return

    newName = path.stem + ".utf8"

    fh = open(filePath, 'r', encoding='utf-8')
    fw = open(newName,  'w', encoding='utf-8')

    count = 0
    while True:
    #{
        line = fh.readline()
        if not line:
            break

        if count > lines_indent:
        #{
            line = tokenize(line, sentencizer.stopwords, case_sensitive=True)

            result = sentencizer.update(line, buildPredict)

            if len(line) > 0:
                if True:
                        fw.write(line + "\n")
                else:
                    for sent in result:
                        fw.write(" ".join([w for w in sent]) + " ")
                    fw.write('\n')

            print(count)
        #}
        count += 1
    #}
    fh.close()
    fw.close()
    sentencizer.finalize()
    return

###############################################################

def main():
    #analyze("data/jeweler-content.txt", 23)

    #analyze("data/train-nn.txt")
    analyze("E:/jeweler_content.txt", 23, buildPredict=True)

    #phrase, result = sentencizer.predict_next("text clustering")

    #analyze("data/dataset.txt")
    #phrase, result = sentencizer.predict_next("data science")

###############################################################
if __name__ == "__main__":
    main()
