import re

# is digit wrapped by another symbols:
# re.search('(?<!\d)\d(?!\d)', str)

# real number:
# re.search('[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?', str)

def is_digit_inside(str):
    return re.search('(?<![A-Za-z0-9$])[-+$]*(?:\d+(?:\.\,\:\d*)?|\.\,\:\d+)(?![^\ ])', str)

    return re.search('(?<![A-Za-z.])[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?!\d\w)', str)
    return re.search('(?<!\d[A-Za-z])[-+$ ]?(?:\d+(?:\.\:\d*)?|\.\:\,\d+)[$%]*(?![A-Za-z\-])', str)

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

ss = "$.225% |"
#ss = "05%. |"
ss = "225 "
ss = "33333.33%% D"
ss = "3.33"

true_test = [ '33.33', '33.33%', '33.33%%', '33.33%% ', '33.33%D', '33.33%D', "3 D", "3%% D",  '33.33 D']
false_test = [ '3D', '3-D', '333D', '333DDD' ]

rgx = "\A([$]?[-+]?[\d]*[.,:]?[\d]+[%\"\' ]+)[^a-zA-Z-]?"

for item in true_test:
    break
    ss = re.search(rgx, item)
    if ss:
        print(ss.group())
    else:
        print("wrong")


for item in false_test:
    break
    ss = re.search(rgx, item)
    if ss:
        print(ss.group())
    else:
        print("wrong")

print("-----------")

ss = "22.22%D"

# should return true
t_test = [
    "160", "$$160", "-160,0 ", "-160.0 ", "-160:0 ", "160.0 "
    "A 160.0 Z", "A 1600 Z", "A 160,0 Z", "A 160:0 Z", "A 1600 Z", "A 160:0 Z", "-160,0", "-160.0", "-160:0", "160.0"
    "A $$160.0 Z", "A $$1600 Z", "A $$160,0 Z", "A $$160:0 Z", "A $$1600 Z", "A $$160:0 Z", "$$-160,0", "$$-160.0", "$$-160:0", "$$160.0" 
    ]

# should return false
f_test = [ 
    "A 160.0Z", "A1600 Z", "A160.0Z", "A 160:0Z", "A1600 Z", "A160:0Z", "A 160. Z", 
    "A160", "A160Z", "160-Z", "160Z", "160.Z", "160.", "160.Z", "160:", "160.0.Z" 
    
    "A $$160.0Z", "A$$1600 Z", "A$$160.0Z", "A $$160:0Z", "A$$1600 Z", "A$$160:0Z", "A $$160. Z", 
    "A$$160", "A$$160Z", "$$160-Z", "$$160Z", "$$160.Z", "$$160.", "$$160.Z", "$$160:", "$$160.0.Z" 
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
