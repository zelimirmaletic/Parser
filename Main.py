from Parser import Parser
import sys
import  time


try:
    # Create variables for file names defined in command line arguments
    inputFileName = sys.argv[1]
    configFileName = sys.argv[2]
except IndexError:
    print('There is a problem with comand line argumnets!')
    sys.exit()
print('*************************************************************************')
print('*                    EBNF  P A R S E R                                  *')
print('*************************************************************************')

myParser = Parser(inputFileName, configFileName)
myParser.loadInputFile()
myParser.loadConfigFile()
print('parser---> Analyzing EBNF...')
time.sleep(1)
myParser.loadParsingList()
myParser.formTerminalRegexes()
print('parser---> \n\t   Crawler---> Scraping web link...')
time.sleep(5)
print('parser---> \n\t   Crawler---> Forming regular expressions from fetched cities...')
myParser.formNonTerminalRegexes()
#myParser.printAllTokens()
print('parser---> EBNF sucessfully analyzed.')
print('\n------------------------PARSING----------------------------------------\n')
myParser.parse()
print('\n----------------------------DONE!--------------------------------------\n')
print('*************************************************************************')
print('*                   Zelimir Maletic 2019                                *')
print('*************************************************************************')
