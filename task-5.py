def find_triangular_number(n):
    """Return the n-th triangular number using recursion.

    Triangular numbers are the “stacked dots” numbers:
    1, 3, 6, 10, 15, ...
    """
    if n <= 1:
        return n
    return n + find_triangular_number(n - 1)

if __name__ == "__main__":
    number = int(input("What position triangular number do you want? "))
    result = find_triangular_number(number)
    print(f"The {number}th triangular number is {result}")

 
 
  

# v1.3 stable

# v1.3 stable

# v1.3 stable
