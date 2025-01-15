import zipfile
import os
import argparse
from PIL import Image
from io import BytesIO
import shutil


def compress_image(image_path, quality=85):
    """
    Сжать изображение до указанного качества.
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert('RGB')
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=quality, optimize=True)
            buffer.seek(0)
            with open(image_path, "wb") as f:
                f.write(buffer.read())
    except Exception as e:
        print(f"Ошибка при сжатии изображения {image_path}: {e}")


def optimize_docx(input_path, output_path):
    """
    Оптимизирует .docx файл, сжимая изображения.
    """
    temp_dir = "temp_docx"
    
    # Очистка и создание временной папки
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    try:
        # Распаковка .docx как zip-архива
        with zipfile.ZipFile(input_path, 'r') as docx:
            docx.extractall(temp_dir)

        # Обработка изображений
        for root, _, files in os.walk(temp_dir):
            for file in files:
                if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
                    img_path = os.path.join(root, file)
                    compress_image(img_path)

        # Сборка нового .docx файла
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as docx_out:
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    archive_name = os.path.relpath(full_path, temp_dir)
                    docx_out.write(full_path, archive_name)

        print(f"Файл успешно оптимизирован: {output_path}")
    except Exception as e:
        print(f"Ошибка при обработке файла {input_path}: {e}")
    finally:
        # Очистка временной папки
        shutil.rmtree(temp_dir)


def optimize_docx_in_folder(input_folder, output_folder):
    """
    Оптимизировать все .docx файлы в папке.
    """
    if not os.path.exists(input_folder):
        print(f"Папка {input_folder} не существует.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.docx'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            try:
                optimize_docx(input_path, output_path)
            except Exception as e:
                print(f"Ошибка при обработке {filename}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для сжатия изображений внутри .docx файлов в указанной папке."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Путь к папке, где хранятся .docx файлы"
    )
    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = os.path.join(input_folder, "compressed")
    
    optimize_docx_in_folder(input_folder, output_folder)