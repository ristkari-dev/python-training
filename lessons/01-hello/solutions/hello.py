def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
