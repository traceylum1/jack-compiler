"""
VMWriter class
    - Called by CompilationEngine to write VM code
"""

class VMWriter:
    """
    constructor: Creates a new output .vm file/stream, and prepares it for writing
    """
    def __init__(self, filePath: str):
        self.vmCode = []
        self.filePath = filePath

    """
    writePush: Writes a VM push command
        - segment: CONSTANT, ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
    """
    def writePush(self, segment: str, index: int) -> None:
        vmSegment = ''
        match segment:
            case 'CONSTANT':
                vmSegment = 'constant'
            case 'ARGUMENT':
                vmSegment = 'argument'
            case 'LOCAL':
                vmSegment = 'local'
            case 'STATIC':
                vmSegment = 'static'
            case 'THIS':
                vmSegment = 'this'
            case 'THAT':
                vmSegment = 'that'
            case 'POINTER':
                vmSegment = 'pointer'
            case 'TEMP':
                vmSegment = 'temp'
        self.vmCode.append(f'push {vmSegment} {str(index)}')


    """
    writePop: Writes a VM pop command
        - segment: ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP
    """
    def writePop(self, segment: str, index: int) -> None:
        vmSegment = ''
        match segment:
            case 'CONSTANT':
                vmSegment = 'constant'
            case 'ARGUMENT':
                vmSegment = 'argument'
            case 'LOCAL':
                vmSegment = 'local'
            case 'STATIC':
                vmSegment = 'static'
            case 'THIS':
                vmSegment = 'this'
            case 'THAT':
                vmSegment = 'that'
            case 'POINTER':
                vmSegment = 'pointer'
            case 'TEMP':
                vmSegment = 'temp'
        self.vmCode.append(f'pop {vmSegment} {str(index)}')


    """
    writeArithmetic: Writes a VM arithmetic-logical command
        - command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
    """
    def writeArithmetic(self, command: str) -> None:
        match command:
            case 'LT':
                self.vmCode.append('lt')
            case 'GT':
                self.vmCode.append('gt')
            case 'AND':
                self.vmCode.append('and')
            case 'OR':
                self.vmCode.append('or')
            case 'ADD':
                self.vmCode.append('add')
            case 'SUB':
                self.vmCode.append('sub')
            case 'EQ':
                self.vmCode.append('eq')


    """
    writeLabel: Writes a VM label command
    """
    def writeLabel(self, label: str) -> None:
        pass


    """
    writeGoto: Writes a VM goto command
    """
    def writeGoto(self, label: str) -> None:
        pass

    """
    writeIf: Writes a VM if-goto command
    """
    def writeIf(self, label: str) -> None:
        pass


    """
    writeCall: Writes a VM call command
    """
    def writeCall(self, name: str, nArgs: int) -> None:
        self.vmCode.append(f'call {name} {str(nArgs)}')


    """
    writeFunction: Writes a VM function command
    """
    def writeFunction(self, name: str, nVars: int) -> None:
        self.vmCode.append(f'function {name} {str(nVars)}')


    """
    writeReturn: Writes a VM return command
    """
    def writeReturn(self) -> None:
        self.vmCode.append('return')


    """
    close: Closes the output file / stream
    """
    def close(self) -> None:
        vmOutput = '\n'.join(self.vmCode)

        vmFilePath = self.filePath.split('.')[0] + '.vm'
        
        with open(vmFilePath, 'w') as file:
            print('Writing to new file: ', vmFilePath)
            file.write(vmOutput)