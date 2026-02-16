import argparse
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

"""
Jack Analyzer
    - Takes as input a .vm file or folder of .vm files
    - Tokenizer parses the file(s) line by line
    - Analyzer compiles statements
    - Outputs the corresponding XML file
"""

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('dirOrFileName')
    arg = parser.parse_args()
    return arg.dirOrFileName


def main():
    dirOrFileName = parse_args()

    fileArr = []

    # If single file input
    if '.' in dirOrFileName:
        fileArr.append(dirOrFileName)

    # Else if directory of .jack files
    else:
        for root, dir, files in os.walk('./' + dirOrFileName):
            dirName = root.split('./')[1]
            print(dirName)
            for f in files:
                if '.jack' in f:
                    print(f)
                    filePath = dirName + '/' + f
                    fileArr.append(filePath)
    print(fileArr)

    for filePath in fileArr:
        tokenizer = JackTokenizer(filePath)
        try:
            CompilationEngine(tokenizer, filePath)
        except RuntimeError as error:
            print(error)
            return

            
if __name__ == '__main__':
    main()