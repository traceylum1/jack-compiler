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
        self.lines = [line for line in self.lines if (line != '' and line[0:3] != '/**' and line[0] != '*' and line[0:2] != '*/')]

        print(self.lines)

        self.prevToken = None
        self.currToken = None
        
        self.currIdx = 0
        self.currLineIdx = 0

        
        self.keywords = [
            'class',
            'new',
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
        return self.currIdx < len(self.lines) and self.currLineIdx < len(self.lines[self.currIdx])


    """
    advance: Gets the next token from the input and makes it the current token
        - Only called if hasMoreTokens returns true
        - Initially no token
        - Use two pointers to parse token
    """
    def advance(self):
        self.prevToken = self.currToken
        start = end = self.currLineIdx
        line = self.lines[self.currIdx]

        # If curr char is symbol (single char), incremend end by one
        if line[end] in self.symbols:
            end += 1

        # Else iterate through full token until space, symbol, or end of line reached
        else:
            while end < len(line) and line[end] != ' ' and line[end] not in self.symbols:
                end += 1

        # Update current token
        self.currToken = line[start:end]

        # Skip white spaces
        while end < len(line) and line[end] == ' ':
            end += 1

        # If finished with current line, move to next one
        if end == len(line):
            end = 0
            self.currIdx += 1

        self.currLineIdx = end

        
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
        elif (prevToken == '=' or prevToken == '[' or prevToken == '-') and currToken.isdigit():
            if int(currToken) > 32767:
                raise RuntimeError('Error: Integer value is greater than 32767')
            return 'INT_CONST'
        
        # How to differeniate between identifier and str const, besides excluding starting with digit?
        # Do we need to know the prev token? ie, whether prev is '=' or keyword
        elif regex.match(currToken) and not currToken[0].isdigit():
            return 'IDENTIFIER'
        elif currToken[0] == "'" or currToken[0] == '"':
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