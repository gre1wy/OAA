class InvertedIndex:
    def __init__(self):
        # Словарь: {слово: {document_id: [позиции]}}
        self.index = {}
        self.next_doc_id = 1  # Инициализация счетчика идентификаторов документов

    def insert(self, doc_id, tokens):
        # Генерация идентификатора документа
        doc_id = self.next_doc_id
        self.next_doc_id += 1  # Увеличение идентификатора для следующего документа

        for pos, token in enumerate(tokens):
            if token not in self.index:
                self.index[token] = {}
            if doc_id not in self.index[token]:
                self.index[token][doc_id] = []
            self.index[token][doc_id].append(pos)

    def print_index(self):
        for word, doc_positions in self.index.items():
            print(f"'{word}': {doc_positions}")

    def search_word(self, word):
        # Поиск документов с конкретным словом
        return list(self.index.get(word, {}).keys())

    def search_range(self, keyword1, keyword2):
        # Поиск документов, содержащих слова в заданном диапазоне
        result_docs = set()
        for word in self.index:
            if keyword1 <= word <= keyword2:
                result_docs.update(self.index[word].keys())
        return list(result_docs)

    def search_distance(self, keyword1, keyword2, max_distance):
        # Поиск документов, где keyword1 и keyword2 находятся на расстоянии не более max_distance
        result_docs = []
        if keyword1 not in self.index or keyword2 not in self.index:
            return result_docs

        for doc_id in self.index[keyword1]:
            if doc_id in self.index[keyword2]:
                pos_word1 = self.index[keyword1][doc_id]
                pos_word2 = self.index[keyword2][doc_id]
                if any(abs(p1 - p2) <= max_distance for p1 in pos_word1 for p2 in pos_word2):
                    result_docs.append(doc_id)

        return result_docs


class DB:
    def __init__(self):
        # Словарь для хранения коллекций: {collection_name: InvertedIndex}
        self.collections = {}

    def create_collection(self, name):
        if name in self.collections:
            print(f"Коллекция '{name}' уже существует.")
        else:
            self.collections[name] = InvertedIndex()
            print(f"Коллекция '{name}' создана.")

    def insert_document(self, collection_name, doc_id, text):
        if collection_name in self.collections:
            self.collections[collection_name].insert(doc_id, text)
            print(f"Документ {doc_id} добавлен в коллекцию '{collection_name}'.")
        else:
            print(f"Коллекция '{collection_name}' не найдена.")

    def print_index(self, collection_name):
        if collection_name in self.collections:
            self.collections[collection_name].print_index()
        else:
            print(f"Коллекция '{collection_name}' не найдена.")

    def search(self, collection_name, word1, word2=None, distance=None):
        if collection_name in self.collections:
            result = self.collections[collection_name].search_where(word1, word2, distance)
            print(f"Результаты поиска: {result}")
        else:
            print(f"Коллекция '{collection_name}' не найдена.")

