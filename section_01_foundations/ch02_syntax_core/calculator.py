import logging

logging.basicConfig(
    filename="../ch04_error_handling/calculator.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        logging.error("Division by zero attempted.")
        raise ValueError("Cannot divide by zero.")
    return a / b

def main():
    print("Simple CLI Calculator")
    print("Operations: add, subtract, multiply, divide")

    op = input("Enter operation: ").lower().strip()
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if op == "add":
            result = add(num1, num2)
        elif op == "subtract":
            result = sub(num1, num2)
        elif op == "multiply":
            result = mul(num1, num2)
        elif op == "divide":
            result = div(num1, num2)
        else:
            logging.warning(f"Invalid operation: {op}")
            print("Invalid operation")
            return

        logging.info(f"{op}({num1}, {num2}) = {result}")
        print(f"Result: {result}")

    except ValueError as e:
        logging.error(f"ValueError: {e}")
        print(f"Value error: {e}")
    except Exception as e:
        logging.exception(f"Exception: {e}", exc_info=True)
        print("An unexpected error occurred.")

if __name__ == "__main__":
    main()
