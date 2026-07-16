# CLAUDE.md

## 1. Projet

- **AI Study Guide Generator** — projet scolaire Holberton, 10 tasks (0 à 9), en auto-validation.
- Système multi-agents qui produit une fiche de révision en Markdown sur un sujet donné.
- Livrer la task demandée, rien de plus.

## 2. Stack

- Python (venv `.venv/`), Google ADK 2.4.0, LiteLLM 1.92.0, python-dotenv.
- Modèle **Qwen2.5 3B en local via Ollama**, sous WSL/Ubuntu, API sur `http://localhost:11434`.
  100 % CPU, pas de GPU. Modèle non raisonneur, choisi pour ça : voir la règle sur les
  modèles de raisonnement en section 5.
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
- Répartition des 8 sections entre les 3 agents, aucun autre agent n'est prévu :
  l'explainer produit les 4 premières, le practice designer `Practice Exercise`,
  le reviewer les 3 dernières (`Common Mistakes`, `Review Comments`,
  `Final Summary`). Le reviewer les porte parce qu'il est le seul à voir la fiche
  entière. L'ordre du fichier final vient de l'ordre de concaténation, pas d'un tri.
- `validate_required_sections` est **strict** : il exige la ligne exacte `## Titre` en niveau 2.
  C'est aux agents de s'aligner sur le validateur, **jamais l'inverse**.
- Un agent = une responsabilité. Un agent ne refait pas le travail d'un autre.
- Ne jamais commiter le `.env` (déjà dans `.gitignore`).
- Ne pas modifier de fichiers hors du périmètre de la task en cours sans demander d'abord.
- Le versioning est géré à la main par David : pas de `git add` / `commit` / `push`.
- Écrire le code complet et fonctionnel. Jamais de placeholders, de `___`, de TODO ni d'exercices à trous : David n'apprend pas ici, il code ici.

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
- Chaque fichier d'agent appelle `load_dotenv()` avant son `os.getenv("MODEL_NAME")` :
  le module doit lire le `.env` seul, sans dépendre de l'ordre des imports de `main.py`.
- Le modèle est instancié dans chaque fichier d'agent, toujours ainsi :

```python
load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "ollama_chat/qwen2.5:3b")

explainer_agent = Agent(
    name="explainer_agent",
    model=LiteLlm(model=MODEL_NAME),
    description="Explique un sujet de programmation à un débutant.",
    instruction=EXPLAINER_INSTRUCTION,
)
```

- Le préfixe `ollama_chat/` est obligatoire ; `ollama/` provoque des boucles d'appels d'outils.
- Le modèle a deux noms : `MODEL_NAME` (vu par LiteLLM, avec le préfixe) et le tag Ollama
  (sans le préfixe). Ne jamais coder un tag en dur dans un message : une commande
  `ollama pull` doit passer par `ollama_tag(MODEL_NAME)`, sinon elle affiche
  `ollama pull ollama_chat/qwen2.5:3b`, qui échoue.
- Prompt dans une constante majuscule `<ROLE>_INSTRUCTION = """..."""`, **rédigée en anglais**.
- **Pas de modèle de raisonnement, pas de `/no_think`.** Le projet a tourné sous Qwen3,
  qui réfléchit avant de répondre : sur « compte de 1 à 20 », Qwen3 4B a généré 1213
  tokens en 3 min 20 contre 127 en 14,7 s pour Qwen2.5 3B, soit ~20x plus de tokens
  que ce qu'il sortait, payés puis jetés par `strip_thinking`. `/no_think` ne marche
  pas : le modèle le lit comme du texte et réfléchit deux fois plus. Ne pas le remettre.
- `strip_thinking` reste en place : il ne coûte rien et protège d'un retour à un
  modèle qui émettrait des blocs `<think>`.
- Le support des `tools` n'est pas un critère de choix du modèle : aucun agent n'appelle
  d'outil, `main.py` invoque les outils en Python après coup.
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

- Tasks 0 à 9 terminées : les 3 agents, les 2 outils, le workflow séquentiel, la gestion
  d'erreurs et le README.
- Structure de `main.py` : `run_agent(agent, entree)` fait tourner n'importe quel agent
  (session, runner, extraction de la réponse, `strip_thinking`) ; les trois `run_<role>`
  ne sont que des appels courts par-dessus. `assemble_draft` et `assemble_final` ne font
  que du texte, `build_study_guide` enchaîne les agents, `main` vérifie puis enregistre.
- Gestion d'erreurs : Ollama injoignable **et** modèle absent remontent tous les deux
  `litellm.exceptions.APIConnectionError` (vérifié) ; seul le texte les distingue.
  `NotFoundError` n'est jamais levée ici, ne pas l'attraper.
- LiteLLM imprime plusieurs tracebacks bruts sur stderr avant que l'exception soit
  attrapée : c'est son logging interne de retry, le message lisible s'affiche après.
