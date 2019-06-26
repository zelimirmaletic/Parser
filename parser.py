import sys
import supportLibrary
import re
from Token import Token

# Create variables for file names defined in command line arguments
inputFileName = "input.txt"  # sys.argv[1]
configFileName = "config.bnf" # sys.argv[2]

# READ INPUT FILE-----------------------------
inputFileLines = []
with open(inputFileName) as inputFileObject:
    for line in inputFileObject:
        inputFileLines.append(line.rstrip())
#---------------------------------------------

# READ CONFIG FILE----------------------------
configFileLines = []
with open(configFileName) as configFileObject:
    for line in configFileObject:
        configFileLines.append(line.rstrip())
#reverse list because of bootom-up parsing
configFileLines.reverse()
# for line in configFileLines:
    # print(line)
#----------------------------------------------



print('-----------------------TERMINAL------------------------------')

token1 = Token('<noun> ::= MAN | DOG')

token1.decomposeConfigLine()
print(token1.tokenName)
print(token1.regularExpression)


print('-----------------------NONTERMINAL------------------------------')

token2 = Token('<a> ::= hello <SUBTOKEN1> hello <SUBTOKEN2>')
token2.decomposeConfigLine()
print(token2.tokenName)
print(token2.subTokens)
print('REGEX---> '+token2.regularExpression)
