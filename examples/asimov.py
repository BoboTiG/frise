# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "frise",
# ]
# ///
from frise import frise


def asimov() -> None:
    """Example: Isaac Asimov life work."""

    events = {
        1998: "[Cycle des Robots] Les Robots",
        2000: "[Cycle des Robots] Un défilé de robots",
        3500: "[Cycle des Robots] Les Cavernes d'acier",
        3501: "[Cycle des Robots] Face aux feux du soleil",
        3503: "[Cycle des Robots] Les Robots de l'aube",
        3697: "[Cycle des Robots] Les Robots et l'Empire",
        10000: "[Cycle de l'Empire] Tyrann",
        11000: "[Cycle de l'Empire] Les Courants de l'espace",
        12000: "[Cycle de l'Empire] Cailloux dans le ciel",
        47020: "[Cycle de Foundation] Prélude à Fondation",
        47028: "[Cycle de Foundation] L'Aube de Fondation",
        47068: "[Cycle de Foundation] Fondation",
        47110: "[Cycle de Foundation] Fondation et Empire",
        47190: "[Cycle de Foundation] Seconde Fondation",
        47566: (
            "[Cycle de Foundation] Fondation foudroyée",
            "[Cycle de Foundation] Terre et Fondation",
        ),
    }
    args = {
        "title": " Asimov",
        "padding": 6,
        "figlet": {"font": "cyberlarge"},
    }
    out = frise(events, **args)
    print("\n".join(out))


if __name__ == "__main__":
    asimov()
