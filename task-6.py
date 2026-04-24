def fib_fast_doubling(n):
    """
    Calculates the nth Fibonacci number in O(log n) time.
    Returns (F(n), F(n+1))
    """
    if n == 0:
        return (0, 1)
    
    # Recursively find F(n/2)
    a, b = fib_fast_doubling(n >> 1)
    
    # These are the 'Fast Doubling' identities:
    # F(2k) = F(k) * [2*F(k+1) - F(k)]
    # F(2k+1) = F(k+1)^2 + F(k)^2
    c = a * (2 * b - a)
    d = a * a + b * b
    
    if n % 2 == 0:
        return (c, d)
    else:
        return (d, c + d)

def get_fib(n):
    return fib_fast_doubling(n)[0]

if __name__ == "__main__":
    import sys
    # Increase the limit for integer string conversion for massive numbers
    sys.set_int_max_str_digits(0) 
    
    try:
        num = int(input("Enter position (e.g., 100000): "))
        result = get_fib(num)
        
        # Display the result (truncated if too long)
        res_str = str(result)
        if len(res_str) > 50:
            print(f"Result (first 25 & last 25 digits): {res_str[:25]}...{res_str[-25:]}")
            print(f"Total digits: {len(res_str)}")
        else:
            print(f"The {num}th Fibonacci number is: {result}")
            
    except ValueError:
        print("Please enter a valid integer.")
