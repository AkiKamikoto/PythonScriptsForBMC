import sys
from pdf2docx import Converter

def convertToDockx(inputPdf, outputDocx):
    


    cv = Converter(inputPdf)
    cv.convert(outputDocx)  # Конвертация
    cv.close()

if __name__ == "__main__":
    input = sys.argv[1]
    output = sys.argv[2]

    convertToDockx(input, output)