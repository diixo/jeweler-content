import re

# is digit wrapped by another symbols:
# re.search('(?<!\d)\d(?!\d)', str)

# real number:
# re.search('[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', str)

def is_digit_inside(str):
    if re.search('(?<![A-Za-z0-9\$])[-+\$]*(?:\d+[%]*(?:\.,:\d*[%]*)?|\.,:\d+[%]*)(?![^\ ,!?])', str) is None:
        return False
    return True

    return re.search('(?<![A-Za-z.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?!\d\w)', str)
    return re.search('(?<!\d[A-Za-z])[-+$ ]?(?:\d+(?:\.\:\d*)?|\.\:\,\d+)[$%]*(?![A-Za-z\-])', str)

def test():

    ss = "$0.2%"
    ss = re.sub(r'[$]?[-+]?[\d]*[.][\d]+', "", ss)
    print(ss)

    ss = "$.225%"
    ss = re.sub(r'[$]?[-+]?[\d]*[.][\d]+', "", ss)
    print(ss)

    ss = "$.225%."
    ss = re.sub(r'[$]?[-+]?[\d]*[.][\d]+', "", ss)
    print(ss)

    ss = "$.225%|"
    ss = re.sub(r'[$]?[-+]?[\d]*[.][\d]+', "", ss)
    print(ss)

    ss = "$+.225% |"
    ss = "$,225% |"
    ss = "$:225% |"
    ss = "$+55%%%   "
    ss = re.sub(r'[$]?[-+]?[\d]*[.,\:]?[\d]+[ %\"\']*', " ", ss)
    print("-->>", ss)

    # should return true
    t_test = [
        "160,", "160, ",
        "160", "$$160", "-160,0 ", "-160.0 ", "-160:0 ", "160.0 ", " -160,0", " -160.0", " -160:0", " 160.0"
        "A 160.0 Z", "A 1600 Z", "A 160,0 Z", "A 160:0 Z", "A 1600 Z", "A 160:0 Z", "-160,0", "-160.0", "-160:0", "160.0"
        "A $$160.0 Z", "A $$1600 Z", "A $$160,0 Z", "A $$160:0 Z", "A $$1600 Z", "A $$160:0 Z", "$$-160,0", "$$-160.0", "$$-160:0", "$$160.0", 

         "160%%", "$$160%%", "-160,0%% ", "-160.0%% ", "-160:0%% ", "160.0%% ", " -160,0%%", " -160.0%%", " -160:0%%", " 160.0%%"
        ]

    # should return false
    f_test = [ 
        "160.", "160. ",
        "A 160.0Z", "A1600 Z", "A160.0Z", "A 160:0Z", "A1600 Z", "A160:0Z", "A 160. Z", 
        "A160", "A160Z", "160-Z", "160Z", "160.Z", "160.", "160.Z", "160:", "160.0.Z" 
        
        "A $$160.0Z", "A$$1600 Z", "A$$160.0Z", "A $$160:0Z", "A$$1600 Z", "A$$160:0Z", "A $$160. Z", 
        "A$$160", "A$$160Z", "$$160-Z", "$$160Z", "$$160.Z", "$$160.", "$$160.Z", "$$160:", "$$160.0.Z",

        "A $$160.0%%Z", "A$$1600%% Z", "A$$160.0%%Z", "A $$160:0Z%%", "A$$1600%% Z", "A$$160:0%%Z", "A $$160%%. Z", 
        "A$$160%%", "A$$160%%Z", "$$160%%-Z" "$$160%%Z", "$$160%%.Z", "$$160%%.", "$$160%%.Z", "$$160%%:", "$$160.0%%.Z" 
        ]

    print("------ true test ---------")
    for item in t_test:
        ss = is_digit_inside(item)
        if ss:
            print("<< OK")
        else:
            print("wrong")

    print("------ false test ---------")
    for item in f_test:
        ss = is_digit_inside(item)
        if ss:
            print("wrong")
        else:
            print(" is OK")

#print(is_digit_inside("i5-13500"))
#test()

#nltk-version
def word_tokenize():
    s = "John's mom went there, but he wasn't there'. So' she said: 'Where are viix.co. !!' 'A a'"
    #s = re.findall("(\w[\w'\.]*\w|\w)", s)
    s = re.findall("(\w[\w'\.]*\w|\w|[\'%:!;,\$\?\.])", s) # nltk-version
    if s:
        print(s)
    return
##########################################
