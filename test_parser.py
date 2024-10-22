import unittest
from unittest.mock import MagicMock
from lexer import Token, Lexer
from parser import Parser
from invertedIndex import DB

class TestParser(unittest.TestCase):
    def setUp(self):

        """Set up test fixtures before each test method"""

        self.db = MagicMock(spec=DB)
        
    def create_parser_with_input(self, input_text):

        """Helper method to create a parser with input text"""

        lexer = Lexer(input_text)
        return Parser(lexer, self.db)

    def test_parse_create(self):

        """Test parsing CREATE command"""
        
        parser = self.create_parser_with_input('CREATE test_collection;')
        
        # Execute parse_create
        collection_name = parser.parse_create()
        
        # Assert the correct collection name was returned
        self.assertEqual(collection_name, 'test_collection')

    def test_parse_insert(self):
        """Test parsing INSERT command"""
        parser = self.create_parser_with_input('INSERT test_collection "hello world";')
        
        # Execute parse_insert
        collection_name, document = parser.parse_insert()
        
        # Assert the correct values were returned
        self.assertEqual(collection_name, 'test_collection')
        self.assertEqual(document, ['hello', 'world'])

    def test_parse_print_index(self):
        """Test parsing PRINT_INDEX command"""
        parser = self.create_parser_with_input('PRINT_INDEX test_collection;')
        
        # Execute parse_print_index
        collection_name = parser.parse_print_index()
        
        # Assert the correct collection name was returned
        self.assertEqual(collection_name, 'test_collection')

    def test_parse_search_simple(self):
        """Test parsing simple SEARCH command"""
        parser = self.create_parser_with_input('SEARCH test_collection;')
        
        # Execute parse_search
        collection_name, word1, word2, dist = parser.parse_search()
        
        # Assert the correct values were returned
        self.assertEqual(collection_name, 'test_collection')
        self.assertIsNone(word1)
        self.assertIsNone(word2)
        self.assertIsNone(dist)

    def test_parse_search_with_word(self):
        """Test parsing SEARCH command with WHERE clause"""
        parser = self.create_parser_with_input('SEARCH test_collection WHERE "test";')
        
        # Execute parse_search
        collection_name, word1, word2, dist = parser.parse_search()
        
        # Assert the correct values were returned
        self.assertEqual(collection_name, 'test_collection')
        self.assertEqual(word1, 'test')
        self.assertIsNone(word2)
        self.assertIsNone(dist)

    def test_parse_search_with_range(self):
        """Test parsing SEARCH command with range"""
        parser = self.create_parser_with_input('SEARCH test_collection WHERE "apple" - "zebra";')
        
        # Execute parse_search
        collection_name, word1, word2, dist = parser.parse_search()
        
        # Assert the correct values were returned
        self.assertEqual(collection_name, 'test_collection')
        self.assertEqual(word1, 'apple')
        self.assertEqual(word2, 'zebra')
        self.assertIsNone(dist)

    def test_parse_search_with_distance(self):
        """Test parsing SEARCH command with distance"""
        parser = self.create_parser_with_input('SEARCH test_collection WHERE "first" <3> "second";')
        
        # Execute parse_search
        collection_name, word1, word2, dist = parser.parse_search()
        
        # Assert the correct values were returned
        self.assertEqual(collection_name, 'test_collection')
        self.assertEqual(word1, 'first')
        self.assertEqual(word2, 'second')
        self.assertEqual(dist, 3)

    def test_invalid_syntax(self):
        """Test parser error handling with invalid syntax"""
        parser = self.create_parser_with_input('CREATE;')  # Missing collection name
        
        # Assert that invalid syntax raises an exception
        with self.assertRaises(Exception):
            parser.parse_create()

    def test_auto_parse_create(self):
        """Test auto_parse with CREATE command"""
        parser = self.create_parser_with_input('CREATE test_collection;')
        
        # Execute auto_parse
        parser.auto_parse()
        
        # Verify that create_collection was called on the DB
        self.db.create_collection.assert_called_once_with('test_collection')

if __name__ == '__main__':
    unittest.main()