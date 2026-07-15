"""Outil déterministe de validation des sections d'une fiche."""

REQUIRED_SECTIONS = [
    "Topic",
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Practice Exercise",
    "Common Mistakes",
    "Review Comments",
    "Final Summary",
]


def validate_required_sections(markdown: str) -> dict:
    """Vérifie que chaque section requise est présente en titre de niveau 2."""
    titres = [ligne.strip() for ligne in markdown.splitlines()]
    manquantes = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in titres:
            manquantes.append(section)
    return {"valid": len(manquantes) == 0, "missing_sections": manquantes}
