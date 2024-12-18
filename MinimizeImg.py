from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(
    description="Скрипт для сжатия картинок (.png, .jpg, .jpeg, .bmp, .gif). Укажите папку с изображениями и если необходимо преобразовать файл в другой формат, то укажите --format <необходимый формат>"
)
parser.add_argument(
    "input_folder",
    type=str,
    help="Путь к папке с изображениями"
)
parser.add_argument(
    "--format",
    type=str,
    choices=["png", "jpg", "jpeg", "bmp", "gif"],
    help="Формат для сохранения изображений. Если не указано, сохраняет в исходном формате."
)
args = parser.parse_args()

def compress_image(input_path, output_path, quality=85, format=None):
    """
    Сжимает изображение и сохраняет его с заданным качеством и форматом.
    
    :param input_path: Путь к исходному изображению.
    :param output_path: Путь, куда сохранить сжатое изображение.
    :param quality: Качество сжатого изображения (по умолчанию 85).
    :param format: Формат сохранения изображения (по умолчанию сохраняется в исходном формате).
    """
    try:
        print(f"Обработка: {input_path}")
        img = Image.open(input_path)

        # Преобразование изображения в RGB, если требуется
        if img.mode in ('RGBA', 'P'):  # RGBA или Indexed (P)
            img = img.convert('RGB')
            print(f"Конвертировано в RGB: {input_path}")

        # Определяем формат сохранения
        save_format = format.upper() if format else img.format
        if save_format == "JPG":  # Для совместимости с Pillow
            save_format = "JPEG"

        # Сжатие изображения и сохранение
        img.save(output_path, quality=quality, optimize=True, format=save_format)
        print(f"Сохранено: {output_path}")
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {e}")

def compress_images_recursively(input_folder, output_folder, quality=85, format=None):
    """
    Рекурсивно сжимает все изображения в указанной папке и её подкаталогах.
    :param input_folder: Путь к папке с исходными изображениями.
    :param output_folder: Путь к папке для сжатых изображений.
    :param quality: Качество сжатого изображения (по умолчанию 85).
    :param format: Формат сохранения изображений (по умолчанию сохраняется в исходном формате).
    """
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(root, filename)

                # Создаём структуру папок в выходной директории
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                base_filename, _ = os.path.splitext(filename)
                extension = f".{format}" if format else os.path.splitext(filename)[1]
                output_path = os.path.join(output_subfolder, f"{base_filename}{extension}")

                compress_image(input_path, output_path, quality, format)
            else:
                print(f"Пропущен файл (не изображение): {filename}")

if __name__ == "__main__":
    input_folder = args.input_folder
    output_folder = os.path.join(input_folder, "compressed")
    compress_images_recursively(input_folder, output_folder, quality=70, format=args.format)
