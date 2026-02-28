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
        self.xmlLines.append('<class>')

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

        if self.tokenizer.tokenType() == 'SYMBOL':
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        self.xmlLines.append('</class>')

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

                # Get new identifier
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()

                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                    else:
                        raise RuntimeError('Identifier expected')
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

        # Empty parameter list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.xmlLines.append('</parameterList>')
            return

        # Get parameter type keyword
        if self.tokenizer.tokenType() == 'KEYWORD':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
        else:
            raise RuntimeError('Keyword expected')

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

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                token = self.tokenizer.keyWord()
                match token:
                    case 'var':
                        self.compileVarDec()
                    case 'let' | 'if' | 'while' | 'do' | 'return':
                        self.compileStatements()
            else:
                raise RuntimeError('Keyword expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        
        # Get closing curly bracket
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        
        self.xmlLines.append('</subroutineBody>')

    """
    compileStatements: Compiles a sequence of statements. Does not handle the enclosing "{}"
    """
    def compileStatements(self):
        self.xmlLines.append('<statements>')
        print('######### calling compileStatements with current token: ', self.tokenizer.currToken)

        while self.tokenizer.tokenType() == 'KEYWORD':
            token = self.tokenizer.keyWord()
            match token:
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
                case _:
                    break
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                print('######### calling compileStatements end loop with current token: ', self.tokenizer.currToken)
            
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
                raise RuntimeError('Keyword expected in compileVarDec')
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
                raise RuntimeError('Identifier or symbol expected in compileVarDec')
        
        self.xmlLines.append('</varDec>')

    """
    compileLet: Compiles a let statement
    """
    def compileLet(self):
        print('######### calling compileLet')
        self.xmlLines.append('<letStatement>')
        
        # Get let keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get variable identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.xmlLines.append('<identifier> ' + self.tokenizer.symbol() + ' </identifier>')
            else:
                raise RuntimeError('Variable identifier expected in compileLet')
        else:
            raise RuntimeError('Unexpected end of input')
        
    
        # Get assignment symbol OR square bracket for array index
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'SYMBOL':
                token = self.tokenizer.symbol()
                match token:
                    case '=':
                        self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                    case '[':
                        self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileExpression()
                        # Get closing square bracket
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        
                # Compile expression after assignment operator
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                self.compileExpression()
                # Get semicolon
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('Symbol expected in compileLet')
        else:
            raise RuntimeError('Unexpected end of input')
        

        self.xmlLines.append('</letStatement>')

    """
    compileIf: Compiles an if statement, possibly with a trailing else clause
    """
    def compileIf(self):
        print('######### calling compileIf')
        self.xmlLines.append('<ifStatement>')

        # Get if keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get opening parenthesis for if conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('( expected in compileIf')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get expression for if conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileExpression()
        
        # Get closing parenthesis for if conditional
        if self.tokenizer.tokenType() == 'SYMBOL':
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        else:
            raise RuntimeError(') expected')

        # Get opening curly bracket for if conditional statements
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('{ expected in compileIf')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get statements for if conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileStatements()
        
        # Get closing curly bracket for if conditional statements
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')

        self.xmlLines.append('</ifStatement>')


    """
    compileWhile: Compiles a while statement
    """
    def compileWhile(self):
        print('######### calling compileWhile')
        self.xmlLines.append('<whileStatement>')

        # Get while keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get opening parenthesis for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('( expected in compileWhile')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get expression for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileExpression()
        
        # Get closing parenthesis for while conditional
        if self.tokenizer.tokenType() == 'SYMBOL':
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        else:
            raise RuntimeError(') expected in compileWhile')
        
        # Get statements for while conditional
        self.compileStatements()

        # Get closing curly bracket for while statements
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        
        self.xmlLines.append('</whileStatement>')

    """
    compileDo: Compiles a do statement
    """
    def compileDo(self):
        self.xmlLines.append('<doStatement>')

        # Get do keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get subroutine term
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self.compileTerm()
        else:
            raise RuntimeError('Identifier expected in compileDo')
        
        # Get semicolon
        if self.tokenizer.tokenType() == 'SYMBOL':
            token = self.tokenizer.symbol()
            self.xmlLines.append('<symbol> ' + token + ' </symbol>')

        self.xmlLines.append('</doStatement>')

    """
    compileReturn: Compiles a return statement
    """
    def compileReturn(self):
        self.xmlLines.append('<returnStatement>')

        # Get return keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get expression or colon
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ';':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                self.compileExpression()
                # Get semicolon
                if self.tokenizer.tokenType() == 'SYMBOL':
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                else:
                    raise RuntimeError('; expected in compileReturn')
        else:
            raise RuntimeError('Unexpected end of input')

        self.xmlLines.append('</returnStatement>')

    """
    compileExpression: Compiles an expression -- term (op term)*
    """
    def compileExpression(self):
        self.xmlLines.append('<expression>')
        
        while True:
            tokenType = self.tokenizer.tokenType()
            print('######### calling compileExpression with currToken', self.tokenizer.currToken)
            if tokenType == 'SYMBOL':
                # Exit loop if end of expression with comma, closing parenthesis for expression list, closing square bracket, or semicolon
                token = self.tokenizer.symbol()
                if token == ',' or token == ')' or token == ']' or token == ';':
                    break
                # Get operator
                self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            else:
                self.compileTerm()
                if self.tokenizer.tokenType() == 'SYMBOL':
                    token = self.tokenizer.symbol()
                    if token == ')' or token == ';' or token == ',':
                        break

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                
        self.xmlLines.append('</expression>')

    """
    compileTerm: Compiles a term
        - If the current token is an identifier, the routine must distinguish between a variable,
        an array entry, or a subroutine call.
        - A single look-ahead token, which may be one of "[", "(", or "." suffices to distinguish between the possibilities.
        - Any other token is not part of this term and should not be advanced over
        - Terms: int const, str const, keyword const, varName, varName'['expression']', subroutine call, '('expression')', unary op term
    """
    def compileTerm(self):

        tokenType = self.tokenizer.tokenType()
        print('######### calling compileTerm with current token', self.tokenizer.currToken)
        match tokenType:
            case 'IDENTIFIER':
                currToken = self.tokenizer.identifier()
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'SYMBOL':
                        nextToken = self.tokenizer.symbol()
                        print("look ahead token", nextToken)
                        match nextToken:
                            # Array index
                            case '[':
                                self.xmlLines.append('<term>')
                                self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                                self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                self.compileExpression()
                            # Subroutine arguments
                            case '(':
                                self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                                self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                    self.compileExpressionList()
                                # Get closing parenthesis of expression list
                                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                return
                            # Method identifier
                            # subroutineName'('expressionList')'
                            # (className | varName)'.'subroutineName'('expressionList')'
                            case '.':
                                self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                                self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')

                                # Get subroutine name
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                                        self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                                    else:
                                        raise RuntimeError('subroutineName expected in compileTerm')
                                else:
                                    raise RuntimeError('Unexpected end of input')
                                
                                # Get opening parenthesis of expression list
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                    if self.tokenizer.tokenType() == 'SYMBOL':
                                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                    else:
                                        raise RuntimeError('( expected in compileTerm')
                                else:
                                    raise RuntimeError('Unexpected end of input')
                                
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                self.compileExpressionList()

                                # Get closing parenthesis of expression list
                                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                return
                            case _:
                                self.xmlLines.append('<term>')
                                self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')

                    else:
                        self.xmlLines.append('<term>')
                        self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')


            case 'INT_CONST':
                self.xmlLines.append('<term>')
                self.xmlLines.append('<intVal> ' + self.tokenizer.intVal() + ' </intVal>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
            case 'STRING_CONST':
                self.xmlLines.append('<term>')
                self.xmlLines.append('<stringVal> ' + self.tokenizer.stringVal() + ' </stringVal>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
            # '('expression')' or unary operator
            case 'SYMBOL':
                self.xmlLines.append('<term>')
                token = self.tokenizer.symbol()
                self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                match token:
                    case '(':
                        self.compileExpression()
                        # Get closing parenthesis
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    case '~':
                        self.compileTerm()
                    case '-':
                        self.compileTerm()
            case 'KEYWORD':
                self.xmlLines.append('<term>')
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        self.xmlLines.append('</term>')


    """
    compileExpressionList: Compiles a (possibly empty) comma-separated list of expressions
    """
    def compileExpressionList(self):
        self.xmlLines.append('<expressionList>')

        print('######### calling compileExpressionList currToken', self.tokenizer.currToken)
        
        # Empty expression list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.xmlLines.append('</expressionList>')
            return
        
        else: 
            self.compileExpression()
            while self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                self.compileExpression()
                if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
                    break
                
        self.xmlLines.append('</expressionList>')