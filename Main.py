from Parser import Parser
import sys
import  time

# Create variables for file names defined in command line arguments
inputFileName = sys.argv[1]
configFileName = sys.argv[2]

print('******************** EBNF PARSER ********************')
myParser = Parser(inputFileName, configFileName)
myParser.loadInputFile()
myParser.loadConfigFile()
print('parser---> scanning EBNF')
time.sleep(1)
myParser.loadParsingList()
myParser.formTerminalRegexes()
print('***************** Zelimir Maletic *******************')
