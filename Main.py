from Parser import Parser
import sys

# Create variables for file names defined in command line arguments
inputFileName = sys.argv[1]
configFileName = sys.argv[2]


myParser = Parser(inputFileName, configFileName)
myParser.loadConfigFile()
myParser.loadParsingList()
myParser.formTerminalRegexes()
