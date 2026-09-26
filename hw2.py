import os
import re
from collections import Counter

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
LIST_FILE = os.path.join(DATA_DIR, 'test_data_set.txt')

def read_corpus():

    if not os.path.exists(LIST_FILE):
        print(f"Помилка: не можу знайти файл {LIST_FILE}")
        return ""

    with open(LIST_FILE, 'r', encoding='utf-8') as f:
        filenames = [line.strip() for line in f if line.strip()]

    combined_text = ""
    loaded = 0

    for name in filenames:
        file_path = None
        for root, dirs, files in os.walk(DATA_DIR):
            if name in files:
                file_path = os.path.join(root, name)
                break
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as tf:
                    combined_text += "\n" + tf.read()
                    loaded += 1
            except Exception:
                pass

    print(f"Успішно завантажено файлів: {loaded} з {len(filenames)}")
    return combined_text

def get_words(text):
    return re.findall(r'[а-яіїєґ\']+', text.lower())

def total_words(text):
    return len(get_words(text))

def unique_words(text):
    return len(set(get_words(text)))

def get_shortest_words(text):
    words = list(set(get_words(text)))
    if not words: return []
    min_len = min(len(w) for w in words)
    return sorted(list(set(w for w in words if len(w) == min_len)))

def get_longest_words(text):
    words = list(set(get_words(text)))
    if not words: return []
    max_len = max(len(w) for w in words)
    return sorted(list(set(w for w in words if len(w) == max_len)))

def get_used_letters(text):
    letters = re.findall(r'[а-яіїєґ]', text.lower())
    return sorted(list(set(letters)))

def get_freq_dict(text):
    words = get_words(text)
    total = len(words)
    if total == 0: return []
    
    counts = Counter(words)
    sorted_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
 
    result = []
    for word, count in sorted_words:
        percent = (count / total) * 100
        result.append((word, percent))
    return result

if __name__ == "__main__":
    print("Працюємо з текстами...")
    corpus_text = read_corpus()
    
    if corpus_text.strip():
        print("\n" + "="*30)
        print("РЕЗУЛЬТАТИ АНАЛІЗУ:")
        print("="*30)
        print(f"1. Загальна кількість слів: {total_words(corpus_text)}")
        print(f"2. Кількість унікальних слів: {unique_words(corpus_text)}")
        print(f"3. Найкоротші слова: {get_shortest_words(corpus_text)}")
        print(f"4. Найдовші слова: {get_longest_words(corpus_text)}")
        print(f"5. Використані літери: {get_used_letters(corpus_text)}")
        
        print("\n6. Частотний словник (топ-10 слів у %):")
        freq_list = get_freq_dict(corpus_text)
        for word, p in freq_list[:10]:
            print(f"   {word}: {p:.2f}%")
        print("="*30)