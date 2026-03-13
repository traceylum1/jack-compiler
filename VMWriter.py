"""
VMWriter class
    - Called by CompilationEngine to write VM code
"""

class VMWriter:
    """
    constructor: Creates a new output .vm file/stream, and prepares it for writing
    """
    def __init__(self):
        self.vmCode = []
    

    """
    writePush: Writes a VM push command
    """
    def writePush(self, segment: str, index: int) -> None:
        self.vmCode.append(f"push ${segment} ${index}\n")

    """
    writePop: Writes a VM pop command
    """
    def writePop(self, segment: str, index: int) -> None:
        self.vmCode.append(f"pop ${segment} ${index}\n")

    """
    writeArithmetic: Writes a VM arithmetic-logical command
    """
    def writeArithmetic(self, command: str) -> None:
        self.vmCode.append(f"${command}\n")

    def writeLabel(self, label: str) -> None:
        pass

    def writeGoto(self, label: str) -> None:
        pass

    def writeIf(self, label: str) -> None:
        pass

    def writeCall(self, label: str) -> None:
        pass

    def writeFunction(self, label: str) -> None:
        pass

    def writeReturn(self, label: str) -> None:
        pass

    def close(self) -> None:
        pass