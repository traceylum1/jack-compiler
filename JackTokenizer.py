"""
JackTokenizer class
    - Handles the parsing of a single .vm file
    - Goes through the input and determines the token type and value
    - Ignores all white space and comments
"""


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

        self.currToken = None
        self.currIdx = 0

        self.currLine = self.lines[self.currIdx]
        self.currLineIdx = 0


        self.tokenTypes = [
            'KEYWORD', 
            'SYMBOL', 
            'IDENTIFIER',
            'INT_CONST',
            'STRING_CONST',
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
        # If curr char is symbol, set as curr token and increment idx
        if self.currLine[self.currLineIdx] in self.symbols:
            self.currToken = self.currLine[self.currLineIdx]
            self.currLineIdx += 1
            return

        line = self.currLine
        lIdx = rIdx = self.currLineIdx

        while line[lIdx] != ' ' and line[lIdx] not in self.symbols:
            lIdx += 1
        
        self.currToken = line[lIdx:rIdx]

        while line[lIdx] == ' ':
            lIdx += 1

        self.currLineIdx = lIdx

    """
    tokenType: Returns the type of the current token, as a constant
    """
    def tokenType(self):
        pass


    """
    keyWord: Returns the keyword which is the current token
        - Only called if tokenType is KEYWORD
    """
    def keyWord(self):
        pass


    """
    symbol: Returns the character which is the current token
        - Only called if tokenType is SYMBOL
    """
    def symbol(self):
        pass


    """
    identifier: Returns the string which is the current token
        - Only called if tokenType is IDENTIFIER
    """
    def identifier(self):
        pass


    """
    intVal: Returns the integer value of the current token
        - Only called if tokenType is INT_CONST
    """
    def intVal(self):
        pass


    """
    symbol: Returns the string value of the current token
        - Only called if tokenType is STRING_CONST
    """
    def stringVal(self):
        pass