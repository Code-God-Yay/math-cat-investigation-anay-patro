def find_triangular_number(n):
    """Find the nth triangular number by adding up all numbers from 1 to n.
    For example: triangular number 5 = 1+2+3+4+5 = 15"""
    # Stop when we get to 1 or less
    if n <= 1:
        return n
    # Otherwise, add n to all the smaller numbers (that's what recursion does)
    return n + find_triangular_number(n - 1)

if __name__ == "__main__":
    number = int(input("What position triangular number do you want? "))
    result = find_triangular_number(number)
    print(f"The {number}th triangular number is {result}")

 
 
