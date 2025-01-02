import math
from collections import Counter

# Node class for Shannon-Fano encoding
class node:
    def __init__(self):
        self.sym = ''  # Symbol
        self.pro = 0.0  # Probability
        self.arr = [0] * 20  # Code array
        self.top = 0

# Function to perform Shannon-Fano encoding
def shannon(l, h, p):
    if l >= h:
        return
    pack1 = sum(p[i].pro for i in range(l, h))
    pack2 = p[h].pro
    diff1 = abs(pack1 - pack2)
    
    j = h - 1
    while j > l:
        pack1 -= p[j].pro
        pack2 += p[j].pro
        diff2 = abs(pack1 - pack2)
        if diff2 >= diff1:
            break
        diff1 = diff2
        j -= 1

    for i in range(l, j + 1):
        p[i].top += 1
        p[i].arr[p[i].top] = 1

    for i in range(j + 1, h + 1):
        p[i].top += 1
        p[i].arr[p[i].top] = 0

    shannon(l, j, p)
    shannon(j + 1, h, p)

# Function to calculate entropy
def calculate_entropy(p):
    return -sum(node.pro * math.log2(node.pro) for node in p if node.pro > 0)

# Function to calculate compressed size
def calculate_compressed_size(p, total_length):
    return sum((node.top + 1) * node.pro * total_length for node in p)

# Function to calculate coding table size
def calculate_table_size(p):
    return sum(len(node.sym) * 8 + (node.top + 1) for node in p)

# Function to sort symbols by probability
def sortByProbability(p):
    p.sort(key=lambda node: node.pro)

# Function to decode Shannon-Fano encoded message
def decode_shannon_fano(coded_message, code_dict):
    decoded_message = ""
    buffer = ""
    inverse_code_dict = {v: k for k, v in code_dict.items()}

    for bit in coded_message:
        buffer += bit
        if buffer in inverse_code_dict:
            decoded_message += inverse_code_dict[buffer]
            buffer = ""
    return decoded_message

# Encapsulate complete Shannon-Fano workflow
def process_shannon_fano(test_word):
    # Calculate frequencies
    frequency = Counter(test_word)
    total_length = len(test_word)

    # Create nodes for each symbol
    p = [node() for _ in range(len(frequency))]
    for i, (char, freq) in enumerate(frequency.items()):
        p[i].sym = char
        p[i].pro = freq / total_length

    # Sort nodes by probability
    sortByProbability(p)

    # Perform Shannon-Fano encoding
    for i in range(len(p)):
        p[i].top = -1
    shannon(0, len(p) - 1, p)


    # Create a dictionary for symbol-to-code mapping
    code_dict = {n.sym: ''.join(map(str, n.arr[:n.top + 1])) for n in p}

    # Encode the message
    coded_message = ''.join(code_dict[char] for char in test_word)

    # Decode the message to verify correctness
    decoded_message = decode_shannon_fano(coded_message, code_dict)

    # Calculate metrics
    avg_code_length = sum(len(code_dict[char]) * freq / total_length for char, freq in frequency.items())
    entropy = calculate_entropy(p)
    original_size = total_length * 8  # ASCII uses 8 bits per character
    compressed_size = calculate_compressed_size(p, total_length)
    table_size = calculate_table_size(p)
    compression_rate = (compressed_size / original_size) * 100
    compression_rate_with_table = ((compressed_size + table_size) / original_size) * 100

    # Return all results as a dictionary
    return {
        "coded_message": coded_message,
        "decoded_message": decoded_message,
        "avg_code_length": round(avg_code_length, 2),
        "entropy": round(entropy, 2),
        "original_size": original_size,
        "compressed_size": round(compressed_size, 2),
        "compression_rate": round(100 - compression_rate, 2),
        "compression_rate_with_table": round(100 - compression_rate_with_table, 2),
        "successful_decode": test_word == decoded_message,
    }


# # Main program
# if __name__ == "__main__":
#     print("Enter the test word: ", end="")
#     test_word = input().strip()

#     # Calculate frequencies
#     frequency = Counter(test_word)
#     total_length = len(test_word)

#     # Create nodes for each symbol
#     p = [node() for _ in range(len(frequency))]
#     for i, (char, freq) in enumerate(frequency.items()):
#         p[i].sym = char
#         p[i].pro = freq / total_length

#     # Sort nodes by probability
#     sortByProbability(p)

#     # Perform Shannon-Fano encoding
#     for i in range(len(p)):
#         p[i].top = -1
#     shannon(0, len(p) - 1, p)

#     # Display results
#     display(len(p), p)

#     # Calculate metrics
#     entropy = calculate_entropy(p)
#     compressed_size = calculate_compressed_size(p, total_length)
#     table_size = calculate_table_size(p)
#     original_size = total_length * 8  # ASCII uses 8 bits per character

#     # Compression rates
#     compression_rate = (compressed_size / original_size) * 100
#     compression_rate_with_table = ((compressed_size + table_size) / original_size) * 100

#     # Print metrics
#     print("\nEntropy of the message: H(X) =", round(entropy, 2), "bits/symbol")
#     print("Compressed size (Shannon-Fano):", round(compressed_size, 2), "bits")
#     print("Compression rate (Shannon-Fano):", round(100 - compression_rate, 2), "%")
#     print("Compression rate (with table):", round(100 - compression_rate_with_table, 2), "%")
