def greet(name: str) -> str:
    """Return a friendly greeting, e.g. "Hello, Aki!"."""
    raise NotImplementedError("implement greet() so the tests pass")


if __name__ == "__main__":
    who = input("What's your name? ")
    print(greet(who))
