from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable

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
    def __init__(self, tokenizer:  JackTokenizer, symbolTable: SymbolTable, filePath: str):
        self.xmlLines = []

        self.tokenizer = tokenizer
        self.symbolTable = symbolTable

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
                identifier = self.tokenizer.identifier()
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')

                self.xmlLines.append('<identifierName> ' + identifier + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'class' + ' </category>')
                
                self.xmlLines.append('</defining>')
                self.xmlLines.append('</identifier>')
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
                if token ==  'static':
                    self.compileClassVarDec()
                elif token == 'field':
                    self.compileClassVarDec()
                elif token == 'constructor':
                    self.compileSubroutineDec()
                elif token == 'function':
                    self.compileSubroutineDec()
                elif token == 'method':
                    self.compileSubroutineDec()

        if self.tokenizer.tokenType() == 'SYMBOL':
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        self.xmlLines.append('</class>')

    """
    compileClassVarDec: Compiles a static variable declaration, or a field declaration
    """
    def compileClassVarDec(self):
        self.xmlLines.append('<classVarDec>')

        # Store for symbol table
        kind = ''
        type = ''
        varName = ''

        # Get field/static keyword
        kind = self.tokenizer.keyWord()
        self.xmlLines.append('<keyword> ' + kind + ' </keyword>')

        # Get primitive type keyword or class identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                type = self.tokenizer.keyWord()
                self.xmlLines.append('<keyword> ' + type + ' </keyword>')
            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                type = self.tokenizer.identifier()
                self.xmlLines.append('<identifier> ' + type + ' </identifier>')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get variable identifier(s)
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'IDENTIFIER':
                varName = self.tokenizer.identifier()

                # Update symbol table, get category and running index
                self.symbolTable.define(varName, type, kind)
                
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')

                self.xmlLines.append('<identifierName> ' + varName + ' </identifierName>')
                self.xmlLines.append('<category> ' + kind + ' </category>')
                self.xmlLines.append('<index> ' + str(self.symbolTable.IndexOf(varName)) + ' </index>')
                
                self.xmlLines.append('</defining>')
                self.xmlLines.append('</identifier>')

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

        # Create new subroutine scope symbol table
        self.symbolTable.startSubroutine()

        # Get function/method/constructor keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get return type keyword or class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'KEYWORD':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<using>')

                self.xmlLines.append('<identifierName> ' + self.tokenizer.identifier() + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'className' + ' </category>')
                
                self.xmlLines.append('</using>')
                self.xmlLines.append('</identifier>')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get subroutine identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')

                self.xmlLines.append('<identifierName> ' + self.tokenizer.identifier() + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'subroutineName' + ' </category>')
                
                self.xmlLines.append('</defining>')
                self.xmlLines.append('</identifier>')
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

        # Store for symbol table
        kind = 'argument'
        type = ''
        varName = ''

        # Get parameter identifier(s)
        while True:

            # Get parameter primitive/class type and identifier together
            tokenType = self.tokenizer.tokenType()

            if tokenType == 'KEYWORD' or tokenType == 'IDENTIFIER':
                if tokenType == 'KEYWORD':
                    type = self.tokenizer.keyWord()
                    self.xmlLines.append('<keyword> ' + type + ' </keyword>')
                elif tokenType == 'IDENTIFIER':
                    type = self.tokenizer.identifier()
                    self.xmlLines.append('<identifier>')
                    self.xmlLines.append('<using>')
                    self.xmlLines.append('<identifierName> ' + type + ' </identifierName>')
                    self.xmlLines.append('</using>')
                    self.xmlLines.append('</identifier>')

                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        varName = self.tokenizer.identifier()

                        # Update symbol table, get category and running index
                        self.symbolTable.define(varName, type, kind)
                        
                        self.xmlLines.append('<identifier>')
                        self.xmlLines.append('<defining>')

                        self.xmlLines.append('<identifierName> ' + varName + ' </identifierName>')
                        self.xmlLines.append('<category> ' + kind + ' </category>')
                        self.xmlLines.append('<index> ' + str(self.symbolTable.IndexOf(varName)) + ' </index>')
                        
                        self.xmlLines.append('</defining>')
                        self.xmlLines.append('</identifier>')
                    else:
                        raise RuntimeError('Identifier expected')
                else:
                    raise RuntimeError('Unexpected end of input')
            
            # Get comma or end of parameter list
            elif tokenType == 'SYMBOL':
                token = self.tokenizer.symbol()
                # End class var dec if semicolon reached
                if token == ')':
                    break
                elif token == ',':
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            else:
                raise RuntimeError('Keyword, identifier or symbol expected')

            # Get next token
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()

        self.xmlLines.append('</parameterList>')

    """
    compileSubroutineBody: Compiles a subroutine's body
    """
    def compileSubroutineBody(self):
        self.xmlLines.append('<subroutineBody>')

        # Get opening curly bracket
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')

        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                token = self.tokenizer.keyWord()
                if token == 'var':
                    self.compileVarDec()
                elif token == 'let' or token == 'if' or token == 'while' or token == 'do' or token == 'return':
                    self.compileStatements()
                    break
                else:
                    break
            else:
                break

        # Get closing curly bracket
        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        
        self.xmlLines.append('</subroutineBody>')

    """
    compileStatements: Compiles a sequence of statements. Does not handle the enclosing "{}"
    """
    def compileStatements(self):
        self.xmlLines.append('<statements>')
        
        while self.tokenizer.tokenType() == 'KEYWORD':
            token = self.tokenizer.keyWord()
            if token == 'let':
                self.compileLet()
            elif token == 'if':
                self.compileIf()
                continue
            elif token == 'while':
                self.compileWhile()
            elif token == 'do':
                self.compileDo()
            elif token == 'return': 
                self.compileReturn()
            else:
                break
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            
        self.xmlLines.append('</statements>')


    """
    compileVarDec: Compiles a var declaration
    """
    def compileVarDec(self):
        self.xmlLines.append('<varDec>')
        
        # Get var keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
    
        # Store for symbol table
        kind = 'local'
        type = ''
        varName = ''

        # Get primitive type keyword or class identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                type = self.tokenizer.keyWord()
                self.xmlLines.append('<keyword> ' + type + ' </keyword>')
            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                type = self.tokenizer.keyWord()
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<using>')
                self.xmlLines.append('<identifierName> ' + type + ' </identifierName>')
                self.xmlLines.append('</using>')
                self.xmlLines.append('</identifier>')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get variable identifier(s)
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'IDENTIFIER':
                varName = self.tokenizer.identifier()

                # Update symbol table, get category and running index
                self.symbolTable.define(varName, type, kind)
                
                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')

                self.xmlLines.append('<identifierName> ' + varName + ' </identifierName>')
                self.xmlLines.append('<category> ' + kind + ' </category>')
                self.xmlLines.append('<index> ' + str(self.symbolTable.IndexOf(varName)) + ' </index>')
                
                self.xmlLines.append('</defining>')
                self.xmlLines.append('</identifier>')

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
        self.xmlLines.append('<letStatement>')
        
        # Get let keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get next token
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get identifier -- varName('['expression']')?
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()
        else:
            raise RuntimeError('Identifier expected in compileLet')

        self.xmlLines.append('<identifier>')
        self.xmlLines.append('<using>')

        self.xmlLines.append('<identifierName> ' + currToken + ' </identifierName>')
        self.xmlLines.append('<category> ' + self.symbolTable.KindOf(currToken) + ' </category>')
        self.xmlLines.append('<index> ' + str(self.symbolTable.IndexOf(currToken)) + ' </index>')
        
        self.xmlLines.append('</using>')
        self.xmlLines.append('</identifier>')
        
        # Get next token, either assignment operator or opening square bracket for array index
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        if self.tokenizer.tokenType() == 'SYMBOL':
            nextToken = self.tokenizer.symbol()
            if nextToken == '[':
                self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                self.compileExpression()
                # Get closing square bracket
                if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ']':
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                else:
                    raise RuntimeError('] expected in compileLet')
    
        # Get assignment operator
        if self.tokenizer.tokenType() == 'SYMBOL':
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        else:
            raise RuntimeError('= expected in compileLet')
        
        # Compile expression after assignment operator
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpression()
            # Get semicolon
            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
        else:
            raise RuntimeError('Unexpected end of input')

        self.xmlLines.append('</letStatement>')

    """
    compileIf: Compiles an if statement, possibly with a trailing else clause
    """
    def compileIf(self):
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

        # Check for else statement
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            # Get else keyword

            if self.tokenizer.tokenType() == 'KEYWORD' and self.tokenizer.keyWord() == 'else':
                self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
                
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                
                    # Get opening curly braces for else statement
                    if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == '{':
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')

                        # Get statements for else conditional
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileStatements()

                        # Get closing curly bracket for else conditional statements
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')

        self.xmlLines.append('</ifStatement>')


    """
    compileWhile: Compiles a while statement
    """
    def compileWhile(self):
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

        # Get opening curly braces for while statements
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
            else:
                raise RuntimeError('{ expected in compileWhile')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get statements for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
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

        # Get subroutine call without using compileTerm
        # subroutineName'('expressionList')'
        # (className | varName)'.'subroutineName'('expressionList')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        # className/varName or subroutineName
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == 'SYMBOL':
                    token = self.tokenizer.symbol()
                    if token == '(':
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileExpressionList()
                        # Get closing parenthesis of expression list
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                    elif token == '.':
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            if self.tokenizer.tokenType() == 'IDENTIFIER':
                                self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                    if self.tokenizer.tokenType() == 'SYMBOL':
                                        token = self.tokenizer.symbol()
                                        if token == '(':
                                            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                            if self.tokenizer.hasMoreTokens():
                                                self.tokenizer.advance()
                                            self.compileExpressionList()
                                            # Get closing parenthesis of expression list
                                            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                            if self.tokenizer.hasMoreTokens():
                                                self.tokenizer.advance()
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
        
        self.compileTerm()

        while True:
            tokenType = self.tokenizer.tokenType()
            if tokenType == 'SYMBOL':
                # Exit loop if end of expression with comma, closing parenthesis for expression list, closing square bracket, semicolon, or assignment
                token = self.tokenizer.symbol()
                if token == ',' or token == ')' or token == ']' or token == ';':
                    break
                # Get operators
                elif token == '<':
                    self.xmlLines.append('<symbol> ' + '&lt;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '>':
                    self.xmlLines.append('<symbol> ' + '&gt;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '"':
                    self.xmlLines.append('<symbol> ' + '&quot;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '&':
                    self.xmlLines.append('<symbol> ' + '&amp;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '-':
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                    self.compileTerm()
                # Unary op term
                elif token == '~':
                    self.compileTerm()
                # '('expression')'
                elif token == '(':
                    self.compileTerm()
                # Other operators
                else:
                    self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
            # Identifier, keyword, integer const, string const
            else:
                self.compileTerm()

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
        if tokenType == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == 'SYMBOL':
                    nextToken = self.tokenizer.symbol()
                    # Array index
                    if nextToken == '[':
                        self.xmlLines.append('<term>')
                        self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                        self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileExpression()
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        # return
                    # Subroutine arguments
                    elif nextToken == '(':
                        self.xmlLines.append('<term>')
                        self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                        self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            self.compileExpressionList()
                        # Get closing parenthesis of expression list
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        # return
                    # Method identifier
                    # subroutineName'('expressionList')'
                    # (className | varName)'.'subroutineName'('expressionList')'
                    elif nextToken == '.':
                        self.xmlLines.append('<term>')
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
                        # return
                    else:
                        self.xmlLines.append('<term>')
                        self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                        # return

                else:
                    self.xmlLines.append('<term>')
                    self.xmlLines.append('<identifier> ' + currToken + ' </identifier>')
                    # return


        elif tokenType == 'INT_CONST':
            self.xmlLines.append('<term>')
            self.xmlLines.append('<integerConstant> ' + self.tokenizer.intVal() + ' </integerConstant>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        elif tokenType == 'STRING_CONST':
            self.xmlLines.append('<term>')
            self.xmlLines.append('<stringConstant> ' + self.tokenizer.stringVal() + ' </stringConstant>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
        # '('expression')' or unary operator
        elif tokenType == 'SYMBOL':
            self.xmlLines.append('<term>')
            token = self.tokenizer.symbol()
            self.xmlLines.append('<symbol> ' + token + ' </symbol>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            if token == '(':
                self.compileExpression()
                # Get closing parenthesis
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
            elif token == '~':
                self.compileTerm()
            elif token == '-':
                self.compileTerm()
        elif tokenType == 'KEYWORD':
            self.xmlLines.append('<term>')
            self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()

        self.xmlLines.append('</term>')


    """
    compileExpressionList: Compiles a (possibly empty) comma-separated list of expressions
    """
    def compileExpressionList(self):
        self.xmlLines.append('<expressionList>')

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