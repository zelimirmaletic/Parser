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
    #'veliki_grad' : myCrawler.regex,
}

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


    def loadParsingList(self):
        for line in self.configFileLines:
            self.parsingList.append(Token(line))
        #for item in self.parsingList:
            #print(item.configFileLine)

    def formTerminalRegexes(self):
        for item in self.parsingList:
            item.formToken()
        print('parser---> forming regexes for terminal tokens')
        time.sleep(1)
