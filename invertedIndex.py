class InvertedIndex:

    """
    Class for implementing an inverted index.
    This structure maps words to document IDs and their positions within those documents.
    """

    def __init__(self):

        # Dictionary: {word: {document_id: [positions]}}
        self.index = {}
        # Counter to assign unique IDs to each document
        self.next_doc_id = 1  

    def insert(self, tokens):

        if not tokens or not isinstance(tokens, list):
            raise ValueError("Invalid input: 'tokens' must be a non-empty list of words.")
        
        # Generate the document ID
        doc_id = self.next_doc_id
        self.next_doc_id += 1  

        for pos, token in enumerate(tokens):
            token = token.lower()  # Case insensitive
            if token not in self.index:
                self.index[token] = {}  # Initialize entry for the new token

            if doc_id not in self.index[token]:
                self.index[token][doc_id] = [] # Initialize the position list for the document
            self.index[token][doc_id].append(pos)

    def print_index(self):

        """Prints the index to the screen"""

        for word, doc_positions in self.index.items():
            print(f"'{word}': {doc_positions}")
    
    def search(self):

        """Returns all documents stored in the index"""

        all_docs = set()   
        for word_docs in self.index.values():
            all_docs.update(word_docs.keys())
        return list(all_docs)

    def search_word(self, word):
    
        """Search for documents by a specific word"""

        word = word.lower()
        return list(self.index.get(word, {}).keys())

    def search_range(self, keyword1, keyword2):
        
        """Search for documents that contain words in the specified range"""

        keyword1, keyword2 = keyword1.lower(), keyword2.lower()
        result_docs = set()

        for word in self.index:
            if keyword1 <= word <= keyword2:
                result_docs.update(self.index[word].keys())
        return list(result_docs)

    def search_distance(self, keyword1, keyword2, exact_distance):

        """Searches for documents where two words are separated by a specific distance"""
        
        keyword1, keyword2 = keyword1.lower(), keyword2.lower()
        result_docs = []

        if keyword1 not in self.index or keyword2 not in self.index:
            return result_docs
        
        for doc_id in self.index[keyword1]:
            if doc_id in self.index[keyword2]:
                pos_word1 = self.index[keyword1][doc_id]
                pos_word2 = self.index[keyword2][doc_id]

                if any(abs(p1 - p2) == exact_distance for p1 in pos_word1 for p2 in pos_word2):
                    result_docs.append(doc_id)

        return result_docs

class FullDocuments:
    """Class for storing and retrieving full documents"""

    def __init__(self):
        # Dictionary: {document_id: document(str)}
        self.full_text = {}

    def add_document(self, doc_id, document):
        """Adds a document to the storage"""
        self.full_text[doc_id] = ' '.join(document)

    def get_document(self, doc_id):
        """Retrieves a document by its ID"""
        return self.full_text.get(doc_id)

    def get_all_documents(self):
        """Retrieves all documents in the storage"""
        return self.full_text

    def search_word(self, word):
        """Search for full documents containing a specific word"""
        word = word.lower()
        result = []
        for doc_id, document in self.full_text.items():
            if word in document.lower().split():
                result.append(document)
        return result

    def search_range(self, keyword1, keyword2):
        """Search for full documents containing words in a specific range"""
        keyword1, keyword2 = keyword1.lower(), keyword2.lower()
        result = []
        for doc_id, document in self.full_text.items():
            words = set(document.lower().split())
            if any(keyword1 <= word <= keyword2 for word in words):
                result.append(document)
        return result

    def search_distance(self, keyword1, keyword2, exact_distance):
        """Search for full documents where two words are separated by a specific distance"""
        keyword1, keyword2 = keyword1.lower(), keyword2.lower()
        result = []
        for doc_id, document in self.full_text.items():
            words = document.lower().split()
            positions1 = [i for i, word in enumerate(words) if word == keyword1]
            positions2 = [i for i, word in enumerate(words) if word == keyword2]
            if any(abs(p1 - p2) == exact_distance for p1 in positions1 for p2 in positions2):
                result.append(document)
        return result



class DB:
    """Class for managing collections of documents"""

    def __init__(self):
        # Dictionary for storing collections: {collection_name: (InvertedIndex, FullDocuments)}
        self.collections = {}

    def create_collection(self, name):
        if name in self.collections:
            print(f"Collection '{name}' already exists.")
        else:
            self.collections[name] = (InvertedIndex(), FullDocuments())
            print(f"Collection '{name}' created.")

    def insert_document(self, collection_name, document):
        if collection_name in self.collections:
            inverted_index, full_documents = self.collections[collection_name]

            doc_id = inverted_index.next_doc_id
            full_documents.add_document(doc_id, document)

            inverted_index.insert(document)
            print(f"Document added to collection '{collection_name}' with ID {doc_id}.")
        else:
            print(f"Collection '{collection_name}' not found.")

    def print_index(self, collection_name):
        if collection_name in self.collections:
            inverted_index, _ = self.collections[collection_name]
            inverted_index.print_index()
        else:
            print(f"Collection '{collection_name}' not found.")

    def search(self, collection_name):
        if collection_name in self.collections:
            inverted_index, full_documents = self.collections[collection_name]
            doc_ids = inverted_index.search()
            documents = [full_documents.get_document(doc_id) for doc_id in doc_ids]
            print(f"All documents in collection '{collection_name}': {documents}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_word(self, collection_name, word):
        if collection_name in self.collections:
            inverted_index, full_documents = self.collections[collection_name]
            doc_ids = inverted_index.search_word(word)
            documents = [full_documents.get_document(doc_id) for doc_id in doc_ids]
            print(f"Search results: {documents}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_range(self, collection_name, word1, word2):
        if collection_name in self.collections:
            inverted_index, full_documents = self.collections[collection_name]
            doc_ids = inverted_index.search_range(word1, word2)
            documents = [full_documents.get_document(doc_id) for doc_id in doc_ids]
            print(f"Search results: {documents}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_distance(self, collection_name, word1, word2, exact_dist):
        if collection_name in self.collections:
            inverted_index, full_documents = self.collections[collection_name]
            doc_ids = inverted_index.search_distance(word1, word2, exact_dist)
            documents = [full_documents.get_document(doc_id) for doc_id in doc_ids]
            print(f"Search results: {documents}")
        else:
            print(f"Collection '{collection_name}' not found.")
