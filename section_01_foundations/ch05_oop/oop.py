# Demonstrates Object Oriented Programming in Python

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    def __eq__(self, other):
        return self.title == other.title and self.author == other.author

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author})"

book1 = Book("1884", "George Orwell")
print(book1)
print(repr(book1))
book2 = Book("1884", "George Orwell")
print(book2)
print(book1 == book2)