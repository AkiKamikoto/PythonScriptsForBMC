import pandas as pd
import sys

# Загрузка данных из Excel
file_path = sys.argv[1] # Путь до файла
column_name = sys.argv[2] # Название колонки где будет искать
# Чтение списка всех листов в Excel
excel_file = pd.ExcelFile(file_path, engine="openpyxl") 
sheet_names = excel_file.sheet_names  # Список всех листов в файле

all_emails = set()

# Проход по всем листам
for sheet in sheet_names:
    # Чтение данных с текущего листа
    emails = pd.read_excel(file_path, sheet_name=sheet, engine="openpyxl")

    
    # Проверяем, есть ли столбец с email (например, "email")
    if column_name in emails.columns:  # Или укажите имя столбца, в котором содержатся email
        email_list = emails[column_name].dropna().tolist()  # Извлекаем все email из столбца и игнорируем пустые значения
        all_emails.update(email_list)  # Добавляем email из текущего листа в общий список

# Форматирование email-адресов
formatted_emails = [f"'{email}'" for email in all_emails]
result = ", \n".join(formatted_emails)

# Сохранение в файл
with open("emails_array.txt", "w", encoding="utf-8") as file:
    file.write(result)

print("Готово! Результат сохранён в 'emails_array.txt'.")
print("Всего строк: ")
print(len(all_emails))
