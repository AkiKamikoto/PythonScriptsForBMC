import os
import pypandoc
import sys

def convert_word_to_pdf(input_folder, output_folder):
    for filename in os.listdir(input_folder):
        if filename.endswith('.docx'):
            input_path = os.path.join(input_folder, filename)
            output_filename = os.path.splitext(filename)[0] + '.pdf'
            output_path = os.path.join(output_folder, output_filename)
            
            # Конвертация файла .docx в .pdf
            try:
                pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
                print(f"Файл {filename} успешно конвертирован в PDF.")
            except Exception as e:
                print(f"Ошибка при конвертации {filename}: {e}")

if __name__ == "__main__":
    input_folder = sys.argv[1]
    output_folder = f"{input_folder}/converted"

    convert_word_to_pdf(input_folder, output_folder)
    print("Конвертация завершена.")
