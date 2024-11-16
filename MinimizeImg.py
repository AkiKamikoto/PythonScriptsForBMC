from PIL import Image
import sys
import os

def compress_image(input_path, output_path, quality=85):
    """
    Сжимает изображение и сохраняет его с заданным качеством.
    
    :param input_path: Путь к исходному изображению.
    :param output_path: Путь, куда сохранить сжатое изображение.
    :param quality: Качество сжатого изображения (по умолчанию 85).
    """
    try:
        # Открытие изображения
        img = Image.open(input_path)

        # Преобразование изображения в формат RGB, если оно в формате RGBA (например, с прозрачным фоном)
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Сжатие изображения и сохранение
        img.save(output_path, quality=quality, optimize=True)

        print(f"Изображение сохранено по пути: {output_path}")
    except Exception as e:
        print(f"Ошибка при обработке {input_path}: {e}")

def compress_images_in_folder(input_folder, output_folder, quality=85):

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
            compress_image(input_path, output_path, quality)

if __name__ == "__main__":
    input_folder = sys.argv[1]  # Папка с изображениями
    output_folder = f"{input_folder}/compressed"  # Папка для сжатых изображений

    compress_images_in_folder(input_folder, output_folder, quality=70)  # Устанавливаем желаемое качество
