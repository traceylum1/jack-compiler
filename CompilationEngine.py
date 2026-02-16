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
        self.xmlLines.append('<subroutineDec>')

        # Get function/method/constructor keyword
        token = self.tokenizer.keyWord()
        match token:
            case 'function' | 'method':
                self.xmlLines.append('<keyword> ' + token + ' </keyword>')

                # Get return type keyword
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()

                    if self.tokenizer.tokenType() == 'KEYWORD':
                        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
                    else:
                        raise RuntimeError('Keyword expected')
                else:
                    raise RuntimeError('Unexpected end of input')

                # Get subroutine identifier
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                    else:
                        raise RuntimeError('Identifier expected')
                else:
                    raise RuntimeError('Unexpected end of input')
        
            case 'constructor':
                self.xmlLines.append('<keyword> ' + token + ' </keyword>')

                # Get constructor identifier
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                    else:
                        raise RuntimeError('Identifier expected')
                else:
                    raise RuntimeError('Unexpected end of input')

                # Get new keyword
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()

                    if self.tokenizer.tokenType() == 'KEYWORD':
                        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
                    else:
                        raise RuntimeError('Keyword expected')
                else:
                    raise RuntimeError('Unexpected end of input')


        # Get opening parenthesis for parameter list
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('( expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get parameter list or closing parenthesis
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            elif self.tokenizer.tokenType() == 'KEYWORD':
                self.compileParameterList()
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get subroutine opening curly bracket
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.compileSubroutineBody()
            else:
                raise RuntimeError('{ expected')
        else:
            raise RuntimeError('Unexpected end of input')

        self.xmlLines.append('</subroutineDec>')

    """
    compileParameterList: Compiles a (possible empty) parameter list. Does not handle the enclosing "()"
    """
    def compileParameterList(self):
        self.xmlLines.append('<parameterList>')

        # Get parameter type keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get parameter identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
            else:
                raise RuntimeError('Identifier expected')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get additional parameter identifier(s)
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            # Get parameter type and identifier together
            if self.tokenizer.tokenType() == 'KEYWORD':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                    else:
                        raise RuntimeError('Identifier expected')
                else:
                    raise RuntimeError('Unexpected end of input')
            
            # Get comma or end of parameter list
            elif self.tokenizer.tokenType() == 'SYMBOL':
                token = self.tokenizer.symbol()
                # End class var dec if semicolon reached
                if token == ')':
                    break
                elif token == ',':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            else:
                raise RuntimeError('Keyword, identifier or symbol expected')


        self.xmlLines.append('</parameterList>')

    """
    compileSubroutineBody: Compiles a subroutine's body
    """
    def compileSubroutineBody(self):
        self.xmlLines.append('<subroutineBody>')

        # Get opening curly bracket
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')

        self.compileStatements()
        
        # Get closing curly bracket
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        
        self.xmlLines.append('</subroutineBody>')

    """
    compileStatements: Compiles a sequence of statements. Does not handle the enclosing "{}"
    """
    def compileStatements(self):
        self.xmlLines.append('<statements>')

        if self.tokenizer.tokenType() == 'KEYWORD':
            token = self.tokenizer.keyWord()
            match token:
                case 'var':
                    self.compileVarDec()
                case 'let':
                    self.compileLet()
                case 'if':
                    self.compileIf()
                case 'while':
                    self.compileWhile()
                case 'do':
                    self.compileDo()
                case 'return':
                    self.compileReturn()

        self.xmlLines.append('</statements>')


    """
    compileVarDec: Compiles a var declaration
    """
    def compileVarDec(self):
        self.xmlLines.append('<varDec>')
        
        # Get var keyword
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
                self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')

            elif self.tokenizer.tokenType() == 'SYMBOL':
                token = self.tokenizer.symbol()
                # End var dec if semicolon reached
                if token == ';':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                    break
                elif token == ',':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            else:
                raise RuntimeError('Identifier or symbol expected')
        
        self.xmlLines.append('</varDec>')

    """
    compileLet: Compiles a let statement
    """
    def compileLet(self):
        self.xmlLines.append('<letStatement>')


        self.xmlLines.append('</letStatement>')

    """
    compileIf: Compiles an if statement, possibly with a trailing else clause
    """
    def compileIf(self):
        self.xmlLines.append('<ifStatement>')

        
        self.xmlLines.append('</ifStatement>')


    """
    compileWhile: Compiles a while statement
    """
    def compileWhile(self):
        self.xmlLines.append('<whileStatement>')

        
        self.xmlLines.append('</whileStatement>')

    """
    compileDo: Compiles a do statement
    """
    def compileDo(self):
        self.xmlLines.append('<doStatement>')

        
        self.xmlLines.append('</doStatement>')

    """
    compileReturn: Compiles a return statement
    """
    def compileReturn(self):
        self.xmlLines.append('<returnStatement>')

        
        self.xmlLines.append('</returnStatement>')

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