import pandas as pd
import argparse

# Настройка аргументов командной строки
parser = argparse.ArgumentParser(
    description="Скрипт для извлечения уникальных email из всех листов Excel-файла. Для его запуска нужно указать 2 аргумента."
)
parser.add_argument(
    "file_path",
    type=str,
    help="Путь к Excel-файлу, из которого нужно извлечь email"
)
parser.add_argument(
    "column_name",
    type=str,
    help="Название столбца в файле Excel, содержащего email"
)

args = parser.parse_args()

file_path = args.file_path  
column_name = args.column_name  

# Чтение списка всех листов в Excel
excel_file = pd.ExcelFile(file_path, engine="openpyxl")
sheet_names = excel_file.sheet_names  # Список всех листов в файле

all_emails = set()

# Проход по всем листам
for sheet in sheet_names:
    # Чтение данных с текущего листа
    emails = pd.read_excel(file_path, sheet_name=sheet, engine="openpyxl")
    
    # Проверяем, есть ли столбец с email
    if column_name in emails.columns:
        email_list = emails[column_name].dropna().tolist()  
        all_emails.update(email_list)  

# Форматирование email-адресов
formatted_emails = [f"'{email}'" for email in all_emails]
result = ", \n".join(formatted_emails)

# Сохранение в файл
with open("emails_array.txt", "w", encoding="utf-8") as file:
    file.write(result)

print("Готово! Результат сохранён в 'emails_array.txt'.")
print(f"Всего строк: {len(all_emails)}")
