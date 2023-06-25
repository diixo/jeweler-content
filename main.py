
from pathlib import Path
from sentencizer import Sentencizer
from tokenizer import tokenize

###############################################################
sentencizer = Sentencizer()

def analyze(filePath, lines_indent = -1):
    global sentencizer

    path = Path(filePath)
    if path.exists() == False: return

    newName = path.stem + "-cyr.utf8"

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
            line = tokenize(line, sentencizer.stopwords)

            sentencizer.update(line)

            if len(line) > 0:
                fw.write(line + "\n")

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
    analyze("E:/jeweler_content.txt")
    #phrase, result = sentencizer.predict_next("text clustering")

    #analyze("data/dataset.txt")
    #phrase, result = sentencizer.predict_next("data science")

###############################################################
if __name__ == "__main__":
    main()
