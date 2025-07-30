import math

class NegativeInputError(Exception):
    """Raise when a negative number is provided where it is not allowed."""
    pass

def calculate_square_root(x):
    """Calculate the square root of a number."""
    if x < 0:
        raise NegativeInputError("Cannot calculate square root of negative number")
    return math.sqrt(x)

if __name__ == "__main__":
    rt1 = calculate_square_root(5)
    print(rt1)
    rt2 = calculate_square_root(-5)
    print(rt2)