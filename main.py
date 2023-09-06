
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

    count = 1
    while True:
    #{
        line = fh.readline()
        if not line:
            break

        if count >= lines_indent:
        #{
            line = tokenize(line, sentencizer.stopwords, case_sensitive=True)

            result = sentencizer.update(line, buildPredict)

            if len(line) > 0:
                if False:
                    fw.write(line + " ;" + str(count) + "\n")
                else:
                    for sent in result:
                        fw.write(" ".join([w for w in sent]))
                    fw.write(";" + str(count) + '\n')
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
    #analyze("data/jeweler-content.txt", 24, buildPredict=False)

    analyze("data/dataset.txt", buildPredict=True)

    #analyze("E:/jeweler_content.txt", 23, buildPredict=False)
    #analyze("E:/jeweler_content-2511937.txt", 23, buildPredict=False)

    #analyze("data/train-nn.txt", buildPredict=True)
    #phrase, result = sentencizer.predict_next("text clustering")
    #phrase, result = sentencizer.predict_next("data science")

###############################################################
if __name__ == "__main__":
    main()
