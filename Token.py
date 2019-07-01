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
    regexWizard = ''
    wizardStrings = ''

    regexTokenName = "(?!<)\w+(?=>)"
    regexNonTerminalTokenExpression = "(?!'| )\w+(?='|)"

    def __init__(self, configFileLine):
        self.configFileLine = configFileLine

    #Functions that keeps track of spaces and | in nonterminal node definition
    def formRegexWizard(self):
        i = 0
        qoutesCounter = 0
        for index,c in enumerate(self.configFileLine):
            if c == '<':
                i+=1
                if i>=2:
                    self.regexWizard += 't'
            #elif c == ' ':
                #if i>=2:
                    #self.regexWizard += 's'
            elif c == '|':
                self.regexWizard += 'l'
            elif c=='"':
                qoutesCounter+=1
                if qoutesCounter % 2 != 0:
                    self.regexWizard += 'w'
            #elif index!=len(self.configFileLine)-1 and c == '>' and self.configFileLine[index+1] == '<':
            #        self.regexWizard += 'b'

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
                matchObject = re.search("(?<=\()(.+(\))*)*(?=\))", self.configFileLine)
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
                self.regularExpression += '('
                for index,match in enumerate(matchObject):
                    self.regularExpression += match
                    if index!=numberOfMatches-1:
                        self.regularExpression+="|"
                self.regularExpression += ')'

        #If not terminal then it's a nonterminal, this means that it has some subtokens
        else:
            #We have to form list of subtokens inside this token
            matches = re.findall(self.regexTokenName,self.configFileLine)
            #we don't need the name of first token, that one is not in definition
            del matches[0]
            #copy list
            self.subTokens = matches[:]
            wizardStringRegex = '\"[^><\"]+(?=\")'
            matches = re.findall(wizardStringRegex,self.configFileLine)
            self.wizardStrings = matches[:]
            #now we create a pattern that will help us later to make regex for nonterminal tokens
            self.formRegexWizard()

            #Wen cannot form regular expressions for nonterminals at this point.
            #There will be another class that will have method to form these RegExes
            #THIS PARSER DOES NOT SUPPORT RECCURSIVE DEFINITION
            #So we have to check that:
            for item in self.subTokens:
                if self.tokenName == item:
                    print('parser---> EBNF ERROR LINE:'+self.configFileLine)
                    print('\t\tReccursive definition found in config file.')
                    print('\t\tThis parser DOES NOT support reccursive de-')
                    print('\t\tfinitions, therefore is unable to continue ')
                    print('\t\tparsing. Terminating program execution...  ')
                    sys.exit()

    def printToken(self):
        print('****************Token info************************')
        print('Config file line: ' + self.configFileLine)
        print('Token name: ' + self.tokenName)
        print('Is this terminal token? : ' + str(self.isTerminal))
        print('Is this table expression? :' + str(self.isTableExpression))
        print('Subtokens: ')
        print(self.subTokens)
        print('Regex Wizard: ' + self.regexWizard)
        print('wizardStrings: ')
        print(self.wizardStrings)
        print('Regular expression: ' + self.regularExpression)
