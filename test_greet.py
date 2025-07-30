from greet import greet

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Walid Newaz") == "Hello, Walid Newaz!"