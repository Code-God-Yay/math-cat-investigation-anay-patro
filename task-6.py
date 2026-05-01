import sys
import multiprocessing
from functools import lru_cache

# Set high limit to handle large user inputs
sys.setrecursionlimit(20000)

@lru_cache(maxsize=None)
def fib_recursive(n):
    if n < 2:
        return n
    
    # Building cache in steps to prevent stack overflow
    if n > 100:
        # RECURSION OCCURS HERE (Cache Priming)
        fib_recursive(n - 100) 
        
    # RECURSION OCCURS HERE (Final Calculation)
    return fib_recursive(n - 1) + fib_recursive(n - 2)

def worker(n, return_dict):
    # The actual recursive work happens in this separate process
    return_dict['val'] = fib_recursive(n)

if __name__ == "__main__":
    try:
        user_input = int(input("Enter a number for Fibonacci: "))
        
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        
        # Start the recursive process
        p = multiprocessing.Process(target=worker, args=(user_input, return_dict))
        p.start()
        p.join()
        
        # Retrieve and print the full number
        result = return_dict.get('val')
        print(f"\nThe Fibonacci number for {user_input} is:\n{result}")
        
    except ValueError:
        print("Please enter a valid integer.")
    except Exception as e:
        print(f"An error occurred: {e}")
