import json, timeit

# Establish a Global Dictionary to store the encoding information for faster recall
encode_dict = {}


class Huffnode:
    """
    Establish a Huffnode Class, where a node contains:
        weight - the number of counts seen by the character(s) it is root of
        character - the character value
        left - the node to the left
        right - the node to the right
    """

    def __init__(huff, weight, character, left, right):
        huff.weight = weight
        huff.character = character
        huff.left = left
        huff.right = right


def BuildHuffmanCodeTree(alpha, counts):
    """This function will build a huffman encoding tree

    Args:
        alpha (list): contains characters in alphabet
        counts (str): corresponds to alpha containing frequency of the alphabet

    Returns:
         (Huffnode): the node of the root of the Greedy Huffman tree
    """
    # First, we will convert the alphabet adn associated into a node list
    # The node list is sorted based on the characters count (lowest being at front)
    node_list = make_node_list(alpha, counts)

    # We will work through the node list until only one node remains
    # To note, the last node will be our root
    while len(node_list) > 1:
        # Remove the two smallest nodes; as the list is sorted, each will be at the front
        # Since pop assigns the value and removes the item, both times will index at the first spot (i.e. 0)
        small_1 = node_list.pop(0)
        small_2 = node_list.pop(0)

        # Create a new Huffnode by merging their values
        new_node = Huffnode(small_1.weight + small_2.weight, None, small_1, small_2)

        # Add the new node back to the node list and sort
        node_list.append(new_node)
        node_list.sort(key=lambda x: x.weight)

    # Return the final remaining node, which is our tree root
    return node_list[0]


def make_node_list(alpha, counts):
    """Makes a sorted list of nodes based on inputs

    Args:
        alpha (list): contains characters in alphabet
        counts (str): corresponds to alpha containing frequency of the alphabet

    Returns:
        (list): sorted Huffnodes, where the first node is the character with the lowest count frequency
    """
    # Create a Huffnode for each charcter (based on its value and count) and add to a list
    node_list = [Huffnode(counts[i], alpha[i], None, None) for i in range(len(alpha))]

    # Sort and return the list
    node_list.sort(key=lambda x: x.weight)
    return node_list


def encode(tree_root, text):
    """This function will encode a message, given the root to a Huffman tree

    Args:
        tree_root (Huffnode): the root to a Greedy Huffman tree
        text (str): the message to be encoded

    Returns:
        (str): the encoded message
    """
    # Call on a helper function to read the Huffman tree and make an encoding dictionary
    # Make sure global dictionary is clean
    encode_dict.clear()
    add_encodings(tree_root, "")

    # Initialize the encoding
    encoding = ""

    # For each character in the message, access its respective encoding value and add to the encoded message
    for letter in text:
        encoding += (encode_dict[letter])

    # Return the encoded message
    return encoding


def encode_slow(tree_root, text):
    """This function will encode a message, given the root to a Huffman tree, without a look-up table

        Args:
            tree_root (Huffnode): the root to a Greedy Huffman tree
            text (str): the message to be encoded

        Returns:
            (str): the encoded message
    """
    # Initialize the encoding
    encoding = ""

    # For each character in the message, call the helper function to get the path in the Huffman Tree
    # Add the path to the growing encoding
    for letter in text:
        encoding += find_path(tree_root, letter, "")

    return encoding


def find_path(node, letter, path):
    """
    A recursive function that will find the path in a Huffman Tree from the root to a given character
    Left is considered a 0, Right is considered a 1
    All characters will be at a leaf and somewhere in the tree, due to the nature of the Huffman Tree creation

    Args:
        node (Huffnode): the node of the tree to check; the initial node in the first call is considered the root
        letter (str): the character to find
        path (str): a growing path the represents the current path from the initial root to the current node

    Returns:
        (str): the path from the initial root to the node holding the desired character
    """
    # When we reach a leaf, we must determine if it is the correct letter
    if node.left is None and node.right is None:

        # Path is returned if the character is correct, otherwise we return None
        if node.character == letter:
            return path
        return

    # If we are not at a leaf, we will keep traversing the tree
    # As we traverse, we will update the path (0 for left, 1 for right) and make the recursive call in that direction
    else:
        left = find_path(node.left, letter, path + str(0))

        # If left holds a value, then the correct path was found and we will continue returning it up
        if left is not None:
            return left

        right = find_path(node.right, letter, path + str(1))

        # If right holds a value, then the correct path was found and we will continue returning it up
        if right is not None:
            return right


def add_encodings(node, path):
    """This function will take a Huffnode and travel to its leaves. Along this traversal,
    it will add to the global encode_dict. Specifically, it will add characters and the path to it from the root.
    Note that left is denoted by a 0, while right is denoted by a 1. This function works recursively,
    and the path begins at the initially called node

    Args:
        node (Huffnode): the root of the tree to be traveled
        path (str): the current path from the initial node to the current node

    Returns:
        Empty Value (function purpose is to add to global dictionary)
    """
    # If we are at a Null pointer, return to continue through other nodes until finished
    if node is None:
        return

    # If we are at a leaf, add the character and path to dictionary
    if node.left is None and node.right is None:
        encode_dict[node.character] = path

    # If we are not at a leaf, update the path (0 for left, 1 for right) and make the recursive call in that direction
    else:
        add_encodings(node.left, path + str(0))
        add_encodings(node.right, path + str(1))


