import re

valid_identifier = r'[a-zA-Z][a-zA-Z0-9_]*'

def parse_command(command):
    # Видаляємо зайві пробіли
    command = re.sub(r'[ \t\r\n]+', ' ', command.strip()) # удаляет внутри строки
    command = re.sub(r' \;', ';', command)
    print("Так виглядає команда післа видалення зайвих пробілів:", command)
    
    # checking if not exist for create and exist for others should be implementing in functions that actually do it

    # CREATE command
    create_match = re.match(r'CREATE (' + valid_identifier + r');.*', command, re.IGNORECASE)
    if create_match:
        collection_name = create_match.group(1)

        print(f"Collection {collection_name} is trying to be created")

        return ("CREATE", collection_name)

    # INSERT command
    insert_match = re.match(r'INSERT (' + valid_identifier + r') "(.*?)";.*', command, re.IGNORECASE)
    if insert_match:

        collection_name = insert_match.group(1)
        document = insert_match.group(2)

        print(f"Document {document} is trying to be inserted into collection {collection_name}")

        return ("INSERT", collection_name, document)

    # PRINT_INDEX command
    print_index_match = re.match(r'PRINT_INDEX (' + valid_identifier + r');.*', command, re.IGNORECASE)
    if print_index_match:

        collection_name = print_index_match.group(1)

        print(f"Index of collection {collection_name} is trying to be printed")

        return ("PRINT_INDEX", collection_name)
    
    # SEARCH command
    search_match = re.match(r'SEARCH (' + valid_identifier + r')( WHERE (.+))?;', command, re.IGNORECASE)
    if search_match:
    
        collection_name = search_match.group(1)
        query = search_match.group(3)

        if query:
            print(f"Searching in {collection_name} with query: {query} is trying to happen")
        else:
            print(f"Searching all documents in {collection_name} is trying to happen")

        return ("Search", collection_name, query)

    print("Invalid command")