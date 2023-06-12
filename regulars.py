import re

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

ss = "$.225% |"
ss = "$,225% |"
ss = "$:225% |"
ss = "55   "
ss = re.sub(r'[$]?[-+]?[\d]*[.,\:]?[\d]+[%\"\']?', "", ss)
print("-->>", ss)

ss = "$.225% |"
#ss = "05%. |"
ss = "225 "
ss = re.search(r"\A([$]?[-+]?[\d]*[.,\:]?[\d]+[ ,:%\"\']?)", ss)
if ss:
    print(ss.group())
else:
    print("wrong")