def decode(tree_root, encoding):
    """This function will decode a message based on its encoding and a given Greedy Huffman tree

    Args:
        tree_root (Huffnode): the root to a Greedy Huffman tree
        encoding (str): the message to be decoded, must be encoded by given Huffman tree

    Returns:
        (str): the decoded message
    """
    # Initialize the output message and set the current node to the root of the Huffman tree
    output = ""
    curr = tree_root

    # We will travel the encoding 1 bit (or character) at a time
    for bit in encoding:

        # If the bit is 0, go left; otherwise, go right
        if bit == "0":
            curr = curr.left
        else:
            curr = curr.right

        # If we have reached a leaf, then add the corresponding value to the output
        if curr.left is None and curr.right is None:
            output += curr.character

            # We must reset the current tree, as we are now starting over and looking for a new charcter
            curr = tree_root

    # Return the decoded message
    return output


def test_compression(frequency_json, message_txt):
    """
    This function will take in the json file for alphabet and counts,
    returning the length of the encoded message txt file

    Args:
        frequncy_json(str): json file of the counts and alphabet
        message_txt(str): txt file of the message to be encoded

    Returns:
        (int): length of encoded message
    """
    # Open the frequency_json and load into dictonary
    f = open(frequency_json)
    freq_dict = json.load(f)

    # Convert dictionary into necessary input for BuildHuffmanCodeTree
    alpha = []
    counts = []
    for key in freq_dict:
        alpha.append(key)
        counts.append(freq_dict[key])

    # Build the Huffman Tree
    tree_root = BuildHuffmanCodeTree(alpha, counts)

    # Open and prepare the message
    message_file = open(message_txt)
    message = message_file.readline()
    message_file.close()

    # Get the encoding and return its length, as well as print useful information
    encoding = encode(tree_root, message)
    print_helper4(alpha, counts, len(encoding))
    return len(encoding)


def print_helper4(alpha, counts, bits):
    """Will print important information regarding question 4

    Args:
        alpha (list): the characters in the alphabet
        counts (list): frequency of each character in alpha
        bits (int): the number of bits in the encoding
    """
    # Report unique characters
    print("There are " + str(len(alpha)) + " characters in the alphabet")

    # Set up total counter, find the total, report the total
    total = 0
    for int in counts:
        total += int
    print("There are " + str(total) + " characters in the message")

    # Report the bits needed to encode
    print("It will take " + str(bits) + " bits to encode the message")


def freq_det(txt, lookup):
    """This function will create a frequency dictionary, and then subsequent lists for use to Build a Huffman Tree,
    encode a message with that tree (both with and without a lookup table) and decode it

    Args:
        txt (str): containing the desired text file to build the Huffman tree adn encode
        lookup (Boolean): True is lookup table, False is no lookup table

    Returns:
        (int): the length of the encoding"""

    # Initialize the frequency dictionary and empty message
    freq_dict = {}
    message = ""

    # Read through the text, adding to the message string and creating a dictionary
    # The dictionary key is a character and the value is the counts
    # https://stackoverflow.com/questions/2988211/how-to-read-a-single-character-at-a-time-from-a-file-in-python
    with open(txt) as f:
        while True:
            letter = f.read(1)
            message += letter
            if letter not in freq_dict:
                freq_dict[letter] = 1
            else:
                freq_dict[letter] += 1
            if not letter:
                break
    f.close()

    # Convert dictionary into necessary input (Alpha and Count as lists) for BuildHuffmanCodeTree
    alpha = []
    counts = []
    for key in freq_dict:
        alpha.append(key)
        counts.append(freq_dict[key])

    # Create the Greedy Huffman tree
    tree_root = BuildHuffmanCodeTree(alpha, counts)

    # Encode the Message (based on whether a lookup table is used), time the step and report the time
    if lookup:
        start_fast = timeit.default_timer()
        encoding = encode(tree_root, message)
        end_fast = timeit.default_timer()
        print("The lookup table encoding took " + str(end_fast - start_fast) + " seconds")

    else:
        start_slow = timeit.default_timer()
        encoding = encode_slow(tree_root, message)
        end_slow = timeit.default_timer()
        print("The encoding without lookup table took " + str(end_slow - start_slow) + " seconds")

    # Decode the message, time the step adn report the time
    start_decode = timeit.default_timer()
    decode(tree_root, encoding)
    end_decode = timeit.default_timer()
    print("The decoding took " + str(end_decode - start_decode) + " seconds")

    # Determine and remove the most common character
    max_char_counts = max(counts)
    max_char = alpha[counts.index(max(counts))]
    print("The most common character is \"" + max_char + "\", which has " + str(max_char_counts) + " appearances.")

    # Report other information on the Huffman Compression and return the length of the encoding
    print_helper4(alpha, counts, len(encoding))
    return len(encoding)


if __name__ == '__main__':
    """To run the functions"""
    print("Message 1: \n")
    test_compression("Frequency1.json", "Message1.txt")
    print("\n")
    print("Message 2: \n")
    test_compression("Frequency2.json", "Message2.txt")
    print("\n")
    print("Fast Encoding: \n")
    freq_det("TaleOfTwoCities.txt", True)
    print("\n")
    print("Slow Encoding: \n")
    freq_det("TaleOfTwoCities.txt", False)
