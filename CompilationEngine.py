from JackTokenizer import JackTokenizer

"""
CompilationEngine class
    - Takes the input from the tokenizer
    - Compiles the non-terminal tokens
    - Outputs to .xml file
"""

class CompilationEngine:
    """
    Constructor: Gets input from tokenizer and outputs xml
    """
    def __init__(self, tokenizer:  JackTokenizer, filePath: str):
        self.xmlLines = []

        self.tokenizer = tokenizer

        if len(tokenizer.lines) == 0:
            print('File empty. Nothing to compile')
            return
        
        # while tokenizer.hasMoreTokens():
        #     try:
        #         tokenizer.advance()
        #         tokenType = tokenizer.tokenType()

        #         token = None
        #         match tokenType:
        #             case 'KEYWORD':
        #                 token = tokenizer.keyWord()
        #             case 'SYMBOL':
        #                 token = tokenizer.symbol()
        #             case 'IDENTIFIER':
        #                 token = tokenizer.identifier()
        #             case 'INT_CONST':
        #                 token = tokenizer.intVal()
        #             case 'STRING_CONST':
        #                 token = tokenizer.stringVal()
                        
        #     except RuntimeError as error:
        #         print(error)
        #         return
        
        self.compileClass()

        xmlOutput = '\n'.join(self.xmlLines)

        xmlFilePath = filePath.split('.')[0] + '.xml'
        
        with open(xmlFilePath, 'w') as file:
            print('Writing to new file: ', xmlFilePath)
            file.write(xmlOutput)
    
    """
    compileClass: Compiles a complete class (called immediately after constructor)
    """
    def compileClass(self):
        self.xmlLines.append('<tokens>')

        # Get class keyword
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
            else:
                raise RuntimeError('Keyword expected')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get class identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
            else:
                raise RuntimeError('Identifier expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get opening curly bracket for class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('{ expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Contents of class -- static or field declarations, and then subroutines
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                token = self.tokenizer.keyWord()
                match token:
                    case 'static':
                        self.compileClassVarDec()
                    case 'field':
                        self.compileClassVarDec()
                    case 'constructor':
                        self.compileSubroutineDec()
                    case 'function':
                        self.compileSubroutineDec()
                    case 'method':
                        self.compileSubroutineDec()
            print(self.tokenizer.currToken)


        self.xmlLines.append('</tokens>')
        pass

    """
    compileClassVarDec: Compiles a static variable declaration, or a field declaration
    """
    def compileClassVarDec(self):
        self.xmlLines.append('<classVarDec>')
        # Get field/static keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
        
        # Get primitive type keyword
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'KEYWORD':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
            else:
                raise RuntimeError('Keyword expected')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get variable identifier(s)
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'IDENTIFIER':
                print(self.tokenizer.currToken, 'should be identifier')
                self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')

            elif self.tokenizer.tokenType() == 'SYMBOL':
                token = self.tokenizer.symbol()
                # End class var dec if semicolon reached
                if token == ';':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                    break
                elif token == ',':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            else:
                raise RuntimeError('Identifier or symbol expected')
            
        self.xmlLines.append('</classVarDec>')
        
    """
    compileSubroutineDec: Compiles a complete method, function, or constructor
    """
    def compileSubroutineDec(self):
        pass

    """
    compileParameterList: Compiles a (possible empty) parameter list. Does not handle the enclosing "()"
    """
    def compileParameterList(self):
        pass

    """
    compileSubroutineBody: Compiles a subroutine's body
    """
    def compileSubroutineBody(self):
        pass

    """
    compileVarDec: Compiles a var declaration
    """
    def compileVarDec(self):
        pass

    """
    compileStatements: Compiles a sequence of statements. Does not handle the enclosing "{}"
    """
    def compileStatements(self):
        pass

    """
    compileLet: Compiles a let statement
    """
    def compileLet(self):
        pass

    """
    compileIf: Compiles an if statement, possibly with a trailing else clause
    """
    def compileIf(self):
        pass

    """
    compileWhile: Compiles a while statement
    """
    def compileWhile(self):
        pass

    """
    compileDo: Compiles a do statement
    """
    def compileDo(self):
        pass

    """
    compileReturn: Compiles a return statement
    """
    def compileReturn(self):
        pass

    """
    compileExpression: Compiles an expression
    """
    def compileExpression(self):
        pass

    """
    compileTerm: Compiles a term
        - If the current token is an identifier, the routine must distringuish between a variable,
        an array entry, or a subroutine call.
        - A single look-ahead token, which may be one of "[", "(", or "." suffices to distinguish between the possibilities.
        - Any other token is not part of this term and should not be advanced over
    """
    def compileTerm(self):
        pass

    """
    compileExpressionList: Compiles a (possibly empty) comma-separated list of expressions
    """
    def compileExpressionList(self):
        pass