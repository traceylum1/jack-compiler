"""
JackTokenizer class
    - Handles the parsing of a single .vm file
    - Goes through the input and determines the token type and value
    - Ignores all white space and comments
"""

import re

class JackTokenizer:
    """
    Constructor: (input file/stream) => None
        - Opens the input file/stream and gets ready to parse it
    """
    def __init__(self, filePath):
        with open(filePath, 'r') as file:
            print('Opening file: ', filePath)
            # Read all lines, strip whitespace, and filter out inline comments
            self.lines = [
                line.split('//')[0].strip() for line in file.readlines()
            ]

        # Remove empty lines and comment lines
        self.lines = [line for line in self.lines if (line != '' or line[0:3] != '\**' or line[0] != '*' or line[0:2] != '*/')]

        self.prevToken = None
        self.currToken = None
        self.currIdx = 0

        self.currLine = self.lines[self.currIdx]
        self.currLineIdx = 0

        
        self.keywords = [
            'class',
            'constructor',
            'function',
            'method',
            'field',
            'static',
            'var',
            'int',
            'char',
            'boolean',
            'void',
            'true',
            'false',
            'null',
            'this',
            'let',
            'do',
            'if',
            'else',
            'while',
            'return'
        ]

        self.symbols = [
            '(',    # symbols
            ')',
            '{',
            '}',
            '[',
            ']',
            ';',
            '.',
            ',',
            '+',    # operators
            '-',
            '*',
            '/',
            '&',
            '|',
            '<',
            '>',
            '=',
            '~',     # unary operator
        ]

        self.intConstRange = [0, 32767]
        # String constant is a sequence of unicode characters not including double quote or newline
        # identifier is a sequence of letters, digits, and underscores, not starting with a digit


    """
    hasMoreTokens: Returns a boolean for whether there are more tokens to parse
    """
    def hasMoreTokens(self):
        return self.currLineIdx < len(self.currLine) or self.currIdx < len(self.lines)


    """
    advance: Gets the next token from the input and makes it the current token
        - Only called if hasMoreTokens returns true
        - Initially no token
    """
    def advance(self):
        self.prevToken = self.currToken

        # If curr char is symbol (single char), set as curr token and increment idx
        if self.currLine[self.currLineIdx] in self.symbols:
            self.currToken = self.currLine[self.currLineIdx]

        else:
            # Loop with two pointers until full token parsed
            line = self.currLine
            lIdx = rIdx = self.currLineIdx

            # Iterate through full token until space or symbol reached
            while line[rIdx] != ' ' and line[rIdx] not in self.symbols:
                rIdx += 1

            self.currToken = line[lIdx:rIdx]
            
        # Skip white spaces
        while line[rIdx] == ' ':
            rIdx += 1

        # Update current line index
        self.currLineIdx = rIdx

    """
    tokenType: Returns the type of the current token, as a constant
    """
    def tokenType(self):
        currToken = self.currToken
        prevToken = self.prevToken

        regex = re.compile('^[A-Za-z0-9_]+$')
        
        if currToken in self.keywords:
            return 'KEYWORD'
        elif currToken in self.symbols:
            return 'SYMBOL'
        # Do we need to ensure digit is within the appropriate range?
        # Only int const if it is after assignment op or an array index
        elif prevToken == '=' or prevToken == '[' and currToken.isdigit():
            return 'INT_CONST'
        
        # How to differeniate between identifier and str const, besides excluding starting with digit?
        # Do we need to know the prev token? ie, whether prev is '=' or keyword
        elif regex.match(currToken) and not currToken[0].isdigit() and prevToken in self.keywords:
            return 'IDENTIFIER'
        else:
            return 'STRING_CONST'


    """
    keyWord: Returns the keyword which is the current token
        - Only called if tokenType is KEYWORD
    """
    def keyWord(self):
        return self.currToken


    """
    symbol: Returns the character which is the current token
        - Only called if tokenType is SYMBOL
    """
    def symbol(self):
        return self.currToken


    """
    identifier: Returns the string which is the current token
        - Only called if tokenType is IDENTIFIER
    """
    def identifier(self):
        return self.currToken


    """
    intVal: Returns the integer value of the current token
        - Only called if tokenType is INT_CONST
    """
    def intVal(self):
        return self.currToken


    """
    symbol: Returns the string value of the current token
        - Only called if tokenType is STRING_CONST
    """
    def stringVal(self):
        return self.currToken