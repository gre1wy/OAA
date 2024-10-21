class InvertedIndex:

    """Клас для реалізації інвертованого індексу"""

    def __init__(self):

        # Словник: {слово: {document_id: [позії]}}
        self.index = {}
        self.next_doc_id = 1  # Ініціалізація лічильника ідентифікаторів документу

    def insert(self, tokens):

        # Генерація ідентифікатора документу
        doc_id = self.next_doc_id
        self.next_doc_id += 1  

        # Перебір токенів та додавання їх у індекс
        for pos, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {}  # Ініціалізація запису для нового токена

            if doc_id not in self.index[token]:
                self.index[token][doc_id] = [] # Ініціалізація списку позицій для документа
            self.index[token][doc_id].append(pos)

    def print_index(self):

        """Виводить індекс на екран"""

        for word, doc_positions in self.index.items():
            print(f"'{word}': {doc_positions}")
    
    def search(self):

        """ Повертає всі документи, які зберігаються в індексі"""

        all_docs = set()   

        # Перебір усіх слів у індексі
        for word_docs in self.index.values():
            all_docs.update(word_docs.keys())
        return list(all_docs)

    def search_word(self, word):
    
        """ Пошук документів за конкретним словом """

        return list(self.index.get(word, {}).keys())

    def search_range(self, keyword1, keyword2):
        
        """ Пошук документів, які містять слова в заданому діапазоні """

        result_docs = set()

        # Перебір усіх слів в індексі
        for word in self.index:
            if keyword1 <= word <= keyword2:
                result_docs.update(self.index[word].keys())
        return list(result_docs)

    def search_distance(self, keyword1, keyword2, exact_distance):

        """ Пошук документів, де keyword1 і keyword2 знаходяться на відстані точно рівною exact_distance """

        result_docs = []

        # Перевірка наявності обох слів в індексі
        if keyword1 not in self.index or keyword2 not in self.index:
            return result_docs
        
        # Перебір документів для першого слова
        for doc_id in self.index[keyword1]:
            if doc_id in self.index[keyword2]:
                pos_word1 = self.index[keyword1][doc_id]
                pos_word2 = self.index[keyword2][doc_id]

                # Перевіряємо, чи є позиції, де відстань між словами точно рівна exact_distance
                if any(abs(p1 - p2) == exact_distance for p1 in pos_word1 for p2 in pos_word2):
                    result_docs.append(doc_id)

        return result_docs


class DB:

    """Клас для управління колекціями документів"""

    def __init__(self):
        
        # Словник для збереження колекцій: {collection_name: InvertedIndex}
        self.collections = {}

    def create_collection(self, name):

        if name in self.collections:
            print(f"Колекція '{name}' вже існує.")
        else:
            self.collections[name] = InvertedIndex()
            print(f"Колекція '{name}' створена.")

    def insert_document(self, collection_name,text):

        if collection_name in self.collections:
            self.collections[collection_name].insert(text)
            print(f"Документ добавлений в колекцію. '{collection_name}'.")
        else:
            print(f"Колекція '{collection_name}' не знайдена.")

    def print_index(self, collection_name): 

        if collection_name in self.collections:
            self.collections[collection_name].print_index()
        else:
            print(f"Колекція '{collection_name}' не знайдена.")
    
    def search(self, collection_name):

        if collection_name in self.collections:
            result = self.collections[collection_name].search()
            print(f"Всі документи в колекції '{collection_name}': {result}")
        else:
            print(f"Колекція '{collection_name}' не знайдена.")

    def search_word(self, collection_name, word):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_word(word)
            print(f"Результати пошуку: {result}")
        else:
            print(f"Колекція '{collection_name}' не знайдена.")

    def search_range(self, collection_name, word1, word2):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_range(word1, word2)
            print(f"Результати пошуку: {result}")
        else:
            print(f"Колекція '{collection_name}' не знайдена.")

    def search_distance(self, collection_name, word1, word2, exact_dist):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_distance(word1, word2, exact_dist)
            print(f"Результати пошуку: {result}")
        else:
            print(f"Колекція'{collection_name}' не знайдена.")

