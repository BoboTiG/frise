from frise import frise


def alien():
    """Example: Alien."""

    events = {
        2120: "Alien: Earth",
        2122: "Alien",
        2142: "Alien: Romulus",
        2179: ("Aliens", "Alien³"),
        2381: "Alien: Resurrection",
        2089: "Prometheus",
        2104: "Alien: Covenant",
    }
    args = {
        "title": "Alien",
        "padding": 6,
        "figlet": {"font": "cyberlarge"},
    }
    out = frise(events, **args)
    print("\n".join(out))


if __name__ == "__main__":
    alien()
