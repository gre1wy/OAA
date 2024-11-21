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

1. Clone the repository:

```

## Error Handling

The program is designed to detect and handle various error situations, such as:

- Incorrect syntax of commands
- Attempting to create a collection with a name that is already in use
- Attempting to execute a command on a non-existent collection
- Providing an insufficient number of values for the `INSERT` command in variants with a relational data model
- Attempting to retrieve non-existent columns in a table using the `SELECT` command in variants with a relational data model

When an error occurs, the program will output an appropriate error message to the user.

## Time and Space Complexity Analysis

The time and space complexity of the implemented algorithms have been analyzed and the following insights can be provided:

- **Insertion of documents into the inverted index**: The time complexity is O(n * m), where n is the number of unique words in the document and m is the number of positions (occurrences) of each word. The space complexity is O(n * m), as the inverted index stores the mapping of words to their positions in each document.
- **Searching for documents**: The time complexity depends on the type of search query:
    - Searching for a single keyword: O(k + d), where k is the number of occurrences of the keyword and d is the number of documents containing the keyword.
    - Searching for a range of keywords: O(k + d), where k is the number of unique keywords in the range and d is the number of documents containing at least one of the keywords in the range.
    - Searching for keywords within a distance: O(k1 * k2 + d), where k1 and k2 are the number of occurrences of the two keywords, and d is the number of documents containing both keywords within the specified distance.
- **Printing the inverted index**: The time complexity is O(k * d), where k is the number of unique words in the index and d is the number of documents containing each word.

## Future Improvements

1. **Handling larger documents**: The current implementation assumes that documents can be entirely loaded into memory. For handling larger documents, the program could be modified to process the documents in smaller chunks or use external storage (e.g., files, databases) to store the inverted index.
2. **Advanced search features**: The program could be extended to support more sophisticated search features, such as:
    - Ranking and scoring of search results based on various factors (e.g., term frequency, inverse document frequency)
    - Stemming and lemmatization to improve search accuracy
    - Handling of synonyms and related terms
3. **Improved user experience**: The program could be enhanced with a more user-friendly command-line interface, including features like autocompletion, command history, and better error reporting.
4. **Persistence and concurrency**: The program could be extended to support persistent storage of the inverted index and collections, allowing for data to be retained between program runs. Additionally, mechanisms for handling concurrent access to the collections could be implemented.
5. **Distributed and scalable architecture**: For larger-scale deployments, the program could be designed to run in a distributed environment, leveraging techniques like sharding, replication, and load balancing to improve scalability and fault tolerance.
