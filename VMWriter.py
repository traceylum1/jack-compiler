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
        - segment: CONSTANT, ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP -- changed to lowercase args
    """
    def writePush(self, segment: str, index: int) -> None:
        vmSegment = ''
        if segment == 'field':
            vmSegment = 'this'
        else:
            vmSegment = segment
        self.vmCode.append(f'push {vmSegment} {str(index)}')


    """
    writePop: Writes a VM pop command
        - segment: ARGUMENT, LOCAL, STATIC, THIS, THAT, POINTER, TEMP -- changed to lowercase args
    """
    def writePop(self, segment: str, index: int) -> None:
        vmSegment = ''
        if segment == 'field':
            vmSegment = 'this'
        else:
            vmSegment = segment
        self.vmCode.append(f'pop {vmSegment} {str(index)}')


    """
    writeArithmetic: Writes a VM arithmetic-logical command
        - command: ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
    """
    def writeArithmetic(self, command: str) -> None:
        if command == 'LT':
            self.vmCode.append('lt')
        elif command == 'GT':
            self.vmCode.append('gt')
        elif command == 'AND':
            self.vmCode.append('and')
        elif command == 'OR':
            self.vmCode.append('or')
        elif command == 'ADD':
            self.vmCode.append('add')
        elif command == 'SUB':
            self.vmCode.append('sub')
        elif command == 'EQ':
            self.vmCode.append('eq')
        elif command == 'NEG':
            self.vmCode.append('neg')
        elif command == 'NOT':
            self.vmCode.append('not')


    """
    writeLabel: Writes a VM label command
    """
    def writeLabel(self, label: str) -> None:
        self.vmCode.append(f'label {label}')


    """
    writeGoto: Writes a VM goto command
    """
    def writeGoto(self, label: str) -> None:
        self.vmCode.append(f'goto {label}')

    """
    writeIf: Writes a VM if-goto command
    """
    def writeIf(self, label: str) -> None:
        self.vmCode.append(f'if-goto {label}')


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