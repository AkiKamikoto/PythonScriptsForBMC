import os
import subprocess
import sys

def compress_pdf(input_folder, output_folder=None, quality='screen'):
    # Если выходная папка не указана, использовать ту же папку
    output_folder = output_folder or input_folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Параметры качества для Ghostscript
    quality_settings = {
        'screen': '/screen',    # Наибольшее сжатие (низкое качество)
        'ebook': '/ebook',      # Среднее качество, хорошее для чтения
        'printer': '/printer',  # Высокое качество, хорошее для печати
        'prepress': '/prepress' # Максимальное качество для проф. печати
    }
    
    gs_quality = quality_settings.get(quality, '/screen')
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"compressed_{filename}")

            # Команда для вызова Ghostscript
            command = [
                'gs', '-sDEVICE=pdfwrite', f'-dPDFSETTINGS={gs_quality}',
                '-dNOPAUSE', '-dBATCH', '-dQUIET',
                f'-sOutputFile={output_path}', input_path
            ]
            
            # Запускаем Ghostscript через subprocess
            try:
                subprocess.run(command, check=True)
                print(f"{filename} успешно сжат и сохранен как {output_path}")
            except subprocess.CalledProcessError:
                print(f"Ошибка сжатия файла {filename}")


def compress_pdf_in_folder(input_folder, output_folder, quality="screen"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Проходим по всем файлам в папке
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # Проверяем, является ли файл pdf 
        if filename.lower().endswith(('pdf')):
            output_path = os.path.join(output_folder, filename)

            # Сжимаем pdf
            compress_pdf(input_path, output_path, quality='screen')
if __name__ == "__main__":
    input_folder = sys.argv1[1] # Укажите папку с PDF файлами
    output_folder = f"{input_folder}/compressed"

    compress_pdf_in_folder(input_folder, output_folder, quality='screen')  # screen, ebook, printer, prepress
