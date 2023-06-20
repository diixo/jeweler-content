
import re
import string
from regulars import is_digit_inside

def tokenize(line, stopwords):
    punct = "©®-%$!?:,;.\'\" "

    # remove html
    line = line.replace('&amp;' , '&')
    line = line.replace('&lt;'  , '<')
    line = line.replace('&gt;'  , '>')
    line = line.replace('&quot;', '"')
    line = line.replace('&#124;', '|')
    line = line.replace('&#39;', '\'')


    line = line.replace('&amp;' , '&')
    line = line.replace('&#39;', '\'')
    line = line.replace('&nbsp;', ' ')
    line = line.replace('\u0080\u0099', '\u0027')

    # normalize apostrophs
    translation = {
        0xfffd: 0x0020, 0x00b7: 0x0020, 0xfeff: 0x0020, 0x2026: 0x0020,
        0x2713: 0x0020, 0x205F: 0x0020, 0x202c: 0x0020, 0x202a: 0x0020, 
        0x200e: 0x0020, 0x200d: 0x0020, 0x200c: 0x0020, 0x200b: 0x0020,
        0x2002: 0x0020, 0x2003: 0x0020,
        0x2015: 0x002d, 0x201e: 0x0020, 0x2028: 0x0020, 0x2032: 0x0027,
        0x2012: 0x002d, 0x0080: 0x0020, 0x0094: 0x0020, 0x009c: 0x0020,
        0xFE0F: 0x0020, 0x200a: 0x0020, 0x202f: 0x0020, 0x2033: 0x0020,
        0x2013: 0x0020, 0x00a0: 0x0020, 0x2705: 0x0020, 0x2714: 0x0020, # 0x2013: 0x002d
        0x201c: 0x0020, 0x201d: 0x0020, 0x021f: 0x0020, 0x0022: 0x0020,
        0x2019: 0x0027, 0x2018: 0x0027, 0x201b: 0x0027, 0x0060: 0x0027, 
        0x00ab: 0x0020, 0x00bb: 0x0020, 0x2026: 0x002e, 0x2014: 0x0020 } # 0x2014: 0x002d
    line = line.translate(translation)

    # remove cyrillic
    line = re.sub(r'[А-їЁІЇҐґ№]', "", line)
    line = re.sub(r'[_\(\)<>/\[\]]', " ", line)
    line = re.sub("\|", " ! ", line).strip()

    text = [item for item in re.split('[\ ]', line) if len(item.strip()) > 0 and not re.search(r'http|www|href|rel=|url=|noopener|noreferrer|class=|text=', 
        item, re.IGNORECASE)]
    
    word_it = "IT"

    for id, word in enumerate(text):

        word = re.sub(r'\b{}\b'.format(re.escape(word_it)), "I-T", word).lower()

        cword = word.strip(punct).lower()

        if is_digit_inside(cword):
            #word = re.sub(r'[-+\$]*(?:\d+[%]*(?:\.\,\:\d*[%]*)?|\.\,\:\d+[%]*)', "", word)
            word =  re.sub(r'[-+\$]*(?:\d+(?:\.\d*)?|(?::\d*)?|\.\d+)[%]*', "", word, flags=re.I)
            cword = word

        if cword in stopwords:
            text[id] = re.sub(cword, "", word, flags=re.I)
        else:
            text[id] = word if (len(word)) else ""

    line = ' '.join([w for w in text if len(w.strip()) > 0])
    return line
