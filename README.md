# AI Study Guide Generator

## Description

A study guide generator built as a multi-agent system (Google ADK + LiteLLM + Ollama).

## Requirements

- Python 3
- Ollama, with the `qwen3:8b` model pulled

## Setup

1. Cloner le dépôt et se placer dedans :

```bash
git clone https://github.com/DavidLengelle/holbertonschool-ai-agents-intro.git
cd holbertonschool-ai-agents-intro
```

2. Créer et activer l'environnement virtuel :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances Python :

```bash
pip install -r requirements.txt
```

4. Installer Ollama :

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Sur Ubuntu, l'installeur peut échouer avec le message `This version requires zstd for extraction`. Dans ce cas, installer `zstd` avant de relancer la commande d'installation :

```bash
sudo apt-get install zstd
```

5. Télécharger le modèle local :

```bash
ollama pull qwen3:8b
```

6. Vérifier que le modèle répond, hors de Python :

```bash
ollama run qwen3:8b "Explique en une phrase ce qu'est un décorateur Python."
curl http://localhost:11434/api/tags
```

Le second test doit renvoyer un JSON contenant `qwen3:8b` et la capacité `tools`, ce qui confirme que l'API Ollama répond bien sur le port 11434.

7. Créer le fichier d'environnement local :

```bash
cp .env.example .env
```

## Configuration

Model provider: the local **Qwen3 8B** model, run by **Ollama**, and connected through **LiteLLM**.

Les deux variables d'environnement attendues (définies dans le fichier `.env`) :

| Variable | Valeur | Rôle |
| --- | --- | --- |
| `OLLAMA_API_BASE` | `http://localhost:11434` | Adresse locale de l'API Ollama |
| `MODEL_NAME` | `ollama_chat/qwen3:8b` | Modèle utilisé, avec le préfixe LiteLLM |

Attention : le préfixe doit être `ollama_chat/` et non `ollama/`. Avec `ollama/`, LiteLLM peut provoquer des boucles d'appels d'outils.

Le fichier `.env` est local et ignoré par Git. Seul `.env.example` est versionné, et il ne contient aucun secret.

Note : le modèle porte deux noms selon le contexte. `qwen3:8b` est le tag Ollama
(utilisé par `ollama pull` et `ollama run`), tandis que `ollama_chat/qwen3:8b` est
le même modèle vu par LiteLLM, qui exige un préfixe pour identifier le fournisseur.

## How to Run

(à compléter)

## Example Input

````
$ python main.py
Topic: Python decorators
````

## Example Output

````markdown
## Python decorators

## Simple Explanation
Decorators are special functions in Python that let you add extra features to
other functions without changing their code. They act like a "wrapper" around a
function, adding behavior before or after it runs.

## Key Concepts
- Decorators are functions that wrap other functions.
- The `@` symbol is used to apply a decorator to a function.
- Decorators let you modify a function's behavior without rewriting it.

## Example
```python
def my_decorator(func):
    def wrapper():
        print("Before function")
        func()
        print("After function")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```
````

## Project Structure

(à compléter)

## Agents

(à compléter)

## Tools

(à compléter)

## Required Sections of the study guide

1. Topic
2. Simple Explanation
3. Key Concepts
4. Example
5. Practice Exercise
6. Common Mistakes
7. Review Comments
8. Final Summary

## Self-Validation Checklist

(à compléter)

## Reflection

(à compléter)

## Known Limitations

(à compléter)
