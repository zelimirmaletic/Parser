import re
from CrawlerStatic import Crawler
from Token import Token
import time
import sys


#Scrape web site and form regex for veliki_grad token
#myCrawler = Crawler()
#myCrawler.scrapeWebLink()
#myCrawler.formRegex()
#After this line we have formed regular expression for matching big cities
#Dictionary for predefined expressions from the given table
tableRegex = {
    'mejl_adresa' : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'broj_telefona' : "(\+387)*(\d){2,3}(\/|-)*(\d){3}(\/|-)*(\d){3}",
    'web_link' : "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    'brojevna_konstanta' : "(\d)*(\.\d*)*",
    'veliki_grad' : 'Barcelona|Madrid|Cacai'#myCrawler.regex,
}

specialRegexChars = ['(' , ')' , '.' , '[' , ']' , '*' , '+', '\\' , '/' ]


def checkSpecialCharacter( character ):
    for item in specialRegexChars:
        if(item == character):
            return True
    return False

def formRegexForWizardString(string):
    regex = ''
    for char in string:
        if char == ' ':
            regex += '\s'
        elif checkSpecialCharacter(char) == True:
            regex += '\\'
            regex += char
        elif char != '"':
            regex += char
    return regex



class Parser():
    inputFileName = ''
    configFileName = ''
    inputFileLines = []
    configFileLines = []
    parsingList = []
    tableParsingList = []

    def __init__(self, inputFileName, configFileName):
        self.inputFileName = inputFileName
        self.configFileName = configFileName

    def loadInputFile(self):
        try:
            with open(self.inputFileName) as inputFileObject:
                for line in inputFileObject:
                    self.inputFileLines.append(line.rstrip())
                print('parser---> input file loaded')
                time.sleep(1)
        except FileNotFoundError:
            print('parser---> ERROR: Problem with fetching input.txt')
            sys.exit()

    def loadConfigFile(self):
        try:
            with open(self.configFileName) as configFileObject:
                for line in configFileObject:
                    self.configFileLines.append(line.rstrip())
                #reverse list because we want to start from terminal tokens
                self.configFileLines.reverse()
                print('parser---> config file loaded')
                time.sleep(1)
        except FileNotFoundError:
            print('parser---> ERROR: Problem with fetching config.bnf ')
            sys.exit()

    def printAllTokens(self):
        for item in self.parsingList:
            item.printToken()
        #for item in self.tableParsingList:
        #    item.printToken()


    def loadParsingList(self):
        for line in self.configFileLines:
            if line!= '':
                self.parsingList.append(Token(line))
        #for item in self.parsingList:
            #print(item.configFileLine)

    def formTableParsingList(self):
        for name,regex in tableRegex.items():
            line = '<'+name+'>:=regex('+regex+')'
            self.tableParsingList.append(Token(line))
        for item in self.tableParsingList:
            item.formToken()


    def formTerminalRegexes(self):
        for item in self.parsingList:
            item.formToken()
        print('parser---> forming regexes for terminal tokens')
        time.sleep(1)
        self.formTableParsingList()

    def formNonTerminalRegexes(self):
        print('parser---> forming regexes for non-terminal tokens')
        for item in self.parsingList:
            i = 0
            wizardStringCounter = 0
            if item.isTerminal == False:
                item.regularExpression += '('
                for c in item.regexWizard:
                    if c == 't':
                        searchKey = item.subTokens[i]
                        errorFlag = 0
                        for temp in self.parsingList:
                            errorFlag+=1
                            if(temp.tokenName == searchKey):
                                item.regularExpression += temp.regularExpression
                                break
                        if errorFlag == len(self.parsingList):
                            print('parser---> ERROR: There is an error in given BNF form. \n\t\t  Missing some terminal token definitions!')
                            print('\t\t  Terminating program execution...')
                            sys.exit()
                        i+=1
                    #elif c == 's':
                        #item.regularExpression += '\s'
                    elif c == 'l':
                        item.regularExpression += '|'
                    #elif c == 'b':
                    #    item.regularExpression += ')('
                    elif c == 'w':
                        item.regularExpression += '('
                        formedRegex = formRegexForWizardString(item.wizardStrings[wizardStringCounter])
                        item.regularExpression += formedRegex
                        item.regularExpression += ')'
                        wizardStringCounter += 1
                item.regularExpression += ')'
