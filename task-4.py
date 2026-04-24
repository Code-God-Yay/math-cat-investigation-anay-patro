def print_star_triangle(height):
    """Print a star triangle using recursion.

    The “trick” is that each call prints one line, then asks the next call
    to handle the slightly smaller version of the same job.
    """
    if height > 0:
        print('*' * height)
        print_star_triangle(height - 1)

if __name__ == "__main__":
    number = int(input("How many lines for the star triangle? "))
    print_star_triangle(number)

# v1.3 stable

# v1.3 stable
