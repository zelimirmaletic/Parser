import re
import sys



class Token():
    # Token data
    isTerminal = False
    isTableExpression = False
    configFileLine = ""
    tokenName = ""
    subTokens = []
    regularExpression = ''

    regexTokenName = "(?!<)\w+(?=>)"
    regexNonTerminalTokenExpression = "(?!'| )\w+(?='|)"

    def __init__(self, configFileLine):
        self.configFileLine = configFileLine

    def formToken(self):
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
            matchObject1=re.search("regex\(", self.configFileLine)
            matchObject2=re.search("standardni_izraz", self.configFileLine)

            if matchObject1!= None:
                #Now we have to form regular expression of this special kind of token
                matchObject = re.search("(?<=\().+?(?=\))", self.configFileLine)
                self.regularExpression = matchObject.group(0)
            elif matchObject2 != None:
                #This one is of special kind, and class parser will resolve that regex
                self.isTableExpression = True
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

        #If not terminal then it's a nonterminal, this means that it has some subtokens
        else:
            #We have to form list of subtokens inside this token
            matches = re.findall(self.regexTokenName,self.configFileLine)
            del matches[0]
            self.subTokens = matches[:]
            #we don't need the name of first token
            #Wen cannot form regular expressions for nonterminals at this point.
            #There will be another class that will have method to form these RegExes
            #THIS PARSER DOES NOT SUPPORT RECCURSIVE DEFINITION
            #So we have to check that:
            for item in self.subTokens:
                if self.tokenName == item:
                    print('parser---> ERROR:')
                    print('\t\tReccursive definition found in config file.')
                    print('\t\tThis parser DOES NOT support reccursive de-')
                    print('\t\tfinitions, therefore is unable to continue ')
                    print('\t\tparsing. Terminating program execution...  ')
                    sys.exit()
