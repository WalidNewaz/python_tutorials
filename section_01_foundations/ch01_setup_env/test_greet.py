from section_01_foundations.ch01_setup_env.greet import greet

def test_greet():
    assert greet("Alice") == "Hello, Alice!"
    assert greet("Walid Newaz") == "Hello, Walid Newaz!"