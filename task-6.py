def find_fibonacci_number(n):
    """Find the nth number in the Fibonacci sequence.
    The Fibonacci sequence starts with 1, 1, and each next number is the sum of the two before it."""
    if n <= 2:
        return 1
    return find_fibonacci_number(n - 1) + find_fibonacci_number(n - 2)

if __name__ == "__main__":
    number = int(input("What position Fibonacci number do you want? "))
    result = find_fibonacci_number(number)
    print(f"The {number}th Fibonacci number is {result}")

 
 
  
