import re
from Token import Token



class Parser():
    inputFileName = ''
    configFileName = ''
    inputFileLines = []
    configFileLines = []
    parsingList = []

    def __init__(self, inputFileName, configFileName):
        self.inputFileName = inputFileName
        self.configFileName = configFileName

    def loadInputFile(self):
        with open(self.inputFileName) as inputFileObject:
            for line in inputFileObject:
                self.inputFileLines.append(line.rstrip())
    def loadConfigFile(self):
        with open(self.configFileName) as configFileObject:
            for line in configFileObject:
                self.configFileLines.append(line.rstrip())
        #reverse list because we want to start from terminal tokens
        self.configFileLines.reverse()

    def loadParsingList(self):
        for line in self.configFileLines:
            self.parsingList.append(Token(line))
        #for item in self.parsingList:
            #print(item.configFileLine)

    def formTerminalRegexes(self):
        for item in self.parsingList:
            print(item.configFileLine)
            item.formToken()
            print(item.tokenName)
            print(item.subTokens)
            print('Regex--->  ' + item.regularExpression)
            print('-----------------------')
