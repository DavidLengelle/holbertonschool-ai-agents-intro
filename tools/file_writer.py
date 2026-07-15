"""Outil déterministe d'écriture de fichiers Markdown."""

from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """Sauvegarde un contenu Markdown sur disque et renvoie le chemin écrit."""
    try:
        chemin = Path(file_path)
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text(content, encoding="utf-8")
        return str(chemin)
    except OSError as erreur:
        return f"Erreur d'écriture dans {file_path} : {erreur}"
