# Huffman Encoding/Decoding - Python

This code implements the Huffman compression and decompression algorithm to compress a text file, and also prints relevant statistics regarding how effective the compression was.

A Huffnode class was created so that objects of HuffNode type could be made.

## Huffnode class:

Establish a Huffnode Class, where a node contains:
- weight - the number of counts seen by the character(s) it is root of
- character - the character value
- left - the node to the left
- right - the node to the right

## BuildHuffmanCodeTree(alpha, counts)
This function will build a huffman encoding tree
- Args: 
  - alpha (list): contains characters in alphabet
  - counts (str): corresponds to alpha containing frequency of the alphabet
- Returns:
  - (Huffnode): the node of the root of the Greedy Huffman tree
  
## make_node_list(alpha, counts)
Makes a sorted list of nodes based on inputs

- Args:
  - alpha (list): contains characters in alphabet
  - counts (str): corresponds to alpha containing frequency of the alphabet

- Returns:
  - (list): sorted Huffnodes, where the first node is the character with the lowest count frequency
  
## encode(tree_root, text)
This function will encode a message, given the root to a Huffman tree

- Args:
    - tree_root (Huffnode): the root to a Greedy Huffman tree
    - text (str): the message to be encoded

- Returns:
    - (str): the encoded message
    
## encode_slow(tree_root, text)
This function will encode a message, given the root to a Huffman tree, without a look-up table

- Args:
    - tree_root (Huffnode): the root to a Greedy Huffman tree
    - text (str): the message to be encoded

- Returns:
    - (str): the encoded message

## find_path(node, letter, path)
A recursive function that will find the path in a Huffman Tree from the root to a given character
Left is considered a 0, Right is considered a 1
All characters will be at a leaf and somewhere in the tree, due to the nature of the Huffman Tree creation

- Args:
  - node (Huffnode): the node of the tree to check; the initial node in the first call is considered the root
  - letter (str): the character to find
  - path (str): a growing path the represents the current path from the initial root to the current node

- Returns:
  - (str): the path from the initial root to the node holding the desired character
  
## add_encodings(node, path)
This function will take a Huffnode and travel to its leaves. Along this traversal,
it will add to the global encode_dict. Specifically, it will add characters and the path to it from the root.
Note that left is denoted by a 0, while right is denoted by a 1. This function works recursively,
and the path begins at the initially called node

- Args:
    - node (Huffnode): the root of the tree to be traveled
    - path (str): the current path from the initial node to the current node

- Returns:
    - Empty Value (function purpose is to add to global dictionary)
    
## decode(tree_root, encoding)
This function will decode a message based on its encoding and a given Greedy Huffman tree

- Args:
  - tree_root (Huffnode): the root to a Greedy Huffman tree
  - encoding (str): the message to be decoded, must be encoded by given Huffman tree

- Returns:
  - (str): the decoded message

## test_compression(frequency_json, message_txt)
This function will take in the json file for alphabet and counts,
returning the length of the encoded message txt file

- Args:
    - frequncy_json(str): json file of the counts and alphabet
    - message_txt(str): txt file of the message to be encoded

- Returns:
    - (int): length of encoded message

## freq_det(txt, lookup)
This function will create a frequency dictionary, and then subsequent lists for use to Build a Huffman Tree,
encode a message with that tree (both with and without a lookup table) and decode it

- Args:
    - txt (str): containing the desired text file to build the Huffman tree adn encode
    - lookup (Boolean): True is lookup table, False is no lookup table

Returns:
    - (int): the length of the encoding
