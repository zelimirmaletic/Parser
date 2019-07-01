import re

string = 'MAN'
regex = '^((THE|A)(\s)(MAN|DOG)|(MAN|DOG))$'
matches = re.match(regex,string)
print(matches)
