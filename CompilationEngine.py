import argparse
import os
from JackTokenizer import JackTokenizer

"""
Compliation Engine
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
    isDirectory = False
    outputFileName = ''

    if '.' in dirOrFileName:
        outputFileName = dirOrFileName.split('.')[0]
        fileArr.append(dirOrFileName)
    
    else:
        isDirectory = True
        outputFileName = dirOrFileName
        for root, dir, files in os.walk("./" + dirOrFileName):
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
        if len(tokenizer.lines) == 0:
            print('File empty. Nothing to translate')
            return

        while tokenizer.hasMoreTokens():
            tokenizer.advance()

if __name__ == '__main__':
    main()