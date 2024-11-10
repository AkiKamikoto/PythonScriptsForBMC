import zipfile
import os
import sys
from PIL import Image
from io import BytesIO
from docx import Document

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

# Пример использования
input_docx = sys.argv[1]
output_docx = sys.argv[2]
optimize_docx(input_docx, output_docx)
