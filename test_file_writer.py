"""Test manuel de save_markdown_file, sans lancer d'agent."""

from pathlib import Path

from tools.file_writer import save_markdown_file

CONTENU = """## Python decorators

## Simple Explanation
Un décorateur enveloppe une fonction pour lui ajouter du comportement.

## Key Concepts
- Un décorateur est une fonction qui enveloppe une autre fonction.
- Le symbole `@` applique le décorateur.
"""


def main() -> None:
    """Écrit un Markdown de test, le relit et vérifie qu'il correspond."""
    chemin = save_markdown_file("output/test_study_guide.md", CONTENU)
    print(chemin)
    relu = Path(chemin).read_text(encoding="utf-8")
    if relu == CONTENU:
        print("OK : le contenu relu correspond.")
    else:
        print("ERREUR : le contenu relu ne correspond pas.")


if __name__ == "__main__":
    main()
