from JackTokenizer import JackTokenizer
from SymbolTable import SymbolTable
from VMWriter import VMWriter

"""
CompilationEngine class
    - Takes the input from the tokenizer
    - Compiles the non-terminal tokens
    - Outputs to .vm file
"""

class CompilationEngine:
    """
    Constructor: Gets input from tokenizer and compiles VM code
    """
    def __init__(self, tokenizer:  JackTokenizer, filePath: str):

        self.tokenizer = tokenizer
        self.symbolTable = SymbolTable()
        self.vmWriter = VMWriter(filePath=filePath)

        self.className = ''
        self.currSubroutineName = ''
        self.currSubroutineType = ''
        self.currSubroutineReturnType = ''
        self.currIfIdx = 0
        self.currWhileIdx = 0


        if len(tokenizer.lines) == 0:
            print('File empty. Nothing to compile')
            return
        
        self.compileClass()

        self.vmWriter.close()
    
    """
    compileClass: Compiles a complete class (called immediately after constructor)
    """
    def compileClass(self):

        # Get class keyword
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                pass
            else:
                raise RuntimeError('Keyword expected')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get class identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.className = self.tokenizer.identifier()


            else:
                raise RuntimeError('Identifier expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get opening curly bracket for class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
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
            pass

    """
    compileClassVarDec: Compiles a static variable declaration, or a field declaration
    """
    def compileClassVarDec(self):

        # Store for symbol table
        kind = ''
        type = ''
        varName = ''

        # Get field/static keyword
        kind = self.tokenizer.keyWord()

        # Get primitive type keyword or class identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'KEYWORD':
                type = self.tokenizer.keyWord()
            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                type = self.tokenizer.identifier()

        else:
            raise RuntimeError('Unexpected end of input')

        # Get variable identifier(s)
        while self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'IDENTIFIER':
                varName = self.tokenizer.identifier()

                # Update symbol table, get category and running index
                self.symbolTable.define(varName, type, kind)
                

                

            elif self.tokenizer.tokenType() == 'SYMBOL':
                token = self.tokenizer.symbol()
                # End class var dec if semicolon reached
                if token == ';':
                    break
                elif token == ',':
                    pass
            else:
                raise RuntimeError('Identifier or symbol expected')
            
        
    """
    compileSubroutineDec: Compiles a complete method, function, or constructor

        - For void subroutine, push const 0 before returning
    """
    def compileSubroutineDec(self):

        # Create new subroutine scope symbol table
        self.symbolTable.startSubroutine()

        # Reset label indexes
        self.currIfIdx = 0
        self.currWhileIdx = 0

        # Get function/method/constructor keyword
        self.currSubroutineType = self.tokenizer.keyWord()


        # Get return type keyword or class
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'KEYWORD':
                self.currSubroutineReturnType = self.tokenizer.keyWord()

            elif self.tokenizer.tokenType() == 'IDENTIFIER':
                self.currSubroutineReturnType = self.tokenizer.keyWord()

        else:
            raise RuntimeError('Unexpected end of input')

        # Get subroutine identifier
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'IDENTIFIER':
                self.currSubroutineName = self.tokenizer.identifier()

            else:
                raise RuntimeError('Identifier expected')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get opening parenthesis for parameter list
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
            else:
                raise RuntimeError('( expected')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get parameter list or closing parenthesis
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileParameterList()
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


    """
    compileParameterList: Compiles a (possible empty) parameter list. Does not handle the enclosing "()"
    """
    def compileParameterList(self):

        # Store for symbol table
        kind = 'argument'
        type = ''
        varName = ''

        # Set first argument as this object -- placeholder so the running index is correct for next parameters
        if self.currSubroutineType == 'method':
            self.symbolTable.define('this', self.className, 'argument')

        # Empty parameter list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            return

        # Get parameter identifier(s)
        while True:

            # Get parameter primitive/class type and identifier together
            tokenType = self.tokenizer.tokenType()

            if tokenType == 'KEYWORD' or tokenType == 'IDENTIFIER':
                if tokenType == 'KEYWORD':
                    type = self.tokenizer.keyWord()
                elif tokenType == 'IDENTIFIER':
                    type = self.tokenizer.identifier()

                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        varName = self.tokenizer.identifier()

                        # Update symbol table, get category and running index
                        self.symbolTable.define(varName, type, kind)
                        

                        
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
                    pass
            else:
                raise RuntimeError('Keyword, identifier or symbol expected')

            # Get next token
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()


    """
    compileSubroutineBody: Compiles a subroutine's body
    """
    def compileSubroutineBody(self):

        # Get opening curly bracket

        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        if self.tokenizer.tokenType() == 'KEYWORD':
            self.compileVarDec()

            # Get block of memory for constructing object, set base addr to pointer 0
            if self.currSubroutineType == 'constructor':
                objSize = self.symbolTable.VarCount('field')
                self.vmWriter.writePush('constant', objSize)
                self.vmWriter.writeCall('Memory.alloc', 1)
                self.vmWriter.writePop('pointer', 0)
            # Set pointer to first argument which is the object
            elif self.currSubroutineType == 'method':
                self.vmWriter.writePush('argument', 0)
                self.vmWriter.writePop('pointer', 0)

            self.compileStatements()
        else:
            raise RuntimeError('Keyword expected in compileSubroutineBody')

        # Get closing curly bracket
        

    """
    compileStatements: Compiles a sequence of statements. Does not handle the enclosing "{}"
    """
    def compileStatements(self):
        
        while self.tokenizer.tokenType() == 'KEYWORD':
            token = self.tokenizer.keyWord()
            if token == 'let':
                self.compileLet()
            elif token == 'if':
                self.compileIf()
                continue        # Advanced in compileIf to check for else statement
            elif token == 'while':
                self.compileWhile()
            elif token == 'do':
                self.compileDo()
            elif token == 'return':
                self.compileReturn(self.currSubroutineReturnType == 'void')
            else:
                break
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            


    """
    compileVarDec: Compiles a var declaration
    """
    def compileVarDec(self):

        # Store for symbol table
        kind = 'local'
        type = ''
        varName = ''
        
        while self.tokenizer.keyWord() == 'var':

            
            # Get var keyword

            # Get primitive type keyword or class identifier
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == 'KEYWORD':
                    type = self.tokenizer.keyWord()
                elif self.tokenizer.tokenType() == 'IDENTIFIER':
                    type = self.tokenizer.keyWord()


            else:
                raise RuntimeError('Unexpected end of input')
            
            # Get variable identifier(s) of current type
            while self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()

                if self.tokenizer.tokenType() == 'IDENTIFIER':
                    varName = self.tokenizer.identifier()

                    # Update symbol table, get category and running index
                    self.symbolTable.define(varName, type, kind)
                    

                    

                elif self.tokenizer.tokenType() == 'SYMBOL':
                    token = self.tokenizer.symbol()
                    # End curr type var dec if semicolon reached
                    if token == ';':
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        break
                    elif token == ',':
                        pass
                else:
                    raise RuntimeError('Identifier or symbol expected in compileVarDec')
                
        
        nVars = self.symbolTable.VarCount('local')

        if self.currSubroutineType == 'method':
            nVars += 1

        self.vmWriter.writeFunction(f"{self.className}.{self.currSubroutineName}", nVars)
        

    """
    compileLet: Compiles a let statement
    """
    def compileLet(self):
        
        # Store for VM writer
        currToken = ''
        currTokenKind = ''
        currTokenIdx = ''

        # Get let keyword

        # Get next token
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        # Get identifier -- varName('['expression']')?
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()
            currTokenKind = self.symbolTable.KindOf(currToken)
            currTokenIdx = self.symbolTable.IndexOf(currToken)

        else:
            raise RuntimeError('Identifier expected in compileLet')


        
        
        isArrayAssignment = False

        # Get next token, either assignment operator or opening square bracket for array index
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        else:
            raise RuntimeError('Unexpected end of input')
        
        if self.tokenizer.tokenType() == 'SYMBOL':
            nextToken = self.tokenizer.symbol()
            if nextToken == '[':
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                
                # Push array base addr to stack
                self.vmWriter.writePush(currTokenKind, currTokenIdx)

                # Compile expression for array index
                self.compileExpression()

                # Compute target address. Keep it on stack until RHS is compiled,
                # then assign via THAT using temp/pointer sequence.
                self.vmWriter.writeArithmetic('ADD')
                isArrayAssignment = True

                # Get closing square bracket
                if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ']':
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                else:
                    raise RuntimeError('] expected in compileLet')
                
            
    
        # Get assignment operator
        if self.tokenizer.tokenType() == 'SYMBOL':
            pass
        else:
            raise RuntimeError('= expected in compileLet')
        
        # Compile expression after assignment operator
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            self.compileExpression()
            # Get semicolon
        else:
            raise RuntimeError('Unexpected end of input')

        if isArrayAssignment:
            self.vmWriter.writePop('temp', 0)
            self.vmWriter.writePop('pointer', 1)
            self.vmWriter.writePush('temp', 0)
            self.vmWriter.writePop('that', 0)
        else:
            self.vmWriter.writePop(currTokenKind, currTokenIdx)


    """
    compileIf: Compiles an if statement, possibly with a trailing else clause
    """
    def compileIf(self):

        # Get if keyword

        # Get opening parenthesis for if conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
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
            pass
        else:
            raise RuntimeError(') expected')
        
        # LABELS
        label_true = f'IF_TRUE_{str(self.currIfIdx)}'
        label_false = f'IF_FALSE_{str(self.currIfIdx)}'
        label_end = f'IF_END_{str(self.currIfIdx)}'

        self.vmWriter.writeIf(label_true)
        self.vmWriter.writeGoto(label_false)
        self.vmWriter.writeLabel(label_true)

        self.currIfIdx += 1


        # Get opening curly bracket for if conditional statements
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
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

        # Check for else statement
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            # Get else keyword

            if self.tokenizer.tokenType() == 'KEYWORD' and self.tokenizer.keyWord() == 'else':

                # LABELS
                self.vmWriter.writeGoto(label_end)
                self.vmWriter.writeLabel(label_false)
                
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                
                    # Get opening curly braces for else statement
                    if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == '{':

                        # Get statements for else conditional
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        self.compileStatements()

                        self.vmWriter.writeLabel(label_end)

                        # Get closing curly bracket for else conditional statements

                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
            
            else:
                self.vmWriter.writeLabel(label_false)

        else:
            raise RuntimeError('Unexpected end of input')



    """
    compileWhile: Compiles a while statement
    """
    def compileWhile(self):

        # Get while keyword

        # Get opening parenthesis for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
            else:
                raise RuntimeError('( expected in compileWhile')
        else:
            raise RuntimeError('Unexpected end of input')
        
        # LABELS
        label_while_start = f'WHILE_START_{str(self.currWhileIdx)}'
        label_while_end = f'WHILE_END_{str(self.currWhileIdx)}'
        self.currWhileIdx += 1

        self.vmWriter.writeLabel(label_while_start)

        # Get expression for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileExpression()
        
        # Get closing parenthesis for while conditional
        if self.tokenizer.tokenType() == 'SYMBOL':
            pass
        else:
            raise RuntimeError(') expected in compileWhile')

        self.vmWriter.writeArithmetic('NOT')
        self.vmWriter.writeIf(label_while_end)

        # Get opening curly braces for while statements
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL':
                pass
            else:
                raise RuntimeError('{ expected in compileWhile')
        else:
            raise RuntimeError('Unexpected end of input')

        # Get statements for while conditional
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
        self.compileStatements()

        # Get closing curly bracket for while statements

        self.vmWriter.writeGoto(label_while_start)
        self.vmWriter.writeLabel(label_while_end)
        

    """
    compileDo: Compiles a do statement

        - Calls a void function/method (never constructor bc it returns base addr)
        - m
    """
    def compileDo(self):

        className = ''
        subroutineName = ''
        nArgs = 0

        # Get do keyword

        # Get subroutine call without using compileTerm
        # subroutineName'('expressionList')'
        # (className | varName)'.'subroutineName'('expressionList')'
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()

        # className/varName or subroutineName
        if self.tokenizer.tokenType() == 'IDENTIFIER':
            currToken = self.tokenizer.identifier()

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()

            if self.tokenizer.tokenType() == 'SYMBOL':
                nextToken = self.tokenizer.symbol()

                # currToken is subroutine name
                if nextToken == '(':
                    subroutineName = currToken



                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()
                    nArgs += self.compileExpressionList()
                    # Get closing parenthesis of expression list
                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()

                # currToken is class or obj name
                elif nextToken == '.':

                    # If current token is name of object, then this is a METHOD
                    if self.symbolTable.isDefined(currToken):
                        className = self.symbolTable.TypeOf(currToken)
                        objType = self.symbolTable.KindOf(currToken)
                        objIdx = self.symbolTable.IndexOf(currToken)
                        self.vmWriter.writePush(objType, objIdx)
                        nArgs += 1
                    else:
                        className = currToken



                    if self.tokenizer.hasMoreTokens():
                        self.tokenizer.advance()

                    # Get subroutine name
                    if self.tokenizer.tokenType() == 'IDENTIFIER':
                        subroutineName = self.tokenizer.identifier()


                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            if self.tokenizer.tokenType() == 'SYMBOL':
                                token = self.tokenizer.symbol()
                                if token == '(':
                                    if self.tokenizer.hasMoreTokens():
                                        self.tokenizer.advance()
                                    nArgs += self.compileExpressionList()

                                    # Get closing parenthesis of expression list
                                    if self.tokenizer.hasMoreTokens():
                                        self.tokenizer.advance()
        else:
            raise RuntimeError('Identifier expected in compileDo')
        
        # Get semicolon
        if self.tokenizer.tokenType() == 'SYMBOL':
            token = self.tokenizer.symbol()

        functionName = ''

        # Method call on object instance
        if className:
            functionName = className + '.' + subroutineName

        # Method call on current class
        else:
            self.vmWriter.writePush('pointer', 0)
            nArgs += 1
            functionName = self.className + '.' + subroutineName
        
        self.vmWriter.writeCall(functionName, nArgs)
        self.vmWriter.writePop('temp', 0)   # Discard default returned 0



    """
    compileReturn: Compiles a return statement
    """
    def compileReturn(self, isVoid):

        # Get return keyword

        # Get expression or colon
        if self.tokenizer.hasMoreTokens():
            self.tokenizer.advance()
            if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ';':
                pass
            else:
                self.compileExpression()
                # Get semicolon
                if self.tokenizer.tokenType() == 'SYMBOL':
                    pass
                else:
                    raise RuntimeError('; expected in compileReturn')
        else:
            raise RuntimeError('Unexpected end of input')
        
        if isVoid:
            self.vmWriter.writePush('constant', 0)

        self.vmWriter.writeReturn()


    """
    compileExpression: Compiles an expression -- term (op term)*
    """
    def compileExpression(self):
        
        self.compileTerm()

        while True:
            tokenType = self.tokenizer.tokenType()
            if tokenType == 'SYMBOL':
                # Exit loop if end of expression with comma, closing parenthesis for expression list, closing square bracket, semicolon
                token = self.tokenizer.symbol()
                if token == ',' or token == ')' or token == ']' or token == ';':
                    break
                
                operator = ''
                # Get operators / symbols
                if token == '<':
                    operator = 'LT'
                elif token == '>':
                    operator = 'GT'
                elif token == '&':
                    operator = 'AND'
                elif token == '|':
                    operator = 'OR'
                elif token == '+':
                    operator = 'ADD'
                elif token == '-':
                    operator = 'SUB'
                elif token == '=':
                    operator = 'EQ'
                elif token == '*':
                    operator = 'MULTIPLY'
                elif token == '/':
                    operator = 'DIVIDE'
                else:
                    raise RuntimeError(f'Invalid expression operator: {token}')

                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                else:
                    raise RuntimeError('Unexpected end of input in compileExpression')

                self.compileTerm()

                if operator == 'MULTIPLY':
                    self.vmWriter.writeCall('Math.multiply', 2) # Call Math.multiply
                elif operator == 'DIVIDE':
                    self.vmWriter.writeCall('Math.divide', 2) # Call Math.divide
                else:
                    self.vmWriter.writeArithmetic(operator)
            else:
                break


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
            currTokenKind = ''
            currTokenIdx = ''
            nArgs = 0

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
                if self.tokenizer.tokenType() == 'SYMBOL':
                    nextToken = self.tokenizer.symbol()
                    
                    # Array index
                    if nextToken == '[':
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()

                        # Push array base addr to stack
                        currTokenKind = self.symbolTable.KindOf(currToken)
                        currTokenIdx = self.symbolTable.IndexOf(currToken)
                        self.vmWriter.writePush(currTokenKind, currTokenIdx)

                        self.compileExpression()
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()

                        # Add the offset of index to the base address and set to THAT
                        self.vmWriter.writeArithmetic('ADD')
                        self.vmWriter.writePop('pointer', 1)

                        self.vmWriter.writePush('that', 0)

                    # METHOD of CURRENT CLASS
                    elif nextToken == '(':

                        # Push this to stack
                        self.vmWriter.writePush('pointer', 0)
                        nArgs = 1

                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            nArgs += self.compileExpressionList()
                        # Get closing parenthesis of expression list
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        
                        self.vmWriter.writeCall(currToken, nArgs)

                    # METHOD OR FUNCTION OF OTHER CLASS
                    # subroutineName'('expressionList')'
                    # (className | varName)'.'subroutineName'('expressionList')'
                    elif nextToken == '.':
                        
                        className = ''
                        subroutineName = ''
                        # Handle METHOD call on object
                        if self.symbolTable.isDefined(currToken):
                            currTokenKind = self.symbolTable.KindOf(currToken)
                            currTokenIdx = self.symbolTable.IndexOf(currToken)
                            className = self.symbolTable.TypeOf(currToken)
                            self.vmWriter.writePush(currTokenKind, currTokenIdx)
                            nArgs += 1
                        # Handle FUNCTION call
                        else:
                            className = currToken


                        # Get subroutine name
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            if self.tokenizer.tokenType() == 'IDENTIFIER':
                                subroutineName = self.tokenizer.identifier()
                            else:
                                raise RuntimeError('subroutineName expected in compileTerm')
                        else:
                            raise RuntimeError('Unexpected end of input')
                        
                        # Get opening parenthesis of expression list
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                            if self.tokenizer.tokenType() == 'SYMBOL':
                                pass
                            else:
                                raise RuntimeError('( expected in compileTerm')
                        else:
                            raise RuntimeError('Unexpected end of input')
                        
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        nArgs += self.compileExpressionList()

                        # Get closing parenthesis of expression list
                        if self.tokenizer.hasMoreTokens():
                            self.tokenizer.advance()
                        
                        self.vmWriter.writeCall(f'{className}.{subroutineName}', nArgs)

                    # Next token is comma or semicolon indicating end of identifier term
                    else:
                        currTokenKind = self.symbolTable.KindOf(currToken)
                        currTokenIdx = self.symbolTable.IndexOf(currToken)
                        self.vmWriter.writePush(currTokenKind, currTokenIdx)




                # # Regular identifier term ? is this necessary? should ONLY expect symbol after identifier term anyways.
                # else:
                    pass





        elif tokenType == 'INT_CONST':
            intValToken = self.tokenizer.intVal()
            self.vmWriter.writePush('constant', int(intValToken))

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            
        elif tokenType == 'STRING_CONST':
            strValToken = self.tokenizer.stringVal()
            
            self.vmWriter.writePush('constant', len(strValToken))
            self.vmWriter.writeCall('String.new', 1)

            for c in strValToken:
                self.vmWriter.writePush('constant', ord(c))
                self.vmWriter.writeCall('String.appendChar', 2)

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()

        # '('expression')' or unary operator
        elif tokenType == 'SYMBOL':
            token = self.tokenizer.symbol()
            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()
            if token == '(':
                self.compileExpression()
                # Get closing parenthesis
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
            elif token == '~':
                self.compileTerm()
                self.vmWriter.writeArithmetic('NOT')
            elif token == '-':
                self.compileTerm()
                self.vmWriter.writeArithmetic('NEG')
        
        # true, false, null, etc.
        elif tokenType == 'KEYWORD':
            token = self.tokenizer.keyWord()
            if token == 'true':
                self.vmWriter.writePush('constant', 1)
                self.vmWriter.writeArithmetic('NEG')
            elif token in ('false', 'null'):
                self.vmWriter.writePush('constant', 0)
            elif token == 'this':
                self.vmWriter.writePush('pointer', 0)

            if self.tokenizer.hasMoreTokens():
                self.tokenizer.advance()



    """
    compileExpressionList: Compiles a (possibly empty) comma-separated list of expressions
    """
    def compileExpressionList(self):

        count = 0


        # Empty expression list
        if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
            return 0
        
        else: 
            self.compileExpression()
            count += 1
            while self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ',':
                if self.tokenizer.hasMoreTokens():
                    self.tokenizer.advance()
                self.compileExpression()
                count += 1
                if self.tokenizer.tokenType() == 'SYMBOL' and self.tokenizer.symbol() == ')':
                    break
                

        return count
