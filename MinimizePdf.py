import os
import subprocess
import argparse

def compress_pdf(input_path, output_path, quality='screen'):
    """Сжимает один PDF-файл и выводит размеры до и после сжатия."""
    # Параметры качества для Ghostscript
    quality_settings = {
        'screen': '/screen',    # Наибольшее сжатие (низкое качество)
        'ebook': '/ebook',      # Среднее качество, хорошее для чтения
        'printer': '/printer',  # Высокое качество, хорошее для печати
        'prepress': '/prepress' # Максимальное качество для проф. печати
    }

    gs_quality = quality_settings.get(quality, '/screen')

    try:
        original_size = os.path.getsize(input_path)

        # Команда для вызова Ghostscript
        command = [
            'gs', '-sDEVICE=pdfwrite', f'-dPDFSETTINGS={gs_quality}',
            '-dNOPAUSE', '-dBATCH', '-dQUIET',
            f'-sOutputFile={output_path}', input_path
        ]

        # Запускаем Ghostscript через subprocess
        subprocess.run(command, check=True)

        compressed_size = os.path.getsize(output_path)
        # Выводим в консоль путь сохранения и размеры (в кб) до-после
        print(f"{input_path} успешно сжат. Размер до: {original_size / 1024:.2f} KB, после: {compressed_size / 1024:.2f} KB")
    except subprocess.CalledProcessError:
        print(f"Ошибка сжатия файла {input_path}")
    except Exception as e:
        print(f"Ошибка обработки файла {input_path}: {e}")

def compress_pdfs_recursively(input_folder, output_folder, quality='screen'):
    """Рекурсивно сжимает все PDF-файлы в папке и её подкаталогах."""
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                input_path = os.path.join(root, filename)

                # Создаём структуру папок в выходной директории
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_path = os.path.join(output_subfolder, f"compressed_{filename}")

                # Сжимаем PDF
                compress_pdf(input_path, output_path, quality)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для сжатия PDF. Укажите папку с PDF файлами или сам PDF файл."
    )
    parser.add_argument(
        "input_folder",
        type=str,
        help="Путь к папке с PDF файлами"
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        default=None,
        help="Путь к выходной папке (по умолчанию создается внутри input_folder)"
    )
    parser.add_argument(
        "--quality",
        type=str,
        choices=['screen', 'ebook', 'printer', 'prepress'],
        default='screen',
        help="Качество сжатия (по умолчанию screen)"
    )

    args = parser.parse_args()

    input_folder = args.input_folder
    output_folder = args.output_folder or os.path.join(input_folder, "compressed")

    compress_pdfs_recursively(input_folder, output_folder, quality=args.quality)
