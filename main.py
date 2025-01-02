from Shanon_Fano import process_shannon_fano
from Huffman import process_huffman_encoding
from collections import Counter
import math

def calculate_theoretical_entropy(text):
    total_chars = len(text)
    frequencies = Counter(text)
    entropy = 0
    
    for freq in frequencies.items():
        probability = freq / total_chars
        entropy -= probability * math.log2(probability)
    
    return entropy

def execute_shannon_fano(test_word):
    results = process_shannon_fano(test_word)
    entropy = calculate_theoretical_entropy(test_word)
    
    return {
        **results,
        "theoretical_entropy": entropy,
        "entropy_efficiency": results["avg_code_length"] / entropy if entropy != 0 else 0
    }

def execute_huffman(test_word):
    results = process_huffman_encoding(test_word)
    entropy = calculate_theoretical_entropy(test_word)
    
    return {
        **results,
        "theoretical_entropy": entropy,
        "entropy_efficiency": results["avg_code_length"] / entropy if entropy != 0 else 0
    }

def letter_count(text):
    return dict(Counter(text))

def compare_performance(test_word):
    shannon_fano_results = execute_shannon_fano(test_word)
    huffman_results = execute_huffman(test_word)
    
    print("\nAnalysis Results:")
    print("-" * 70)
    
    metrics = [
        ("Letter Frequencies", letter_count(test_word)),
        ("Theoretical Entropy (bits/symbol)", 
         [shannon_fano_results["theoretical_entropy"], 
          huffman_results["theoretical_entropy"]]),
        ("Average Code Length (bits/symbol)", 
         [shannon_fano_results["avg_code_length"], 
          huffman_results["avg_code_length"]]),
        ("Entropy Efficiency", 
         [shannon_fano_results["entropy_efficiency"], 
          huffman_results["entropy_efficiency"]]),
        ("Compression Rate without Table (%)", 
         [shannon_fano_results["compression_rate"], 
          huffman_results["compression_ratio"]]),
        ("Compression Rate with Table (%)", 
         [shannon_fano_results["compression_rate_with_table"], 
          huffman_results["compression_ratio_with_table"]]),
        ("Original Size (bits)", 
         [shannon_fano_results["original_size"], 
          huffman_results["original_size"]]),
        ("Compressed Size (bits)", 
         [shannon_fano_results["compressed_size"], 
          huffman_results["compressed_size"]])
    ]
    
    for metric, values in metrics:
        if isinstance(values, dict):
            print(f"\n{metric}:")
            for k, v in values.items():
                print(f"{k}: {v}")
        else:
            print(f"\n{metric}:")
            print(f"Shannon-Fano: {values[0]:.4f}")
            print(f"Huffman: {values[1]:.4f}")
    
    print("\nEncoded Messages:")
    print(f"Shannon-Fano: {shannon_fano_results['coded_message']}")
    print(f"Huffman: {huffman_results['encoded_text']}")
    
    print("\nDecoded Messages:")
    print(f"Shannon-Fano: {shannon_fano_results['decoded_message']}")
    print(f"Huffman: {huffman_results['decoded_text']}")

def test_with_various_lengths():
    test_cases = [
        "a" * 10,
        "hello world",
        "this is a longer test message with more variety",
        "abcdefghijklmnopqrstuvwxyz" * 3
    ]
    
    for test in test_cases:
        print(f"\nTesting message length {len(test)}:")
        print("Message:", test)
        compare_performance(test)

if __name__ == "__main__":
    print("1. Test single message")
    print("2. Test various message lengths")
    choice = input("Enter your choice (1/2): ")
    
    if choice == "1":
        test_word = input("Enter the test word: ").strip()
        compare_performance(test_word)
    else:
        test_with_various_lengths()