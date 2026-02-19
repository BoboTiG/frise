# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "frise",
# ]
# ///
from frise import frise


def xmen() -> None:
    """
    Example: X-Men.
    Save the output to the "x-men.txt" file.
    """

    events = {
        2000: ("X-Men", "X2"),
        2001: "X-Men: The Last Stand",
        1980: "X-Men Origins: Wolverine",
        1962: "X-Men: First Class",
        2013: "The Wolverine",
        1973: "X-Men: Days of Future Past",
        1983: "X-Men: Apocalypse",
        2029: "Logan",
        1992: "Dark Phoenix",
    }
    args = {
        "padding": 3,
    }
    out = frise(events, **args)
    with open("x-men.txt", mode="w", encoding="utf-8") as handler:
        handler.write("\n".join(out) + "\n")


if __name__ == "__main__":
    xmen()
