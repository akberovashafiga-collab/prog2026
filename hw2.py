import os
import re
from collections import Counter

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(DATA_DIR, 'test_data_set.txt')

def read_corpus_files():
    all_text = ""
    
    if not os.path.exists(LIST_FILE):
        print(f"Помилка: не знайдено файл {LIST_FILE}")
        return ""

    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        filenames = [line.strip() for line in f if line.strip()]

    success_count = 0
    for filename in filenames:
        # Шукаємо файл у підпапках (good, bad, so-so тощо)
        file_path = None
        for root, dirs, files in os.walk(DATA_DIR):
            if filename in files:
                file_path = os.path.join(root, filename)
                break
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as tf:
                    all_text += "\n" + tf.read()
                    success_count += 1
            except Exception:
                pass

    print(f"Успішно завантажено файлів: {success_count} із {len(filenames)}")
    return all_text

def get_clean_words(text):
    return re.findall(r'[а-яіїєґ\']+', text.lower())

def frequency_dict_percentage(text):
    words = get_clean_words(text)
    total = len(words)
    if total == 0: return {}
    counts = Counter(words)
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return {w: (c / total) * 100 for w, c in sorted_counts}

def shortest_words(text):
    words = list(set(get_clean_words(text)))
    if not words: return []
    min_l = min(len(w) for w in words)
    return sorted(list(set([w for w in words if len(w) == min_l])))

def longest_words(text):
    words = list(set(get_clean_words(text)))
    if not words: return []
    max_l = max(len(w) for w in words)
    return sorted(list(set([w for w in words if len(w) == max_l])))

def count_unique_words(text):
    return len(set(get_clean_words(text)))

def count_total_words(text):
    return len(get_clean_words(text))

def used_letters(text):
    letters = re.findall(r'[а-яіїєґ]', text.lower())
    return sorted(list(set(letters)))

def most_frequent_letter(text):
    letters = re.findall(r'[а-яіїєґ]', text.lower())
    if not letters: return None
    counts = Counter(letters)
    max_c = max(counts.values())
    return [char for char, cnt in counts.items() if cnt == max_c]

if __name__ == "__main__":
    print("Обробка текстів...")
    text = read_corpus_files()
    
    if text.strip():
        print("\n" + "=" * 40)
        print("РЕЗУЛЬТАТИ АНАЛІЗУ:")
        print("=" * 40)
        print(f"1. Загальна кількість слів: {count_total_words(text)}")
        print(f"2. Кількість унікальних слів: {count_unique_words(text)}")
        print(f"3. Найкоротші слова: {shortest_words(text)}")
        print(f"4. Найдовші слова: {longest_words(text)}")
        print(f"5. Найчастіша літера: {most_frequent_letter(text)}")
        print(f"6. Використані літери: {used_letters(text)}")
        
        freq = frequency_dict_percentage(text)
        print(f"\n7. Частотний словник у % (перші 10 слів):")
        freq = frequency_dict_percentage(text)
        print(f"\n7. Частотний словник у % (перші 10 слів):")
        # Ось тут правильно перетворюємо на список ПЕРЕД зрізом [:10]:
        freq_items = list(freq.items())
        for word, percentage in freq_items[:10]:
            print(f"   '{word}': {percentage:.2f}%")
        print("=" * 40)
