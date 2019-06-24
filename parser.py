import sys
import supportLibrary
import re

# Create variables for file names defined in command line arguments
inputFileName = "input.txt"  # sys.argv[1]
configFileName = "config.bnf" # sys.argv[2]

# READ INPUT FILE-----------------------------
inputFileLines = []
with open(inputFileName) as inputFileObject:
    for line in inputFileObject:
        inputFileLines.append(line.rstrip())
        print(dfsdfsdfd)
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


# ANALYZE CONFIG FILE--------------------------------------------------------------------------------

class Token():
    # Token data
    isTerminal = False
    configFileLine = ""
    tokenName = ""
    subTokens = []
    regularExpression = ''

    regexTokenName = "(?!<)\w+(?=>)"
    regexNonTerminalTokenExpression = "(?!'| )\w+(?='|)"
    tableRegex = {
    'mejl_adresa' : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'broj_telefona' : "(\+387)*(\d){2,3}(\/|-)*(\d){3}(\/|-)*(\d){3}",
    'web_link' : "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    'brojevna_konstanta' : "(\d)*(\.\d*)*",
    'veliki_grad' =
    }

    def __init__(self, configFileLine):
        self.configFileLine = configFileLine

    def decomposeConfigLine(self):
        # Determine token name
        matchObject = re.search(self.regexTokenName, self.configFileLine)
        self.tokenName = matchObject.group(0)
        #If have only one pair of <> then this token is a terminal one
        countBrackets = self.configFileLine.count('<')
        if countBrackets == 1:
            self.isTerminal = True
            # This token is terminal therefore has no subtokens
            # Here the lists subToken stays empty

            # We have to check wether a token is of a special form AKA one from the given table

            # REGEX(.....)
            matchObject=re.search("regex\(", self.configFileLine)
            if matchObject!= None:
                #Now we have to form regular expression of this special kind of token
                matchObject = re.search("(?<=\().+?(?=\))", self.configFileLine)
                self.regularExpression = matchObject.group(0)

            else:
                #now we have to form a list of nonterminal token expressions
                matchObject = re.findall(self.regexNonTerminalTokenExpression, self.configFileLine )
                del matchObject[0]
                #now we have to form regex for this token
                numberOfMatches = len(matchObject);
                for index,match in enumerate(matchObject):
                    self.regularExpression += match
                    if index!=numberOfMatches-1:
                        self.regularExpression+="|"

        #If not terminal then it's a terminal, this means that it has some subtokens
        else:
            #We have to form list of subtokens inside this token
            matchObject = re.findall(self.regexTokenName,self.configFileLine)
            for match in matchObject:
                self.subTokens.append(match)
            del self.subTokens[0] #we dont need the name of first token
            #Wen cannot form regular expressions for nonterminals at this point.
            #There will be another class that will have method to form these RegExes





#------------------------------------------------------------------------------------------------------

print('-----------------------TERMINAL------------------------------')

token1 = Token('<noun> ::= MAN | DOG')

token1.decomposeConfigLine()
print(token1.tokenName)
print(token1.regularExpression)


print('-----------------------NONTERMINAL------------------------------')

token2 = Token('<a> ::= regex(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')
token2.decomposeConfigLine()
print(token2.tokenName)
print(token2.subTokens)
print('REGEX---> '+token2.regularExpression)
