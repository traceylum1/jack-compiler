"""
SymbolTable class
    - Handles variable management in class level and subroutine levels
    - Stores variable type, kind, and index
"""

class SymbolTable:
    """
    Constructor: Creates a new symbol table
    """
    def __init__(self):
        self.classScope = {}
        self.subroutineScope = None

        self.indices = {
            'STATIC': 0,
            'FIELD': 0,
            'ARG': 0,
            'VAR': 0,
        }
    

    """
    startSubroutine: Starts a new subroutine scope (i.e. resets the subroutine's symbol table)
    """
    def startSubroutine(self):
        self.subroutineScope = {}


    """
    define: Defines a new identifier of the given name, type, and kind, and assigns it a running index.
        - STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope

        Parameters:
            name (String)
            type (String)
            kind (STATIC, FIELD, ARG, or VAR)
    """
    def define(self, name, type, kind):
        match kind:
            case 'STATIC' | 'FIELD':
                self.classScope[name] = {'type': type, 'kind': kind, 'index': self.VarCount(kind)}
            case 'ARG' | 'VAR':
                self.subroutineScope[name] = {'type': type, 'kind': kind, 'index': self.VarCount(kind)}
        self.indices[kind] += 1

    """
    VarCount: Returns the number of variables of the given kind already defined in the current scope

        Parameters:
            kind (STATIC, FIELD, ARG, or VAR)

        Returns:
            int
    """
    def VarCount(self, kind):
        return self.indices[kind]


    """
    KindOf: Returns the kind of the named identifier in the current scope
        - If the identifier is unknown in the current scope, returns NONE
    
        Parameters:
            name (String)
        
        Returns:
            (STATIC, FIELD, ARG, VAR, NONE)
    """
    def KindOf(self, name):
        if name in self.subroutineScope:
            return self.subroutineScope[name].kind
        elif name in self.classScope:
            return self.classScope[name].kind
        else:
            return 'NONE'

    """
    TypeOf: Returns the type of the named identifier in the current scope

        Parameters:
            name (string)
        
        Returns:
            String
    """
    def TypeOf(self, name):
        if name in self.subroutineScope:
            return self.subroutineScope[name].type
        elif name in self.classScope:
            return self.classScope[name].type
        else:
            raise Exception('Identifier not declared')

    """
    IndexOf: Returns the index assigned to the named identifier

        Parameters:
            name (String)
        
        Returns:
            int
    """
    def IndexOf(self, name):
        if name in self.subroutineScope:
            return self.subroutineScope[name].index
        elif name in self.classScope:
            return self.classScope[name].index
        else:
            raise Exception('Identifier not declared')
