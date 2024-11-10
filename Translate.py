from googletrans import Translator, LANGUAGES

def translate_word(word, source_language, target_languages):
    """
    Переводит слово с одного языка на несколько других.

    :param word: Слово для перевода.
    :param source_language: Язык исходного слова (например, 'ru', 'kk').
    :param target_languages: Список языков для перевода (например, ['en', 'kk']).
    :return: Слово на других языках.
    """
    translator = Translator()
    translations = {}

    for target_language in target_languages:
        try:
            translated = translator.translate(word, src=source_language, dest=target_language)
            translations[target_language] = translated.text
        except Exception as e:
            translations[target_language] = f"Ошибка перевода: {e}"
    
    return translations

def main():
    print("Добро пожаловать в переводчик!")
    print("Для завершения работы нажмите Ctrl + C (или Cmd + C на macOS).")
    
    while True:
        # Запрашиваем слово с указанием языка
        user_input = input("Введите слово и его язык (например, 'привет ru'): ")
        
        if user_input.lower() == "выход":
            print("Завершение работы.")
            break
        
        try:
            parts = user_input.rsplit(" ", 1)
            if parts[1] == 'ру':
                source_language = 'ru'
            # Разделяем введенную строку на части
            else:
                  # Разделение по последнему пробелу
                source_language = parts[1].lower()
            word = parts[0]


              # Приводим язык к нижнему регистру
        except IndexError:
            print("Ошибка! Пожалуйста, введите слово и язык через пробел.")
            continue
        
        # Проверка, существует ли исходный язык в доступных языках
        if source_language not in LANGUAGES:
            print(f"Неверный язык: {source_language}. Пожалуйста, используйте правильный код языка.")
            continue
        
        # Запрашиваем целевые языки, если они не указаны
        target_languages_input = input("Введите целевые языки через запятую (например, 'en,kk' для перевода на английский и казахский), или нажмите Enter для автоматического перевода на английский и казахский: ")
        
        if target_languages_input.strip() == "":  # Если не введены целевые языки, по умолчанию переводим на английский и казахский
            target_languages = ['en', 'kk']
        else:
            target_languages = target_languages_input.lower().split(',')
        
        # Проверка на корректность целевых языков
        invalid_languages = [lang for lang in target_languages if lang not in LANGUAGES]
        if invalid_languages:
            print(f"Некорректные языки: {', '.join(invalid_languages)}. Пожалуйста, используйте правильные коды языков.")
            continue
        
        # Переводим слово на указанные языки
        translations = translate_word(word, source_language, target_languages)

        # Выводим результат
        for lang, translation in translations.items():
            print(f"{lang.upper()}: {translation}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nЗавершение работы программы.")
