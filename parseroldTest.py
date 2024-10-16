import unittest
from OAA.parserold import parse_command

class TestParseCommand(unittest.TestCase):
    #test create
    create_whitespaces_success = ["CREATE myCollection;",
                                  "    CREATE myCollection;",
                                  "    CREATE    myCollection;",
                                  "    CREATE      myCollection   ;     "
                                  ]
    create_whitespaces_success_result = [("CREATE", "myCollection")]
    create_whitespaces_fail = ["CREATE my Collection;",  # пробел в названии колекции
                               "CRE ATE myCollection;", # пробел в названии команды
                               ]
    
    create_semicolon_fail = ["CREATE myCollection", # без ;
                             "CREATE ;myCollection" # название коллекции вне команды
                             ] 
    create_semicolon_success = ["CREATE myColl;ection"]
    create_semicolon_success_result = [("CREATE", "myColl")]

    create_register_success = ["CREATE myCollection;", "CReaTE myCollECtion;", "create MyCollection;", "CREATE MYCOLLECTION;",]
    create_register_success_result = [("CREATE", "myCollection"), ("CReaTE", "myCollECtion"), ("create", "MyCollection"), ("CREATE", "MYCOLLECTION")]
    
    
    create_collection_name_fail = ["CREATE 45235myCollection;", 
                                   "CREATE my#Collection;", 
                                   "CREATE 'myCollection';",
                                   'CREATE "myCollection";',]

    #test insert 

    insert_whitespaces_success = ["INSERT myCollection \"document   about smth\";",
                                  "    INSERT myCollection \"document   about smth\";",
                                  "    INSERT    myCollection \"document about smth\";",
                                  "    INSERT      myCollection   \"document about smth\"     ;     "
                                  ]
    insert_whitespaces_success_result = [("INSERT", "myCollection", "document about smth")]
    insert_whitespaces_fail = ["CREATE my Collection;",  # пробел в названии колекции
                               "CRE ATE myCollection;", # пробел в названии команды
                               ]

    print_index_commands_whitespaces_success = []   
    print_index_commands_whitespaces_success_result = ()
    print_index_commands_whitespaces_fail = []

    search_match_commands_whitespaces_success = []   
    search_match_commands_whitespaces_success_result = ()
    search_match_commands_whitespaces_fail = []

    search_match_query_commands_whitespaces_success = []   
    search_match_query_commands_whitespaces_success_result = ()
    search_match_query_commands_whitespaces_fail = []

    semicolon_fail = ["CREATE myCollection", # без ;
                      "INSERT ;myCollection"] # название коллекции вне команды
    semicolon_success = ["CREATE myColl;ection", "INSERT gggg "]
    semicolon_success_result = [("CREATE", "myColl")]

    collection_name_fail = []

    different_register_success = []
    different_register_success_result = []




    def test_create_command_valid(self):
        command = "CREATE myCollection;"
        result = parse_command(command)
        self.assertEqual(result, ("CREATE", "myCollection"))

    def test_create_command_valid2(self):
        command = "CREATE myCollection ;"
        result = parse_command(command)
        self.assertEqual(result, ("CREATE", "myCollection"))
    
    def test_create_command_invalid(self):
        command = "CREATE 123InvalidCollection;"
        result = parse_command(command)
        self.assertIsNone(result)  # Expecting None for invalid identifier

    def test_insert_command_valid(self):
        command = 'INSERT myCollection "This is a test document";'
        result = parse_command(command)
        self.assertEqual(result, ("INSERT", "myCollection", "This is a test document"))
    
    def test_insert_command_invalid(self):
        command = 'INSERT myCollection This is a test document;'
        result = parse_command(command)
        self.assertIsNone(result)  # Expecting None for missing quotes around the document

    def test_print_index_command_valid(self):
        command = "PRINT_INDEX myCollection;"
        result = parse_command(command)
        self.assertEqual(result, ("PRINT_INDEX", "myCollection"))
    
    def test_print_index_command_invalid(self):
        command = "PRINT_INDEX;"
        result = parse_command(command)
        self.assertIsNone(result)  # Expecting None for missing collection name

    def test_search_command_valid_no_query(self):
        command = "SEARCH myCollection;"
        result = parse_command(command)
        self.assertEqual(result, ("Search", "myCollection", None))

    def test_search_command_valid_with_query(self):
        command = 'SEARCH myCollection WHERE keyword="test";'
        result = parse_command(command)
        self.assertEqual(result, ("Search", "myCollection", 'keyword="test"'))

    def test_search_command_invalid(self):
        command = "SEARCH ;"
        result = parse_command(command)
        self.assertIsNone(result)  # Expecting None for missing collection name

    def test_whitespace_handling(self):
        command = "  CREATE   myCollection  ; "
        result = parse_command(command)
        self.assertEqual(result, ("CREATE", "myCollection"))  # Should handle extra spaces

    def test_invalid_command(self):
        command = "DROP myCollection;"
        result = parse_command(command)
        self.assertIsNone(result)  # DROP is not a valid command in this context

if __name__ == '__main__':
    unittest.main()