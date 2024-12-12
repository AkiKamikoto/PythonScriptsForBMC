import zipfile
import os
import argparse
from PIL import Image
from io import BytesIO
from docx import Document

# Настройка аргументов командной строки
parser = argparse.ArgumentParser(
    description="Скрипт для сжатия docx/word файлов. Для его запуска нужно указать 1 аргумент."
)
parser.add_argument(
    "input_docx",
    type=str,
    help="Путь к папке где хранятся word файлы"
)

args = parser.parse_args()

def compress_image(image_path, output_path, quality=85):
    """
    Сжать изображение до указанного качества.
    """
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img.save(output_path, format='JPEG', quality=quality, optimize=True)

def optimize_docx(input_path, output_path):
    """
    Оптимизирует .docx файл, сжимая изображения.
    """
    # Временная папка для извлечения содержимого .docx
    temp_dir = "temp_docx"
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)
    os.mkdir(temp_dir)

    # Открытие .docx файла как zip-архива
    with zipfile.ZipFile(input_path, 'r') as docx:
        docx.extractall(temp_dir)

    # Обработка всех изображений в директории с содержимым .docx
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                img_path = os.path.join(root, file)
                compressed_img_path = img_path + "_compressed.jpg"
                compress_image(img_path, compressed_img_path)
                
                # Заменить оригинальное изображение на сжатое
                os.replace(compressed_img_path, img_path)

    # Создание нового .docx файла с оптимизированными изображениями
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_out:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                docx_out.write(os.path.join(root, file),
                               os.path.relpath(os.path.join(root, file), temp_dir))

    # Удалить временную директорию
    for root, dirs, files in os.walk(temp_dir, topdown=False):
        for file in files:
            os.remove(os.path.join(root, file))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    os.rmdir(temp_dir)

    print(f"Файл успешно оптимизирован и сохранен как: {output_path}")


def optimize_docx_in_folder(input_folder, output_folder):

    # Проверяем, существует ли папка для вывода
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    # Проходим по всем файлам в папке
        for filename in os.listdir(input_folder):
            input_path = os.path.join(input_folder, filename)
        
        # Проверяем, является ли файл изображением (по расширению)
        if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
            output_path = os.path.join(output_folder, filename)

            # Сжимаем изображение
            optimize_docx(input_path, output_path)


if __name__ == "__main__":
    input_docx = args.input_docx
    output_docx = f"{input_docx}/compressed"
    optimize_docx_in_folder(input_docx, output_docx)
