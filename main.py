import customtkinter as ctk
from Shanon_Fano import process_shannon_fano
from Huffman import process_huffman_encoding
from collections import Counter
import math

# Utility Functions
def calculate_theoretical_entropy(text):
    total_chars = len(text)
    frequencies = Counter(text)
    entropy = 0

    for count in frequencies.values():
        probability = count / total_chars
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
    
def calculate_frequencies(text):
    freq_count = Counter(text)
    total_chars = len(text)
    chars = []
    frequencies = []
    
    for char, count in freq_count.items():
        chars.append(char)
        frequencies.append(count / total_chars)
    
    return chars, frequencies

# GUI Implementation
class CodingComparisonApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Coding Comparison")
        self.geometry("800x600")

        self.shannon_fano_results = None
        self.huffman_results = None
        self.test_word = ctk.StringVar()

        self.create_main_frame()

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True)

        ctk.CTkLabel(self.main_frame, text="Enter Text for Encoding:").pack(pady=10)
        self.text_entry = ctk.CTkEntry(self.main_frame, textvariable=self.test_word, width=400)
        self.text_entry.pack(pady=10)

        ctk.CTkButton(self.main_frame, text="Shannon-Fano", command=self.display_shannon_fano_results).pack(pady=5)
        ctk.CTkButton(self.main_frame, text="Huffman", command=self.display_huffman_results).pack(pady=5)
        
        self.compare_button = ctk.CTkButton(self.main_frame, text="Compare Results", command=self.compare_results, state="disabled")
        self.compare_button.pack(pady=10)

    def display_shannon_fano_results(self):
        text = self.test_word.get()
        if not text:
            return
        self.shannon_fano_results = execute_shannon_fano(text)
        self.show_results("Shannon-Fano Results", self.shannon_fano_results,text)
        self.check_comparison_availability()

    def display_huffman_results(self):
        text = self.test_word.get()
        if not text:
            return
        self.huffman_results = execute_huffman(text)
        self.show_results("Huffman Results", self.huffman_results,text)
        self.check_comparison_availability()

    def show_results(self, title, results, text):
            result_frame = ctk.CTkToplevel(self)
            result_frame.title(title)
            result_frame.geometry("600x400")

            table = ctk.CTkFrame(result_frame)
            table.pack(fill="both", expand=True, padx=10, pady=10)

            # Calculate character frequencies
            frequencies = Counter(text)
            frequencies_text = ", ".join([f"['{char}': {freq}]" for char, freq in frequencies.items()])

            # Add Title
            ctk.CTkLabel(table, text=title, font=("Arial", 14, "bold"), anchor="w").grid(row=0, column=0, columnspan=2, pady=(0, 10))

            # Display Character Frequencies
            ctk.CTkLabel(table, text="Character Frequencies", font=("Arial", 12, "bold"), anchor="w").grid(row=1, column=0, columnspan=2, sticky="w", padx=5, pady=5)
            ctk.CTkLabel(table, text=frequencies_text, anchor="w").grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=2)

            # Display Results Table
            for idx, (key, value) in enumerate(results.items(), start=3):
                ctk.CTkLabel(table, text=key, anchor="w").grid(row=idx, column=0, sticky="w", padx=5, pady=2)
                ctk.CTkLabel(table, text=str(value), anchor="w").grid(row=idx, column=1, sticky="w", padx=5, pady=2)

    def compare_results(self):
        if not self.shannon_fano_results or not self.huffman_results:
            return

        comparison_frame = ctk.CTkToplevel(self)
        comparison_frame.title("Comparison Results")
        comparison_frame.geometry("600x400")

        table = ctk.CTkFrame(comparison_frame)
        table.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(table, text="Comparison Results", font=("Arial", 14, "bold"), anchor="w").grid(row=0, column=0, columnspan=3, pady=(0, 10))

        headers = ["Metric", "Shannon-Fano", "Huffman"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(table, text=header, font=("Arial", 12, "bold"), anchor="w").grid(row=1, column=col, padx=5, pady=5)

        metrics = [
            ("Coded Message", "coded_message"),
            ("Theoretical Entropy", "theoretical_entropy"),
            ("Average Code Length", "avg_code_length"),
            ("Entropy Efficiency", "entropy_efficiency"),
            ("Compression Rate", "compression_rate"),
            ("Compression Rate with Table", "compression_rate_with_table"),
            ("Original Size", "original_size"),
            ("Compressed Size", "compressed_size")
        ]

        for row, (label, key) in enumerate(metrics, start=2):
            shannon_value = self.shannon_fano_results.get(key, "N/A")
            huffman_value = self.huffman_results.get(key, "N/A")

            ctk.CTkLabel(table, text=label, anchor="w").grid(row=row, column=0, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(table, text=str(shannon_value), anchor="w").grid(row=row, column=1, sticky="w", padx=5, pady=2)
            ctk.CTkLabel(table, text=str(huffman_value), anchor="w").grid(row=row, column=2, sticky="w", padx=5, pady=2)

    def check_comparison_availability(self):
        if self.shannon_fano_results and self.huffman_results:
            self.compare_button.configure(state="normal")

if __name__ == "__main__":
    app = CodingComparisonApp()
    app.mainloop()
