class InvertedIndex:

    """Class for implementing an inverted index
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

        # Iterate over tokens and add them to the index
        for pos, token in enumerate(tokens):
            token = token.lower()  # Case insensitive
            if token not in self.index:
                self.index[token] = {}  # Initialize entry for the new token

            if doc_id not in self.index[token]:
                self.index[token][doc_id] = [] # Initialize the position list for the document
            self.index[token][doc_id].append(pos)

    def print_index(self):

        """Prints the index to the screen

        Example output:
            'apple': {1: [0, 5], 2: [1]}
            'banana': {1: [2]}
            'orange': {2: [3, 4]}
        """

        for word, doc_positions in self.index.items():
            print(f"'{word}': {doc_positions}")
    
    def search(self):

        """Returns all documents stored in the index"""

        all_docs = set()   

        # Iterate over all words in the index
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

        # Iterate over all words in the index
        for word in self.index:
            if keyword1 <= word <= keyword2:
                result_docs.update(self.index[word].keys())
        return list(result_docs)

    def search_distance(self, keyword1, keyword2, exact_distance):

        """Searches for documents where two words are separated by a specific distance"""
        
        keyword1, keyword2 = keyword1.lower(), keyword2.lower()
        result_docs = []

        # Check if both words exist in the index
        if keyword1 not in self.index or keyword2 not in self.index:
            return result_docs
        
        # Iterate over documents for the first word
        for doc_id in self.index[keyword1]:
            if doc_id in self.index[keyword2]:
                pos_word1 = self.index[keyword1][doc_id]
                pos_word2 = self.index[keyword2][doc_id]

                # Check if there are positions where the distance between the words is exactly equal to exact_distance
                if any(abs(p1 - p2) == exact_distance for p1 in pos_word1 for p2 in pos_word2):
                    result_docs.append(doc_id)

        return result_docs


class DB:

    """Class for managing collections of documents using the inverted index"""

    def __init__(self):

        # Dictionary for storing collections: {collection_name: InvertedIndex}
        self.collections = {}

    def create_collection(self, name):

        if name in self.collections:
            print(f"Collection '{name}' already exists.")
        else:
            self.collections[name] = InvertedIndex()
            print(f"Collection '{name}' created.")

    def insert_document(self, collection_name,text):

        if collection_name in self.collections:
            self.collections[collection_name].insert(text)
            print(f"Document added to collection '{collection_name}'.")
        else:
            print(f"Collection '{collection_name}' not found.")

    def print_index(self, collection_name): 

        if collection_name in self.collections:
            self.collections[collection_name].print_index()
        else:
            print(f"Collection '{collection_name}' not found.")
    
    def search(self, collection_name):

        if collection_name in self.collections:
            result = self.collections[collection_name].search()
            print(f"All documents in collection '{collection_name}': {result}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_word(self, collection_name, word):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_word(word)
            print(f"Search results: {result}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_range(self, collection_name, word1, word2):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_range(word1, word2)
            print(f"Search results: {result}")
        else:
            print(f"Collection '{collection_name}' not found.")

    def search_distance(self, collection_name, word1, word2, exact_dist):

        if collection_name in self.collections:
            result = self.collections[collection_name].search_distance(word1, word2, exact_dist)
            print(f"Search results: {result}")
        else:
            print(f"Collection '{collection_name}' not found.")

