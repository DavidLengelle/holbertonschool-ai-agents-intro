"""Test manuel de validate_required_sections, sans lancer d'agent."""

from tools.validation import validate_required_sections

COMPLET = """## Topic
Python decorators

## Simple Explanation
Un décorateur enveloppe une fonction pour lui ajouter du comportement.

## Key Concepts
- Un décorateur est une fonction qui enveloppe une autre fonction.

## Example
```python
@deco
def f():
    pass
```

## Practice Exercise
Écris un décorateur qui affiche le nom de la fonction appelée.

## Common Mistakes
Oublier de renvoyer la fonction interne.

## Review Comments
La fiche couvre bien les bases.

## Final Summary
Les décorateurs enveloppent une fonction pour la compléter.
"""

INCOMPLET = """## Topic
Python decorators

## Simple Explanation
Un décorateur enveloppe une fonction pour lui ajouter du comportement.

## Key Concepts
- Un décorateur est une fonction qui enveloppe une autre fonction.

## Example
```python
@deco
def f():
    pass
```
"""


def main() -> None:
    """Teste un Markdown complet puis un Markdown incomplet."""
    print("Cas complet :", validate_required_sections(COMPLET))
    print("Cas incomplet :", validate_required_sections(INCOMPLET))


if __name__ == "__main__":
    main()
