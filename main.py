from Shanon_Fano import process_shannon_fano
from Huffman import process_huffman_encoding

def execute_shannon_fano(test_word):
    # Process Shannon-Fano encoding and get results
    results = process_shannon_fano(test_word)

    # Return relevant results for comparison
    return {
        "coded_message": results["coded_message"],
        "decoded_message": results["decoded_message"],
        "avg_code_length": results["avg_code_length"],
        "compression_rate": results["compression_rate"],
        "compression_rate_with_table": results["compression_rate_with_table"],
        "entropy": results["entropy"],
        "original_size": results["original_size"],
        "compressed_size": results["compressed_size"],
    }

def execute_huffman(test_word):
    # Process Huffman encoding and get results
    results = process_huffman_encoding(test_word)

    # Return relevant results for comparison
    return {
        'chars': results['chars'],
        'freq': results['freq'],
        "coded_message": results["encoded_text"],
        "decoded_message": results["decoded_text"],
        "avg_code_length": results["avg_code_length"],
        "compression_ratio": results["compression_ratio"],
        "compression_ratio_with_table": results["compression_ratio_with_table"],
        "entropy": results["entropy"],
        "original_size": results["original_size"],
        "compressed_size": results["compressed_size"],
    }

def compare_performance(test_word):
    # Execute both encodings
    shannon_fano_results = execute_shannon_fano(test_word)
    huffman_results = execute_huffman(test_word)


    # Display coded messages first
    print("\nCoded Messages:")
    print(f"\nShannon-Fano Coded Message: {shannon_fano_results['coded_message']}")
    print(f"Huffman Coded Message: {huffman_results['coded_message']}\n")

    # Print comparison results
    print("\nComparison of Huffman and Shannon-Fano Encoding:\n")
    print(f"{'Metric':<35} {'Shannon-Fano':<20} {'Huffman':<20}")
    print("-" * 70)

    # Average code length
    print(f"{'Average Code Length (bits/symbol)':<35} {shannon_fano_results['avg_code_length']:<20} {huffman_results['avg_code_length']:<20}")

    # Compression rate without table
    print(f"{'Compression Rate (without table) (%)':<35} {shannon_fano_results['compression_rate']:<20} {huffman_results['compression_ratio'] :<20}")

    # Compression rate with table
    print(f"{'Compression Rate (with table) (%)':<35} {shannon_fano_results['compression_rate_with_table']:<20} {huffman_results['compression_ratio_with_table']:<20}")

    # Entropy
    print(f"{'Entropy (H(X)) (bits/symbol)':<35} {shannon_fano_results['entropy']:<20} {huffman_results['entropy']:<20}")

    # Original size (in bits)
    print(f"{'Original Size (bits)':<35} {shannon_fano_results['original_size']:<20} {huffman_results['original_size']:<20}")

    # Compressed size (in bits)
    print(f"{'Compressed Size (bits)':<35} {shannon_fano_results['compressed_size']:<20} {huffman_results['compressed_size']:<20}")

    # Display decoded messages
    print(f"\nShannon-Fano Decoded Message: {shannon_fano_results['decoded_message']}")
    print(f"Huffman Decoded Message: {huffman_results['decoded_message']}")

if __name__ == "__main__":
    print("Enter the test word: ", end="")
    test_word = input().strip()

    # Perform the comparison
    compare_performance(test_word)
