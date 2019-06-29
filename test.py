import re

string = '<a>:= <b> abc <c>'
regex = '\w+(?=\s*|\||<)?'
matches = re.findall(regex,string)
print(matches)
