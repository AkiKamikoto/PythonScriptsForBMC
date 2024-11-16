import sys
from pdf2docx import Converter

def convertToDockx(inputPdf, outputDocx):
    


    cv = Converter(inputPdf)
    cv.convert(outputDocx)  # Конвертация
    cv.close()

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = f"{input_file}/compressed"

    convertToDockx(input_file, output_file)