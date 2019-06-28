import re


string  = '<a>:=      <b> <c> <d>|<e> <g>'


def formRegexWizard(string):
    wizard = ''
    i = 0
    for c in string:
        if c == '<':
            i+=1
            if i>=2:
                wizard += 't'
        elif c == ' ':
            if i>=2:
                wizard += 's'
        elif c == '|':
            wizard += 'l'
    print(wizard)


formRegexWizard(string)
