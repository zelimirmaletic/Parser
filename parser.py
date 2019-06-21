import sys
import supportLibrary
import re

# Create variables for file names defined in command line arguments
inputFileName = "input.txt"  # sys.argv[1]
configFileName = "config.bnf" # sys.argv[2]

# READ INPUT FILE
inputFileLines = []
with open(inputFileName) as inputFileObject:
    for line in inputFileObject:
        inputFileLines.append(line.rstrip())

# READ CONFIG FILE

configFileLines = []
with open(configFileName) as configFileObject:
    for line in configFileObject:
        configFileLines.append(line.rstrip())
#reverse list because of bootom-up parsing
configFileLines.reverse()
for line in configFileLines:
    print(line)
# ANALYZE CONFIG FILE

class Token():
    isTerminal = False
    configFileLine = ""
    tokenName = ""
    subTokens = []
    regularExpression = ''
    regexTokenName = "(?!<)\w+(?=>)"
    regexNonTerminalTokenExpression = "(?!'| )\w+(?='|)"

    def __init__(self, configFileLine):
        self.configFileLine = configFileLine

    def decompozeConfigLine(self):
        countBrackets = self.configFileLine.count('<');
        if countBrackets == 1:
            # This token is terminal therefore has no subtokens
            #using RegEx to extract name of the token in BNF
            matchObject=re.search(self.regexTokenName, self.configFileLine)
            self.tokenName = matchObject.group(0)
            # Here the lists subToken and terminalToken stay empty
            #now we have to form a list of nonterminal token expressions
            matchObject = re.findall(self.regexNonTerminalTokenExpression, self.configFileLine )
            #now we have to form regex for this token
            numberOfMatches = len(matchObject);
            for index,match in enumerate(matchObject):
            	self.regularExpression += match
            	if index!=numberOfMatches-1:
            		self.regularExpression+="|"
            



token1 = Token("<ANIMAL> := 'CAT' | 'DOG' | 'PARROT' | 'LAMA' ")
token1.decompozeConfigLine()
print(token1.tokenName)
print(token1.regularExpression)
