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
    'veliki_grad' : 'Barcelona|Paris|London',#myCrawler.regex,
    'mejl_adresa' : '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    'broj_telefona' : "(\+387)*(\d){2,3}(\/|-)*(\d){3}(\/|-)*(\d){3}",
    'web_link' : "https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
    'brojevna_konstanta' : "(\d)*(\.\d*)*",
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
                print('parser---> Input file loaded')
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
                print('parser---> Config file loaded')
                time.sleep(1)
        except FileNotFoundError:
            print('parser---> ERROR: Problem with fetching config.bnf ')
            sys.exit()

    def printAllTokens(self):
        for item in self.parsingList:
            item.printToken()

    def loadParsingList(self):
        for line in self.configFileLines:
            if line!= '':
                self.parsingList.append(Token(line))

    def formTableParsingList(self):
        for name,regex in tableRegex.items():
            line = '<' + name + '>:=regex(('+ regex + '))'
            self.tableParsingList.append(Token(line))
        for item in self.tableParsingList:
            item.formToken()

    def formTerminalRegexes(self):
        print('parser---> Forming regexes for given table definitions')
        self.formTableParsingList()
        time.sleep(0.5)

        for item in self.parsingList:
            item.formToken()
            if item.isTableExpression == True:
                for index,token in enumerate(self.tableParsingList):
                    item.regularExpression += token.regularExpression
                    if index != len(self.tableParsingList)-1:
                        item.regularExpression += '|'
        print('parser---> Forming regexes for terminal tokens')
        time.sleep(0.5)

    def formNonTerminalRegexes(self):
        print('parser---> Forming regexes for non-terminal tokens')
        time.sleep(0.5)
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
                            print('parser---> BNF ERROR LINE:' + item.configFileLine)
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




    def parse(self):
        #first we have to open(crete) XML File
        with open("output.xml", 'w') as outputStream:
            #Define recursive functoin for generating parse tree
            def diveToBottom(self,tokenName, inputLine):
                for token in self.parsingList:
                    if token.tokenName==tokenName and token.isTerminal:
                        #This part below is for writing logic
                        match = re.search(token.regularExpression,inputLine)
                        if match!= None:
                            outputStream.write('\n')
                            outputStream.write('<' + token.tokenName + '>')
                            #outputStream.write('\n')
                            outputStream.write(match.group())
                            #outputStream.write('\n')
                            outputStream.write('</' + token.tokenName + '>\n')
                            return
                    elif token.tokenName==tokenName and token.isTerminal == False:
                        for subtoken in token.subTokens:
                            for item in self.parsingList:
                                if subtoken == item.tokenName and item.isTerminal:
                                    diveToBottom(self, subtoken, inputLine)
                                elif subtoken == item.tokenName and item.isTerminal==False:
                                    outputStream.write('\n')
                                    outputStream.write('<' + subtoken + '>')
                                    diveToBottom(self, subtoken, inputLine)
                                    outputStream.write('</' + subtoken + '>\n')


            outputStream.write('<root>')
            #We have to search tokens from top to bottom, so we reverse parsingList
            self.parsingList.reverse()
            for index,inputLine in enumerate(self.inputFileLines):
                flagError = True
                for token in self.parsingList:
                    match = re.match(token.regularExpression, inputLine)
                    if match != None and inputLine == match.group():
                        flagError = False
                        #call recursive function for writing
                        if token.isTerminal == True:
                            diveToBottom(self, token.tokenName, inputLine)
                        else:
                            outputStream.write('\n')
                            outputStream.write('<' + token.tokenName + '>')
                            diveToBottom(self, token.tokenName, inputLine)
                            outputStream.write('</' + token.tokenName + '>\n')
                    break

                if(flagError==True):
                    print('parser---> PARSING ERROR: Invalid input on line ' + str(index+1))
                    print('           (The line: [' + inputLine + '] cannot be parsed with the given grammar.')


            outputStream.write('</root>')
