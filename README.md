# Algorithm Analysis Foundations

# Text Collection Management System

## Overview

This is a console-based program that allows users to manage a collection of text documents and perform efficient full-text search using an inverted index data structure

## Features

The program supports the following commands:

1. **CREATE `<collection_name>;`** - Creates a new collection with the specified name.
2. **INSERT `<collection_name> "<document>";`** - Adds a new document to the specified collection.
3. **PRINT_INDEX `<collection_name>;`** - Prints the internal structure of the inverted index built for the specified collection.
4. **SEARCH `<collection_name> [WHERE <query>];`** - Searches for documents in the specified collection that match the given query. The query can be:
    - `"<keyword>"` - Finds documents containing the specified keyword.
    - `"<keyword_1>" - "<keyword_2>"` - Finds documents containing any word between `<keyword_1>` and `<keyword_2>` (inclusive).
    - `"<keyword_1>" <N> "<keyword_2>"` - Finds documents where `<keyword_1>` and `<keyword_2>` are exactly `N` words apart, regardless of their positions and order.

## Implementation Details

The program is implemented using the following components:

1. **Lexer (`lexer.py`)**: Responsible for tokenizing the input text into a sequence of tokens (e.g., keywords, identifiers, quoted strings).
2. **Parser (`parser.py`)**: Parses the sequence of tokens and executes the corresponding commands.
3. **Inverted Index (`invertedIndex.py`)**: Implements the inverted index data structure, which maps words to the documents they appear in and their positions within those documents.
4. **Database (`invertedIndex.py`)**: Manages the collections of documents and their associated inverted indexes.
5. **Main Entry Point (`main.py`)**: Provides the command-line interface and coordinates the interaction between the other components.

## Usage
...
## Error Handling

The program is designed to detect and handle various error situations, such as:

- Incorrect syntax of commands
- Attempting to create a collection with a name that is already in use
- Attempting to execute a command on a non-existent collection

When an error occurs, the program will output an appropriate error message to the user.


