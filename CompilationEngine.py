from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

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
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(filePath=filePath)

        self.className = ''
        self.currSubroutineName = ''

        if len(tokenizer.lines) == 0:
            print('File empty. Nothing to compile')
            return
        
        self.compileClass()

        xmlOutput = '\n'.join(self.xmlLines)

        xmlFilePath = filePath.split('.')[0] + '.xml'
        
        with open(xmlFilePath, 'w') as file:
            print('Writing to new file: ', xmlFilePath)
            file.write(xmlOutput)
        
        self.vmWriter.close()
    
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
                self.className = self.tokenizer.identifier()

                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')
                self.xmlLines.append('<identifierName> ' + self.className + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'className' + ' </category>')
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

                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<using>')
                self.xmlLines.append('<identifierName> ' + type + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'className' + ' </category>')
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

        - For void subroutine, push const 0 before returning
    """
    def compileSubroutineDec(self):
        self.xmlLines.append('<subroutineDec>')

        # Create new subroutine scope symbol table
        self.symbolTable.startSubroutine()

        # Store for VM writer
        funcType = ''
        returnType = ''


        # Get function/method/constructor keyword
        funcType = self.tokenizer.keyWord()
        match funcType:
            case 'function':
                pass
            case 'method':
                pass
            case 'constructor':
                pass

        self.xmlLines.append('<keyword> ' + funcType + ' </keyword>')

        # Get return type keyword or class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'KEYWORD':
                returnType = self.tokenizer.keyWord()
                self.xmlLines.append('<keyword> ' + returnType + ' </keyword>')

            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                returnType = self.tokenizer.keyWord()

                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<using>')
                self.xmlLines.append('<identifierName> ' + returnType + ' </identifierName>')
                self.xmlLines.append('<category> ' + 'className' + ' </category>')
                self.xmlLines.append('</using>')
                self.xmlLines.append('</identifier>')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get subroutine identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.currSubroutineName = self.tokenizer.identifier()

                self.xmlLines.append('<identifier>')
                self.xmlLines.append('<defining>')
                self.xmlLines.append('<identifierName> ' + self.currSubroutineName + ' </identifierName>')
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
    def compileParameterList(self) -> int:
        self.xmlLines.append('<parameterList>')

        # Store for symbol table
        kind = 'argument'
        type = ''
        varName = ''

        # Empty parameter list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.xmlLines.append('</parameterList>')
            return

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

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        if self.tokenizer.tokenType() == 'KEYWORD':
            self.compileVarDec()
            self.compileStatements()
        else:
            raise RuntimeError('Keyword expected in compileSubroutineBody')

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

        # No local variables
        if self.tokenizer.keyWord() != 'var':
            self.vmWriter.writeFunction(self.currSubroutineName, 0)
            return

        self.xmlLines.append('<varDec>')

        # Store for symbol table
        kind = 'local'
        type = ''
        varName = ''
        
        # Get var keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

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
                self.xmlLines.append('<category> ' + 'className' + ' </category>')

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
        else:
            raise RuntimeError('Unexpected end of input')
        
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
        else:
            raise RuntimeError('Unexpected end of input')
        
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
        else:
            raise RuntimeError('Unexpected end of input')

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

        - Calls a void function/method (never constructor bc it returns base addr)
        - m
    """
    def compileDo(self):
        self.xmlLines.append('<doStatement>')

        className = ''
        subroutineName = ''
        argCount = 0

        # Get do keyword
        self.xmlLines.append('<keyword> ' + self.tokenizer.keyWord() + ' </keyword>')

        # Get subroutine call without using compileTerm
        # subroutineName'('expressionList')'
        # (className | varName)'.'subroutineName'('expressionList')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        # className/varName or subroutineName
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()
            # self.xmlLines.append('<identifier> ' + self.tokenizer.identifier() + ' </identifier>')
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == 'SYMBOL':
                    nextToken = self.tokenizer.symbol()
                    # currToken is subroutine name
                    if nextToken == '(':
                        subroutineName = currToken

                        self.xmlLines.append('<identifier>')
                        self.xmlLines.append('<using>')
                        self.xmlLines.append('<identifierName> ' + currToken + ' </identifierName>')
                        self.xmlLines.append('<category> ' + 'subroutineName' + ' </category>')
                        self.xmlLines.append('</using>')
                        self.xmlLines.append('</identifier>')

                        self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')

                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileExpressionList()
                        # Get closing parenthesis of expression list
                        self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                    # currToken is class name
                    elif nextToken == '.':
                        className = currToken

                        self.xmlLines.append('<identifier>')
                        self.xmlLines.append('<using>')
                        self.xmlLines.append('<identifierName> ' + currToken + ' </identifierName>')
                        self.xmlLines.append('<category> ' + 'className' + ' </category>')
                        self.xmlLines.append('</using>')
                        self.xmlLines.append('</identifier>')

                        self.xmlLines.append('<symbol> ' + nextToken + ' </symbol>')

                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            # Get subroutine name
                            if self.tokenizer.tokenType() == 'IDENTIFIER':
                                subroutineName = self.tokenizer.identifier()

                                self.xmlLines.append('<identifier>')
                                self.xmlLines.append('<using>')
                                self.xmlLines.append('<identifierName> ' + subroutineName + ' </identifierName>')
                                self.xmlLines.append('<category> ' + 'subroutineName' + ' </category>')
                                self.xmlLines.append('</using>')
                                self.xmlLines.append('</identifier>')

                                if self.tokenizer.hasMoreTokens():
                                    self.tokenizer.advance()
                                    if self.tokenizer.tokenType() == 'SYMBOL':
                                        token = self.tokenizer.symbol()
                                        if token == '(':
                                            self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                                            if self.tokenizer.hasMoreTokens():
                                                self.tokenizer.advance()
                                            argCount = self.compileExpressionList()

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

        functionName = ''
        if className != '':
            functionName = className + '.' + subroutineName
        else:
            functionName = subroutineName
        
        self.vmWriter.writeCall(functionName, argCount)
        self.vmWriter.writePop('TEMP', 0)   # Discard default returned 0

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
        
        self.vmWriter.writeReturn()

        self.xmlLines.append('</returnStatement>')

    """
    compileExpression: Compiles an expression -- term (op term)*
    """
    def compileExpression(self):
        self.xmlLines.append('<expression>')
        
        self.compileTerm()
        operator = ''

        while True:
            tokenType = self.tokenizer.tokenType()
            if tokenType == 'SYMBOL':
                # Exit loop if end of expression with comma, closing parenthesis for expression list, closing square bracket, semicolon
                token = self.tokenizer.symbol()
                if token == ',' or token == ')' or token == ']' or token == ';':
                    break
                # Get operators / symbols
                elif token == '<':
                    operator = 'LT'
                    self.xmlLines.append('<symbol> ' + '&lt;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '>':
                    operator = 'GT'
                    self.xmlLines.append('<symbol> ' + '&gt;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '"':
                    self.xmlLines.append('<symbol> ' + '&quot;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '&':
                    operator = 'AND'
                    self.xmlLines.append('<symbol> ' + '&amp;' + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '|':
                    operator = 'OR'
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '+':
                    operator = 'ADD'
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '-':
                    operator = 'SUB'
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '*':
                    operator = 'MULTIPLY'
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                elif token == '/':
                    operator = 'DIVIDE'
                    self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                
                # Unary op term
                elif token == '~':
                    self.compileTerm()
                # '('expression')'
                elif token == '(':
                    self.compileTerm()
                # # Other operators
                # else:
                #     self.xmlLines.append('<symbol> ' + token + ' </symbol>')
                #     if self.tokenizer.hasMoreTokens():
                #         self.tokenizer.advance()

            # Identifier, keyword, integer const, string const
            else:
                self.compileTerm()
            
        match operator:
            case 'MULTIPLY':
                self.vmWriter.writeCall('Math.multiply', 2) # Call Math.multiply
            case 'DIVIDE':
                self.vmWriter.writeCall('Math.divide', 2) # Call Math.divide
            case _:
                self.vmWriter.writeArithmetic(operator)

        self.xmlLines.append('</expression>')

    """
    compileTerm: Compiles a term
        - If the current token is an identifier, the routine must distinguish between a variable,
        an array entry, or a subroutine call.
        - A single look-ahead token, which may be one of "[", "(", or "." suffices to distinguish between the possibilities.
        - Any other token is not part of this term and should not be advanced over
        - Terms: int const, str const, keyword const, varName, varName'['expression']', subroutine call, '('expression')', unary op term

        SUBROUTINE CALL:
            - Needs to differentiate between function, method, constructor calls
            - FUNCTION: not called on any object (nArgs) -- ie: Output.printInt(1), move()
                PROCESS:
                    1. ALWAYS contains 2 identifiers, check if first one is in symbol table
                        a. if so, it is a METHOD on target object -- handle as METHOD
                        b. if not, it is a FUNCTION (from current or other class)
                    2. push arguments to stack
                    3. call function (call className.subroutineName nArgs)

            - METHOD: Called on an object (nArgs + THIS) -- ie: object.erase() OR move()
                PROCESS:
                    1. check symbol table to see if object is declared -- identifierName: { type: className, kind: 'local', index: int }
                        a. if so, it is a METHOD on target object -- handle as METHOD
                        b. if not, it is a FUNCTION call
                    2. push object to stack (pointer 0)
                    3. push arguments to stack
                    4. call method (call (className.)?subroutineName nArgs+1)

            - CONSTRUCTOR: get block of nVar size, store in pointer 0
                PROCESS: 
                    1. call malloc with size nVar
                    2. malloc find n size block (initialize all to 0?)
                    3. malloc returns base memory addr
                    4. store pointer to new object in local/field var
                    5. to access object, set pointer 0 to object
                    6. use THIS 0-(nVar-1) to access object's local vars

        ARRAY INDEX:
            - ALWAYS work with THAT 0 -- necessary to index with identifiers too. ie works for both arr[x] and arr[5]
            - set pointer 1 to array pointer
            - offset base address by index (keep in THAT 0)
    """
    def compileTerm(self):

        tokenType = self.tokenizer.tokenType()
        if tokenType == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()

            currTokenKind = self.symbolTable.KindOf(currToken)
            currTokenIdx = self.symbolTable.IndexOf(currToken)

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

                    # Subroutine call and arguments
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

                    # Next token is comma or semicolon indicating end of term
                    else:
                        self.xmlLines.append('<term>')
                        self.xmlLines.append('<identifier>')
                        self.xmlLines.append('<using>')

                        self.xmlLines.append('<identifierName> ' + currToken + ' </identifierName>')
                        self.xmlLines.append('<category> ' + currTokenKind + ' </category>')
                        self.xmlLines.append('<index> ' + str(currTokenIdx) + ' </index>')

                        self.xmlLines.append('</using>')
                        self.xmlLines.append('</identifier>')

                # # Regular identifier term ? is this necessary? should ONLY expect symbol after identifier term anyways.
                # else:
                #     self.xmlLines.append('<term>')

                #     self.xmlLines.append('<identifier>')
                #     self.xmlLines.append('<using>')

                #     self.xmlLines.append('<identifierName> ' + currToken + ' </identifierName>')
                #     self.xmlLines.append('<category> ' + currTokenKind + ' </category>')
                #     self.xmlLines.append('<index> ' + currTokenIdx + ' </index>')

                #     self.xmlLines.append('</using>')
                #     self.xmlLines.append('</identifier>')


        elif tokenType == 'INT_CONST':
            intValToken = self.tokenizer.intVal()
            self.vmWriter.writePush('CONSTANT', int(intValToken))
            self.xmlLines.append('<term>')
            self.xmlLines.append('<integerConstant> ' + intValToken + ' </integerConstant>')
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

        count = 0

        self.xmlLines.append('<expressionList>')

        # Empty expression list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            self.xmlLines.append('</expressionList>')
            return
        
        else: 
            self.compileExpression()
            count += 1
            while self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                self.xmlLines.append('<symbol> ' + self.tokenizer.symbol() + ' </symbol>')
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                self.compileExpression()
                count += 1
                if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
                    break
                
        self.xmlLines.append('</expressionList>')

        return count