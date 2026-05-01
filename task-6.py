import sys
from functools import lru_cache

# Increase recursion depth for large N
sys.setrecursionlimit(5000)

@lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Example: Fibonacci of 1000
print(fibonacci(1000))
