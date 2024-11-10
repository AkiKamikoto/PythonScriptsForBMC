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
    # Открытие изображения
    img = Image.open(input_path)

    # Преобразование изображения в формат RGB, если оно в формате RGBA (например, с прозрачным фоном)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    # Сжатие изображения и сохранение
    img.save(output_path, quality=quality, optimize=True)

    print(f"Изображение сохранено по пути: {output_path}")

# Пример использования
input_image_path = sys.argv[1]  # Замените на путь к вашему изображению
output_image_path = sys.argv[2]  # Замените на путь для сохранения сжатого изображения

compress_image(input_image_path, output_image_path, quality=70)  # Установите желаемое качество
