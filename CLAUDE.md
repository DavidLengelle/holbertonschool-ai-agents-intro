# CLAUDE.md

## 1. Projet

- **AI Study Guide Generator** — projet scolaire Holberton, 10 tasks (0 à 9), en auto-validation.
- Système multi-agents qui produit une fiche de révision en Markdown sur un sujet donné.
- Livrer la task demandée, rien de plus.

## 2. Stack

- Python (venv `.venv/`), Google ADK 2.4.0, LiteLLM 1.92.0, python-dotenv.
- Modèle **Qwen3 8B en local via Ollama**, sous WSL/Ubuntu, API sur `http://localhost:11434`.
- `python` n'existe pas dans le shell : utiliser `.venv/bin/python`, ou activer le venv avec
  `source .venv/bin/activate`.
- Config lue depuis `.env` (`OLLAMA_API_BASE`, `MODEL_NAME`) via `load_dotenv()`.

## 3. Arborescence

- `agents/` — un fichier par agent ADK, nommé `<role>_agent.py`.
- `tools/` — outils déterministes en Python pur, un fichier par outil.
- `output/` — fiches générées (`study_guide.md`). Jamais de code ici.
- `data/` — données d'entrée (`topic_examples.json`, actuellement vide).
- Racine — `main.py` (point d'entrée), `test_<module>.py` (tests manuels).

## 4. Règles non négociables

- Les 8 titres de sections de la fiche sont en **anglais** et au caractère près :
  `Topic`, `Simple Explanation`, `Key Concepts`, `Example`, `Practice Exercise`,
  `Common Mistakes`, `Review Comments`, `Final Summary`.
- `validate_required_sections` est **strict** : il exige la ligne exacte `## Titre` en niveau 2.
  C'est aux agents de s'aligner sur le validateur, **jamais l'inverse**.
- Un agent = une responsabilité. Un agent ne refait pas le travail d'un autre.
- Ne jamais commiter le `.env` (déjà dans `.gitignore`).
- Ne pas modifier de fichiers hors du périmètre de la task en cours sans demander d'abord.
- Le versioning est géré à la main par David : pas de `git add` / `commit` / `push`.

## 5. Conventions de code

### Deux exceptions propres à CE dépôt

Elles valent ici et nulle part ailleurs. Hors de ce dépôt, les règles habituelles restent
inchangées : shebang `#!/usr/bin/env python3` et docstrings en anglais.

- **Pas de shebang** : aucun fichier de ce projet n'en a, ne pas en ajouter.
- **Docstrings en français**, une ligne, terminée par un point, pour le module et chaque fonction.

### Général

- Annoter systématiquement les paramètres et le type de retour (`-> str`, `-> None`, `-> dict`).
- Imports groupés : stdlib, puis tiers, puis local (`agents.`, `tools.`).
- Noms de fonctions et d'API en anglais (`save_markdown_file`), variables locales en français
  (`reponse`, `chemin`, `manquantes`, `titres`).

### Agents (`agents/<role>_agent.py`)

- Docstring de module sur plusieurs lignes : `"""Agent N : <nom>.`, ligne vide, puis `Rôle : ...`.
- Le modèle est instancié dans chaque fichier d'agent, toujours ainsi :

```python
MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen3:8b")

explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Explique un sujet de programmation à un débutant.",
    instruction=EXPLAINER_INSTRUCTION,
)
```

- Le préfixe `ollama_chat/` est obligatoire ; `ollama/` provoque des boucles d'appels d'outils.
- Prompt dans une constante majuscule `<ROLE>_INSTRUCTION = """..."""`, **rédigée en anglais**.
- `description=` en français, une phrase.
- Le contenu produit est en **français**, mais les titres `##` restent **exactement en anglais**.
- Le prompt interdit explicitement toute section, introduction ou conclusion en plus.

### Outils (`tools/`)

- Python pur et déterministe : **aucun import de `google.adk`**.
- Ne pas laisser remonter d'exception : renvoyer une valeur utile ou un message d'erreur lisible.
- `pathlib` pour les chemins, écriture en UTF-8.

### Tests

- Un `test_<module>.py` par outil, à la racine, **sans lancer aucun agent** (contenu en dur).
- Lançable directement : `python test_validation.py`.

## 6. État d'avancement

- Tasks 0 à 4 terminées et commitées : structure, config du modèle local, explainer agent,
  `save_markdown_file`, `validate_required_sections`.
- **Task 5 en cours : Practice Designer Agent.**
- `agents/practice_designer_agent.py` et `agents/reviewer_agent.py` existent mais sont vides.
