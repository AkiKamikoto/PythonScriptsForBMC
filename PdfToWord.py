import argparse
import os
from pdf2docx import Converter

def convert_to_docx(input_pdf, output_docx):
    """
    Конвертирует PDF-файл в DOCX.

    :param input_pdf: Путь к входному PDF-файлу.
    :param output_docx: Путь для сохранения выходного DOCX-файла.
    """
    try:
        print(f"Конвертация: {input_pdf} -> {output_docx}")
        cv = Converter(input_pdf)
        cv.convert(output_docx)  # Конвертация
        cv.close()
        print(f"Успешно: {output_docx}")
    except Exception as e:
        print(f"Ошибка при конвертации {input_pdf}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для конвертации PDF в DOCX. Укажите файл или папку с PDF-файлами."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Путь к папке с PDF файлами или к одному PDF файлу."
    )
    args = parser.parse_args()

    input_path = args.input_folder

    if os.path.isfile(input_path) and input_path.lower().endswith(".pdf"):
        # Если указан одиночный файл
        output_file = os.path.splitext(input_path)[0] + ".docx"
        convert_to_docx(input_path, output_file)
    elif os.path.isdir(input_path):
        # Если указана папка, конвертируем все PDF-файлы
        output_folder = os.path.join(input_path, "converted")
        os.makedirs(output_folder, exist_ok=True)

        for filename in os.listdir(input_path):
            if filename.lower().endswith(".pdf"):
                input_pdf = os.path.join(input_path, filename)
                output_docx = os.path.join(output_folder, os.path.splitext(filename)[0] + ".docx")
                convert_to_docx(input_pdf, output_docx)
    else:
        print("Указан неверный путь. Проверьте, что это файл PDF или папка с PDF-файлами.")
