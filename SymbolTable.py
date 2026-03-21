"""
SymbolTable class
    - Handles variable management in class level and subroutine levels
    - Stores variable type, kind, and index
    
    VM segment kinds:
        - local
        - argument
        - this
        - that
        - static
        - constant
        - pointer
        - temp
"""

class SymbolTable:
    """
    Constructor: Creates a new symbol table
    """
    def __init__(self):
        self.classScope = {}
        self.subroutineScope = None

        self.indices = {
            'static': 0,
            'field': 0,
            'argument': 0,
            'local': 0,   # local var
        }
    

    """
    startSubroutine: Starts a new subroutine scope (i.e. resets the subroutine's symbol table)
    """
    def startSubroutine(self):
        self.subroutineScope = {}
        self.indices['argument'] = 0
        self.indices['local'] = 0


    """
    define: Defines a new identifier of the given name, type, and kind, and assigns it a running index.
        - STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope

        Parameters:
            name (String)
            type (String)
            kind (static, field, argument, or local)
    """
    def define(self, name: str, type: str, kind: str) -> None:
        match kind:
            case 'static' | 'field':
                if name in self.classScope:
                    raise RuntimeError(f'Class variable already defined - {name}')
                self.classScope[name] = {'type': type, 'kind': kind, 'index': self.VarCount(kind)}
            case 'argument' | 'local':
                if name in self.subroutineScope:
                    raise RuntimeError(f'Subroutine variable already defined - {name}')
                self.subroutineScope[name] = {'type': type, 'kind': kind, 'index': self.VarCount(kind)}

        self.indices[kind] += 1


    """
    VarCount: Returns the number of variables of the given kind already defined in the current scope

        Parameters:
            kind (static, field, argument, or local)

        Returns:
            int
    """
    def VarCount(self, kind: str) -> int:
        return self.indices[kind]


    """
    KindOf: Returns the kind of the named identifier in the current scope
        - If the identifier is unknown in the current scope, returns 'none'
    
        Parameters:
            name (String)
        
        Returns:
            (static, field, argument, local, none)
    """
    def KindOf(self, name: str) -> str:
        if self.subroutineScope and name in self.subroutineScope:
            return self.subroutineScope[name]['kind']
        elif name in self.classScope:
            return self.classScope[name]['kind']
        else:
            return 'none'


    """
    TypeOf: Returns the type of the named identifier in the current scope

        Parameters:
            name (string)
        
        Returns:
            String
    """
    def TypeOf(self, name: str) -> str:
        if self.subroutineScope and name in self.subroutineScope:
            return self.subroutineScope[name]['type']
        elif name in self.classScope:
            return self.classScope[name]['type']
        else:
            raise Exception('Identifier not declared')

    """
    IndexOf: Returns the index assigned to the named identifier

        Parameters:
            name (String)
        
        Returns:
            int
    """
    def IndexOf(self, name: str) -> int:
        if self.subroutineScope and name in self.subroutineScope:
            return self.subroutineScope[name]['index']
        elif name in self.classScope:
            return self.classScope[name]['index']
        else:
            raise Exception('Identifier not declared')

    def isDefined(self, name: str) -> bool:
        return name in self.subroutineScope