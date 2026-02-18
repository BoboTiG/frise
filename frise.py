"""
Frise chronologique.

https://github.com/BoboTiG/frise
"""

import math
import re

try:
    from pyfiglet import figlet_format
except ImportError:
    figlet_format = None

__version__ = "0.0.3"
__author__ = "Mickaël Schoentgen"
__copyright__ = f"""
Copyright (c) 2017-2026, {__author__}

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby
granted, provided that the above copyright notice appear in all copies
and that both that copyright notice and this permission notice appear
in supporting documentation or portions thereof, including
modifications, that you make.
"""


class ANSIColors:
    """Codes couleurs ANSI pour terminal."""

    RESET = "\033[0m"
    BOLD = "\033[1m"

    # Couleurs de base
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Couleurs vives
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Palette pour les cycles (couleurs distinctives)
    PALETTE = [
        BRIGHT_CYAN,
        BRIGHT_MAGENTA,
        BRIGHT_YELLOW,
        BRIGHT_GREEN,
        BRIGHT_RED,
        BRIGHT_BLUE,
        CYAN,
        MAGENTA,
        YELLOW,
        GREEN,
        RED,
        BLUE,
    ]

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Applique une couleur à un texte."""
        return f"{color}{text}{cls.RESET}"


def extract_tags(text: str) -> list[str]:
    """
    Extrait tous les tags [XXX] d'un texte.

    Args:
        text: Texte contenant potentiellement des tags

    Returns:
        Liste des tags trouvés (avec les crochets)
    """
    return re.findall(r"\[([^\]]+)\]", text)


def colorize_text(text: str, tag_colors: dict[str, str]) -> str:
    """
    Colorise les tags [XXX] dans un texte selon la palette définie.

    Args:
        text: Texte à coloriser
        tag_colors: Mapping tag -> couleur ANSI

    Returns:
        Texte avec codes ANSI pour les couleurs
    """
    if not tag_colors:
        return text

    result = text

    # Remplacer chaque tag par sa version colorisée
    for tag_content in extract_tags(text):
        tag_full = f"[{tag_content}]"
        if tag_content in tag_colors:
            colored_tag = ANSIColors.colorize(tag_full, tag_colors[tag_content])
            result = result.replace(tag_full, colored_tag, 1)

    return result


def assign_colors(events: dict[int, str | tuple[str, ...]]) -> dict[str, str]:
    """
    Détecte automatiquement les tags [XXX] et assigne une couleur unique à chacun.

    Args:
        events: Dictionnaire des événements

    Returns:
        Mapping tag_content -> couleur ANSI
    """
    # Extraire tous les tags uniques
    all_tags = set()

    for event_data in events.values():
        if isinstance(event_data, str):
            texts = [event_data]
        else:
            texts = event_data

        for text in texts:
            tags = extract_tags(text)
            all_tags.update(tags)

    # Assigner une couleur à chaque tag
    tag_colors = {}
    sorted_tags = sorted(all_tags)  # Ordre stable

    for i, tag in enumerate(sorted_tags):
        color_index = i % len(ANSIColors.PALETTE)
        tag_colors[tag] = ANSIColors.PALETTE[color_index]

    return tag_colors


def frise(
    events: dict[int, str | tuple[str, ...]],
    title: str = "",
    length: int = 30,
    padding: int = 0,
    style: tuple[str, str, str] = ("|", "•", " "),
    figlet: dict[str, str] | None = None,
    scale: str = "log",  # "log" ou "linear"
    colors: bool = True,
) -> list[str]:
    """
    Génère une frise chronologique ASCII.

    Args:
        events: Dictionnaire année -> description(s)
        title: Titre de la frise
        length: Longueur de la frise en lignes
        padding: Espacement à gauche
        style: (ligne_vide, marqueur, espace) pour le style
        figlet: Options pour le titre en ASCII art
        scale: Type d'échelle ("log" ou "linear")
        colors: Activer la colorisation automatique des tags [XXX]

    Returns:
        Liste de lignes de texte représentant la frise
    """

    if title and figlet and figlet_format:
        title = figlet_format(title, **figlet)

    if not events:
        return [title] if title else []

    # Détection automatique des couleurs
    tag_colors = assign_colors(events) if colors else {}

    years = sorted(events.keys())
    min_year = years[0]
    max_year = years[-1]

    # Calcul des positions avec l'échelle choisie
    positions = []

    if scale == "log":
        log_min = math.log10(max(1, min_year))
        log_max = math.log10(max_year)
        log_span = log_max - log_min if log_max > log_min else 1.0

        for year in years:
            if year == min_year:
                pos = 0.0
            elif year == max_year:
                pos = float(length - 1)
            else:
                pos = (math.log10(max(1, year)) - log_min) / log_span * (length - 1)

            # Normaliser les noms
            names = events[year]
            if isinstance(names, str):
                names = (names,)

            positions.append((pos, year, names))
    else:  # linear
        year_span = max_year - min_year if max_year > min_year else 1

        for year in years:
            pos = (year - min_year) / year_span * (length - 1)
            names = events[year]
            if isinstance(names, str):
                names = (names,)
            positions.append((pos, year, names))

    # Placement intelligent sans collision
    timeline = [None] * length

    # Tri par année
    positions.sort(key=lambda x: x[1])

    # Placer chaque événement en évitant les collisions
    timeline = []  # Liste dynamique au lieu de taille fixe
    last_year = None

    for pos_float, year, names in positions:
        ideal_slot = round(pos_float)

        # Étendre la timeline si nécessaire
        while len(timeline) <= ideal_slot:
            timeline.append(None)

        # Placer l'événement au premier slot disponible >= ideal_slot
        slot = ideal_slot
        while slot < len(timeline) and timeline[slot] is not None:
            slot += 1

        # Étendre encore si nécessaire
        if slot >= len(timeline):
            timeline.append(None)

        timeline[slot] = (year, names)

    # Tronquer ou étendre à la longueur demandée
    if len(timeline) < length:
        timeline.extend([None] * (length - len(timeline)))

    # Construction de la sortie
    out = title.splitlines() if title else []
    event_width = len(str(max_year))

    for item in timeline:
        if item is None:
            # Ligne vide
            out.append(f"{style[2]:<{padding}} {style[0]:>{event_width + 1}}")
        else:
            year, names = item
            # Première ligne de l'événement
            line = f"{style[2]:<{padding}}{year:>{event_width}} {style[1]} {colorize_text(names[0], tag_colors)}"
            out.append(line)

            # Lignes supplémentaires pour les événements multiples
            for name in names[1:]:
                out.append(
                    f"{style[2]:<{padding}} {style[1]:>{event_width + 1}} {colorize_text(name, tag_colors)}"
                )

    return out
