from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser(
    description="Скрипт для сжатия картинок (.png, .jpg, .jpeg, .bmp, .gif). Укажите файл или папку с изображениями и, если необходимо преобразовать файл в другой формат, укажите --format <необходимый формат>"
)
parser.add_argument(
    "input_path",
    type=str,
    help="Путь к файлу или папке с изображениями"
)
parser.add_argument(
    "--format",
    type=str,
    choices=["png", "jpg", "jpeg", "bmp", "gif"],
    help="Формат для сохранения изображений. Если не указано, сохраняет в исходном формате."
)
parser.add_argument(
    "--resize",
    type=int,
    default=None,
    help="Максимальная длина стороны изображения (если указано, изображения будут уменьшены)."
)
args = parser.parse_args()

def compress_image(input_path, output_path, quality=30, format=None, resize=None):
    """
    Сжимает изображение и сохраняет его с заданным качеством, форматом и размером.
    
    :param input_path: Путь к исходному изображению.
    :param output_path: Путь, куда сохранить сжатое изображение.
    :param quality: Качество сжатого изображения (по умолчанию 30).
    :param format: Формат сохранения изображения (по умолчанию сохраняется в исходном формате).
    :param resize: Максимальная длина стороны изображения (если указано).
    """
    try:
        img = Image.open(input_path)

        # Уменьшение размеров изображения
        if resize:
            img.thumbnail((resize, resize))

        # Преобразование изображения в RGB, если требуется
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        save_format = format.upper() if format else img.format
        if save_format == "JPG":
            save_format = "JPEG"

        img.save(output_path, quality=quality, optimize=True, format=save_format)
        original_size = os.path.getsize(input_path) / 1024
        compressed_size = os.path.getsize(output_path) / 1024
        print(f"{input_path} -> {output_path} | До: {original_size:.2f} KB, После: {compressed_size:.2f} KB")
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {e}")

def compress_images_recursively(input_folder, output_folder, quality=30, format=None, resize=None):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)
                base_filename, _ = os.path.splitext(filename)
                extension = f".{format}" if format else os.path.splitext(filename)[1]
                output_path = os.path.join(output_subfolder, f"{base_filename}{extension}")
                compress_image(input_path, output_path, quality, format, resize)
            else:
                print(f"Пропущен файл (не изображение): {filename}")

if __name__ == "__main__":
    input_path = args.input_path
    if os.path.isfile(input_path):
        output_folder = os.path.join(os.path.dirname(input_path), "compressed")
        os.makedirs(output_folder, exist_ok=True)
        base_filename, _ = os.path.splitext(os.path.basename(input_path))
        extension = f".{args.format}" if args.format else os.path.splitext(input_path)[1]
        output_path = os.path.join(output_folder, f"{base_filename}{extension}")
        compress_image(input_path, output_path, quality=30, format=args.format, resize=args.resize)
    elif os.path.isdir(input_path):
        output_folder = os.path.join(input_path, "compressed")
        compress_images_recursively(input_path, output_folder, quality=30, format=args.format, resize=args.resize)
    else:
        print("Указанный путь не является файлом или папкой.")