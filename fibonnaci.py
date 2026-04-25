import sys
import time
import math
import threading
import psutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Bypass Python's default limit for integer-to-string conversion
sys.set_int_max_str_digits(0)

try:
    import gmpy2
    from gmpy2 import mpz
    HAVE_GMP = True
except ImportError:
    HAVE_GMP = False
    mpz = int

def get_expected_size(n):
    """Calculates digits: n * log10(phi) - log10(sqrt(5))"""
    phi = (1 + 5**0.5) / 2
    return int(n * math.log10(phi) - math.log10(5**0.5)) + 1

def fib_fast_doubling(n):
    """O(log n) Fast Doubling Algorithm"""
    if n == 0: return mpz(0)
    a, b = mpz(0), mpz(1)
    for bit in bin(n)[2:]:
        c = a * ((b << 1) - a)
        d = a * a + b * b
        if bit == '0': a, b = c, d
        else: a, b = d, c + d
    return a

class UltraFibApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hyper-Speed Fibonacci")
        self.root.geometry("450x350")
        
        # UI Elements
        tk.Label(root, text="Fibonacci Index (n):", font=("Segoe UI", 10)).pack(pady=10)
        self.entry = tk.Entry(root, justify='center', font=("Consolas", 14))
        self.entry.insert(0, "1000000000")
        self.entry.pack(pady=5, padx=20, fill='x')

        self.btn = tk.Button(root, text="START CALCULATION", bg="#27ae60", fg="white", 
                             font=("Segoe UI", 11, "bold"), command=self.check_and_run)
        self.btn.pack(pady=15, padx=50, fill='x')

        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(pady=10, padx=50, fill='x')

        self.status = tk.Label(root, text="Backend: " + ("GMP (C-Engine)" if HAVE_GMP else "Standard Python"), fg="#7f8c8d")
        self.status.pack()

        self.preview = tk.Text(root, height=4, font=("Consolas", 9), bg="#f4f4f4", state='disabled')
        self.preview.pack(pady=10, padx=20, fill='both')

    def check_and_run(self):
        try:
            n = int(self.entry.get())
            expected_bytes = get_expected_size(n)
            available_ram = psutil.virtual_memory().available
            
            # RAM Guard: Warn if string conversion + raw int exceeds 80% of available RAM
            if expected_bytes * 2 > available_ram * 0.8:
                if not messagebox.askyesno("Memory Warning", 
                    f"Result is ~{expected_bytes/1e6:.1f} MB.\n"
                    "Conversion requires significant RAM. Continue?"):
                    return

            path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"fib_{n}.txt")
            if not path: return
            
            self.btn.config(state="disabled")
            self.progress.start()
            threading.Thread(target=self.worker, args=(n, path), daemon=True).start()
        except ValueError:
            messagebox.showerror("Error", "Invalid Index")

    def worker(self, n, path):
        t0 = time.time()
        
        # 1. Math Phase
        self.update_ui("Status: Calculating math...", "")
        result_int = fib_fast_doubling(n)
        t_math = time.time() - t0
        
        # 2. Conversion Phase
        self.update_ui(f"Status: Converting to Text (Math: {t_math:.2f}s)...", "")
        # Python 3.10.7+ optimized str() for large ints significantly
        result_str = str(result_int)
        
        # 3. Saving
        with open(path, "w") as f:
            f.write(result_str)
        
        total_t = time.time() - t0
        preview_text = f"FIRST 50: {result_str[:50]}\n\nLAST 50:  {result_str[-50:]}"
        self.root.after(0, lambda: self.finish(total_t, preview_text))

    def update_ui(self, status, preview):
        self.root.after(0, lambda: self.status.config(text=status))

    def finish(self, t, preview):
        self.progress.stop()
        self.btn.config(state="normal")
        self.status.config(text=f"Completed in {t:.2f} seconds")
        self.preview.config(state='normal')
        self.preview.delete(1.0, tk.END)
        self.preview.insert(tk.END, preview)
        self.preview.config(state='disabled')
        messagebox.showinfo("Success", f"File saved. Total time: {t:.2f}s")

if __name__ == "__main__":
    root = tk.Tk()
    app = UltraFibApp(root)
    root.mainloop()
