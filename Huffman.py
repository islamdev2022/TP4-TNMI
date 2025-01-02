import heapq
from collections import Counter
import math

class Node:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

def calculate_frequencies(text):
    freq_count = Counter(text)
    total_chars = len(text)
    chars = []
    frequencies = []
    
    for char, count in freq_count.items():
        chars.append(char)
        frequencies.append(count / total_chars)
    
    return chars, frequencies

def calculate_entropy(frequencies):
    # H(X) = -Σ p(x) * log2(p(x))
    return -sum(p * math.log2(p) for p in frequencies if p > 0)

def calculate_compression_metrics(text, huffman_codes, frequencies):
    # Original size (8 bits per character in ASCII)
    original_size = len(text) * 8
    
    # Compressed size (sum of code lengths * frequency * text length)
    compressed_size = sum(len(code) * freq * len(text) 
                         for (char, code), freq in zip(huffman_codes.items(), frequencies))
    
    # Calculate coding table size in bits
    # For each character: 8 bits (ASCII) + code length bits
    table_size = sum(8 + len(code) for code in huffman_codes.values())
    
    # Calculate compression ratios
    compression_ratio = original_size / compressed_size
    compression_ratio_with_table = original_size / (compressed_size + table_size)
    
    # Calculate average code length
    avg_code_length = sum(len(code) * freq for (char, code), freq in zip(huffman_codes.items(), frequencies))
    
    return {
        'original_size': original_size,
        'compressed_size': compressed_size,
        'table_size': table_size,
        'compression_ratio': compression_ratio,
        'compression_ratio_with_table': compression_ratio_with_table,
        'avg_code_length': avg_code_length
    }
    
def build_huffman_tree(chars, freq):
    priority_queue = [Node(char, f) for char, f in zip(chars, freq)]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left_child = heapq.heappop(priority_queue)
        right_child = heapq.heappop(priority_queue)
        merged_node = Node(frequency=left_child.frequency + right_child.frequency)
        merged_node.left = left_child
        merged_node.right = right_child
        heapq.heappush(priority_queue, merged_node)
    
    return priority_queue[0]

def generate_huffman_codes(node, code="", huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}
    
    if node is not None:
        if node.symbol is not None:
            huffman_codes[node.symbol] = code
        generate_huffman_codes(node.left, code + "1", huffman_codes)
        generate_huffman_codes(node.right, code + "0", huffman_codes)
    return huffman_codes

def huffman_encode(text):
    # Calculate frequencies from the input text
    chars, freq = calculate_frequencies(text)
    
    # Calculate entropy
    entropy = calculate_entropy(freq)
    
    # Build the Huffman tree
    root = build_huffman_tree(chars, freq)
    
    # Generate Huffman codes
    huffman_codes = generate_huffman_codes(root)
    
    # Calculate compression metrics
    metrics = calculate_compression_metrics(text, huffman_codes, freq)
    
    # Print detailed analysis
    print("\n=== Huffman Coding Analysis ===")
    
    print("\nCharacter Frequencies:")
    for char, frequency in zip(chars, freq):
        print(f"{char}: {frequency:.4f}")
    
    print("\nHuffman Codes:")
    for char, code in huffman_codes.items():
        print(f"Character: {char}, Code: {code}")
    
    print("\nCompression Metrics:")
    print(f"Entropy: {entropy:.4f} bits")
    print(f"Average Code Length: {metrics['avg_code_length']:.4f} bits")
    print(f"Original Size: {metrics['original_size']} bits")
    print(f"Compressed Size: {metrics['compressed_size']:.0f} bits")
    print(f"Coding Table Size: {metrics['table_size']} bits")
    print(f"Compression Ratio (without table): {metrics['compression_ratio']:.2f}")
    print(f"Compression Ratio (with table): {metrics['compression_ratio_with_table']:.2f}")
    
    # Encode the text
    encoded = "".join(huffman_codes[char] for char in text)
    print(f"\nEncoded text: {encoded}")
    
    return encoded, huffman_codes

def huffman_decode(encoded_text, huffman_codes):
    reverse_mapping = {code: char for char, code in huffman_codes.items()}
    decoded = ""
    current_code = ""
    
    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_mapping:
            decoded += reverse_mapping[current_code]
            current_code = ""
    
    return decoded

if __name__ == "__main__":
    # Get input from user
    text = input("Enter text to encode: ")
    
    # Encode the text and get analysis
    encoded, codes = huffman_encode(text)
    
    # Decode the text
    decoded = huffman_decode(encoded, codes)
    
    # Verify decoding
    print(f"\nDecoded text: {decoded}")
    print(f"Successful decode: {text == decoded}")