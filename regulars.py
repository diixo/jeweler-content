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

ss = "$+.225% |"
ss = "$,225% |"
ss = "$:225% |"
ss = "$+55   "
ss = re.sub(r'[$]?[-+]?[\d]*[.,\:]?[\d]+[%\"\']?', "", ss)
print("-->>", ss)

ss = "$.225% |"
#ss = "05%. |"
ss = "225 "
#ss = "3-D"
ss = re.search(r"\A([$]?[-+]?[\d]*[.,:]?[\d]+[ ,:%\"\']?)[^a-zA-Z\-:]+", ss)
if ss:
    print(ss.group())
else:
    print("wrong")

print("------------------------------")
ss = "333.3D"

ss = re.search(r"\A(?:[$]?[-+]?[\d]*[.,:]?[\d]+[a-zA-Z]+)+", ss)
if ss:
    print(ss.group())
else:
    print("wrong")