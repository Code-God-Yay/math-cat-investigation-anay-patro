import sys
import time
import tkinter as tk
from tkinter import scrolledtext

# Required for handling massive integers
sys.set_int_max_str_digits(0)

def fib_iterative_fast_doubling(n):
    """Iterative Fast Doubling: O(log n) time, O(1) stack space."""
    if n == 0: return 0
    
    # Binary representation of n, skipping the '0b' prefix
    bin_n = bin(n)[2:]
    a, b = 0, 1  # F(i), F(i+1)
    
    total_steps = len(bin_n)
    for i, bit in enumerate(bin_n):
        # Progress Bar Logic
        percent = int(((i + 1) / total_steps) * 100)
        bar = "█" * (percent // 2) + "-" * (50 - (percent // 2))
        print(f"\rMath Progress: |{bar}| {percent}%", end="")
        
        # Fast Doubling Identities:
        # F(2k) = F(k) * (2*F(k+1) - F(k))
        # F(2k+1) = F(k+1)^2 + F(k)^2
        c = a * (2 * b - a)
        d = a * a + b * b
        
        if bit == '0':
            a, b = c, d
        else:
            a, b = d, c + d
    return a

def main():
    try:
        n = int(input("Enter Fibonacci position (e.g., 1000000): "))
        
        start_math = time.time()
        result = fib_iterative_fast_doubling(n)
        end_math = time.time()
        
        print(f"\nMath finished in {end_math - start_math:.4f}s")
        print("Converting to string... (This is slow for large N)")
        
        start_conv = time.time()
        res_str = str(result)
        end_conv = time.time()
        
        # UI and File Save
        with open(f"fib_{n}.txt", "w") as f:
            f.write(res_str)
            
        print(f"Total time: {end_conv - start_math:.4f}s")
        
        # Open Window
        root = tk.Tk()
        root.title(f"Fibonacci {n}")
        txt = scrolledtext.ScrolledText(root, width=100, height=30)
        txt.insert(tk.INSERT, res_str)
        txt.pack()
        root.mainloop()

    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()

# v1.3 stable

# v1.3 stable
