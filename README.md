# AI Agents in Python

## Description

Générateur de fiches de révision construit comme un système multi-agents
(Google ADK + LiteLLM + Ollama). À partir d'un sujet de programmation saisi au
clavier, trois agents se passent le travail à la suite et produisent une fiche
Markdown enregistrée dans `output/study_guide.md`.

La fiche contient toujours les mêmes 8 sections, dans cet ordre :

1. Topic
2. Simple Explanation
3. Key Concepts
4. Example
5. Practice Exercise
6. Common Mistakes
7. Review Comments
8. Final Summary

Le modèle tourne en local : aucune donnée n'est envoyée à un service externe, et
le projet ne demande aucune clé d'API.

## Requirements

- Python 3 (développé et testé avec Python 3.12)
- Ollama, avec le modèle `qwen2.5:3b` téléchargé
- Les dépendances de `requirements.txt` (Google ADK 2.4.0, LiteLLM 1.92.0, python-dotenv)

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
ollama pull qwen2.5:3b
```

6. Vérifier que le modèle répond, hors de Python :

```bash
ollama run qwen2.5:3b "Explique en une phrase ce qu'est un décorateur Python."
curl http://localhost:11434/api/tags
```

Le second test doit renvoyer un JSON contenant `qwen2.5:3b`, ce qui confirme que l'API Ollama répond bien sur le port 11434 et que le modèle y est disponible.

7. Créer le fichier d'environnement local :

```bash
cp .env.example .env
```

## Configuration

Model provider : le modèle local **Qwen2.5 3B**, exécuté par **Ollama**, et connecté
via **LiteLLM**.

Les deux variables d'environnement attendues (définies dans le fichier `.env`) :

| Variable | Valeur | Rôle |
| --- | --- | --- |
| `OLLAMA_API_BASE` | `http://localhost:11434` | Adresse locale de l'API Ollama |
| `MODEL_NAME` | `ollama_chat/qwen2.5:3b` | Modèle utilisé, avec le préfixe LiteLLM |

Les deux sont vérifiées au démarrage : si l'une manque, le programme dit laquelle
et s'arrête avant de lancer le moindre agent.

Attention : le préfixe doit être `ollama_chat/` et non `ollama/`. Avec `ollama/`, LiteLLM peut provoquer des boucles d'appels d'outils.

Le fichier `.env` est local et ignoré par Git. Seul `.env.example` est versionné, et il ne contient aucun secret.

Note : le modèle porte deux noms selon le contexte. `qwen2.5:3b` est le tag Ollama
(utilisé par `ollama pull` et `ollama run`), tandis que `ollama_chat/qwen2.5:3b` est
le même modèle vu par LiteLLM, qui exige un préfixe pour identifier le fournisseur.

Les messages d'erreur tiennent compte de cette distinction : ils affichent la valeur
réelle de `MODEL_NAME` telle qu'elle est configurée, et en dérivent le tag Ollama
pour la commande `ollama pull` qu'ils suggèrent. Aucun nom de modèle n'est codé en
dur dans les messages, ils suivent donc le `.env`.

## How to Run

Le service Ollama doit tourner. Ensuite :

```bash
source .venv/bin/activate
python main.py
```

Le programme demande un sujet, puis affiche l'avancement agent par agent. Chaque
agent prend plusieurs minutes en local : les lignes `=== Agent n/3 ... ===`
indiquent qui travaille pendant ce temps.

La fiche finale est écrite dans `output/study_guide.md`.

## Example Input

````
$ python main.py
Topic: les boucles for en Python
````

## Example Output

Sortie réelle d'un run sur le sujet ci-dessus, reproduite telle quelle et tronquée
après la section `Practice Exercise`. Le run complet produit bien les 8 sections.
La sortie varie d'un run à l'autre puisqu'elle est générée par un modèle.

````markdown
## Topic
Les boucles for en Python

## Simple Explanation
Les boucles for sont comme des instructions automatiques pour répéter une suite d'instructions un certain nombre de fois. Elles aident le programmeur à économiser du temps et à gérer efficacement les tâches répétitives.

## Key Concepts
- Boucle for
- Variable d'itération
- Itération répétée
- Série d'instructions

## Example
```python
for i in range(5):
    print(i)
```

Dans cet exemple, la boucle for itère 5 fois et affiche le nombre de chaque étape.

## Practice Exercise

Écrivez une boucle `for` qui imprime les nombres de 0 à 9 sur une seule ligne séparés par des virgules.

**Exemple d'entrée :**
None

**Exemple de sortie :**
0,1,2,3,4,5,6,7,8,9
````

La sortie continue avec les sections `Common Mistakes`, `Review Comments` et
`Final Summary`, produites par le reviewer.

## Project Structure

```
.
├── agents/
│   ├── explainer_agent.py          Agent 1 : explication du sujet
│   ├── practice_designer_agent.py  Agent 2 : exercice pratique
│   └── reviewer_agent.py           Agent 3 : relecture et sections finales
├── tools/
│   ├── file_writer.py              Écriture de la fiche sur disque
│   └── validation.py               Contrôle des 8 sections requises
├── data/
│   └── topic_examples.json         Réservé à des sujets d'exemple, vide pour l'instant
├── output/
│   └── study_guide.md              Fiche générée par le dernier run
├── main.py                         Point d'entrée : enchaîne les agents
├── test_file_writer.py             Test manuel de l'outil d'écriture
├── test_validation.py              Test manuel de l'outil de validation
├── requirements.txt
├── .env.example                    Modèle de configuration, sans secret
└── README.md
```

## Agents

| Agent | Reçoit | Produit |
| --- | --- | --- |
| `explainer_agent` | Le sujet saisi | Les sections `Topic`, `Simple Explanation`, `Key Concepts` et `Example` |
| `practice_designer_agent` | Le sujet et l'explication | La section `Practice Exercise` |
| `reviewer_agent` | Le brouillon complet (explication + exercice) | Les sections `Common Mistakes`, `Review Comments` et `Final Summary` |

Le reviewer porte les trois dernières sections parce qu'il est le seul agent à
voir la fiche entière : `Common Mistakes` et `Final Summary` demandent cette vue
d'ensemble. Il commente et complète, il ne réécrit jamais le travail des autres.

## Tools

| Outil | Reçoit | Produit |
| --- | --- | --- |
| `save_markdown_file(file_path, content)` | Un chemin et le contenu Markdown | Écrit le fichier en UTF-8 en créant le dossier au besoin, et renvoie le chemin écrit, ou un message d'erreur lisible si l'écriture échoue |
| `validate_required_sections(markdown)` | La fiche assemblée | Un dictionnaire `{"valid": bool, "missing_sections": list}` listant les sections requises absentes |

Les deux outils sont en Python pur et déterministe : ils n'importent pas
`google.adk` et ne laissent remonter aucune exception. Chacun a son test manuel à
la racine, lançable sans agent :

```bash
python test_validation.py
python test_file_writer.py
```

## Self-Validation Checklist

- [x] Le projet tourne avec un modèle local, sans clé d'API ni service externe.
- [x] Trois agents distincts, une responsabilité chacun, un fichier par agent.
- [x] Deux outils déterministes en Python pur, sans import de `google.adk`.
- [x] Les agents s'exécutent en séquence, chacun recevant la sortie du précédent.
- [x] La fiche générée contient les 8 sections requises, dans l'ordre.
- [x] Les titres de sections sont en anglais, au caractère près.
- [x] La validation signale les sections manquantes sans bloquer l'écriture.
- [x] La fiche est enregistrée dans `output/study_guide.md`.
- [x] Sujet vide et variables d'environnement manquantes sont détectés avant tout appel au modèle.
- [x] Ollama injoignable, modèle absent et erreur d'écriture donnent un message lisible.
- [x] Aucun secret dans le code, dans le README ni dans `.env.example` ; le `.env` est ignoré par Git.
- [x] Chaque module et chaque fonction ont une docstring.

## Reflection

**Quelle est la différence entre un appel direct à un LLM et un agent ?**

Un appel direct envoie un texte au modèle et récupère sa réponse : je gère moi-même
le prompt, l'historique et le format attendu. Un agent est le modèle plus tout ce
qui l'entoure : une instruction système qui fixe son rôle une fois pour toutes,
une session qui garde le contexte, et la possibilité d'appeler des outils. Dans ce
projet, l'écart concret est que je ne répète pas le rôle à chaque appel : chaque
agent a son `instruction`, et `run_agent` se contente de lui passer le texte
d'entrée. La séquence d'agents me donne aussi trois prompts courts et spécialisés
au lieu d'un seul prompt géant qui devrait tout faire.

**Quel est le rôle de chaque agent ?**

L'explainer reçoit le sujet et pose les quatre premières sections : le sujet, une
explication simple, les concepts clés et un exemple de code. Le practice designer
reçoit le sujet et cette explication, et conçoit un exercice court réalisable en
10 à 20 minutes, sans donner la solution. Le reviewer reçoit le brouillon complet
et produit les trois dernières sections : les erreurs typiques de débutant sur le
sujet, ses remarques de relecture avec un verdict, et le résumé final. Chaque
agent a une seule responsabilité et ne refait pas le travail d'un autre.

**Quel est le rôle de chaque outil ?**

`validate_required_sections` vérifie que les 8 titres requis sont bien présents en
niveau 2 dans la fiche assemblée, et renvoie la liste de ceux qui manquent.
`save_markdown_file` écrit la fiche sur disque en UTF-8, crée le dossier de sortie
s'il n'existe pas, et renvoie un message lisible plutôt qu'une exception si
l'écriture échoue. Les deux sont déterministes : ils font un travail que le modèle
ferait moins bien et de façon variable.

**Qu'est-ce qui a été le plus difficile ?**

Obtenir des titres de sections stables. Le validateur exige la ligne exacte
`## Titre`, et le modèle avait tendance à remplacer `## Topic` par le sujet
lui-même, ou à ajouter des titres de niveau 2 en plus. J'ai dû écrire dans les
prompts que ces lignes sont des étiquettes fixes et non des variables, et interdire
explicitement tout autre titre de niveau 2. Le problème est revenu avec le reviewer,
qui reçoit du Markdown contenant déjà des titres et pouvait les recopier. La leçon
est que c'est aux agents de s'aligner sur le validateur, jamais l'inverse.

**Quelles sont les limites du modèle choisi ?**

Ma principale limite ne venait pas de la taille du modèle mais de son type. J'ai
commencé avec Qwen3, un modèle de raisonnement : il génère un bloc de réflexion
avant de répondre. Sur ma configuration, entièrement sur le CPU sous WSL et sans
GPU, ça rendait les runs impossibles à terminer. J'ai mesuré sur la consigne
« compte de 1 à 20 » : Qwen3 4B a généré 1213 tokens en 3 min 20, là où Qwen2.5 3B
en a généré 127 en 14,7 s. Qwen3 produisait environ 20 fois plus de tokens qu'il
n'en sortait, et `strip_thinking` jetait ensuite tout ce que j'avais payé en temps
de calcul. J'ai essayé l'interrupteur `/no_think`, sans succès : le modèle l'a lu
comme du texte ordinaire et a réfléchi deux fois plus.

Je suis passé à Qwen2.5 3B, qui ne réfléchit pas. J'avais initialement retenu un
modèle supportant les outils, mais c'était un faux critère : mes agents n'appellent
aucun outil, j'invoque `save_markdown_file` et `validate_required_sections` depuis
`main.py` en Python. Je payais donc une capacité dont je ne me sers pas.

Les limites qui restent : la fenêtre de contexte est de 4096 tokens, ce qui suffit
ici mais contraindrait une fiche plus longue, puisque le reviewer reçoit tout ce
que les deux autres ont écrit. Et la sortie varie d'un run à l'autre : deux runs
sur le même sujet ne donnent pas la même fiche, et le respect du format des titres
n'est jamais garanti à 100 %.

Ce changement de modèle n'est pas un gain net, c'est un arbitrage, et je le documente
comme tel. Qwen3 4B écrivait un meilleur contenu, mais son raisonnement lui coûtait
environ 20 fois plus de tokens que ce qu'il produisait, et un run complet dépassait
l'heure sur mon CPU. Qwen2.5 3B fait le même run en 3 minutes environ, mais il
hallucine : il a écrit qu'il fallait terminer une boucle `for` par un point-virgule
en Python, ce qui est faux, et il laisse tomber des consignes de mes prompts, comme
le verdict final du reviewer. J'ai donc échangé de la qualité contre du temps de
calcul. Le projet tourne sur Qwen2.5 3B pour cette raison : sur cette machine, un
run qui se termine et qu'il faut relire vaut mieux qu'un run plus juste qui
n'aboutit pas.

## Known Limitations

- **Lenteur** : le modèle tourne en local via Ollama, à 100 % sur le CPU sous WSL,
  sans accélération GPU. Un run complet reste long, et chaque agent se compte en
  minutes.
- **Le choix d'un modèle de raisonnement était une erreur** : le projet a d'abord
  tourné sous Qwen3, un modèle qui produit un bloc de réflexion avant de répondre.
  Mesure sur la consigne « compte de 1 à 20 » : Qwen3 4B a généré 1213 tokens en
  3 min 20, contre 127 tokens en 14,7 s pour Qwen2.5 3B. Qwen3 générait environ
  20 fois plus de tokens qu'il n'en sortait réellement : la réflexion était payée
  en temps de calcul, puis jetée par `strip_thinking`. L'interrupteur `/no_think`
  n'a rien réglé, le modèle lisant la consigne comme du texte ordinaire et
  réfléchissant deux fois plus. Le projet est passé à Qwen2.5 3B, qui ne réfléchit
  pas.
- **Le support des outils n'était pas nécessaire** : les agents de ce projet
  n'appellent aucun outil. `save_markdown_file` et `validate_required_sections`
  sont invoqués depuis `main.py`, en Python, une fois les agents terminés. Le
  critère « le modèle supporte les tools » n'avait donc pas à peser dans le choix,
  et il a contribué à retenir un modèle inutilement lourd.
- **Le contenu produit peut être faux** : rien ne vérifie l'exactitude technique de
  la fiche. Sur le run « les boucles for en Python », le modèle a écrit dans
  `Common Mistakes` : « Oublier de terminer la boucle avec un point-virgule. »
  Cette règle n'existe pas en Python. La fiche est structurellement valide et
  factuellement fausse : la validation ne contrôle que la présence des titres,
  jamais ce qu'il y a dessous.
- **Les consignes des prompts sont perdues en partie** : le prompt du reviewer exige
  un verdict final, `approuvé` ou `à réviser`. Il n'apparaît pas dans la sortie. Le
  même prompt interdit les remarques vagues et impose de nommer la section visée ;
  les remarques obtenues restent générales, du type « pourrait être améliorée pour
  inclure des cas plus complexes ». Un modèle de 3 milliards de paramètres suit
  moins de règles simultanées qu'un modèle plus gros : plus le prompt contient de
  contraintes, plus il en laisse tomber.
- **Personne ne relit le reviewer** : il est le dernier agent de la chaîne. Ses trois
  sections partent directement dans la fiche finale, sans qu'aucun agent ne les
  examine. C'est la raison pour laquelle l'erreur du point-virgule est passée : elle
  a été écrite précisément à l'endroit que plus rien ne contrôle. La chaîne relit ce
  que produisent les deux premiers agents, pas ce que produit le troisième.
- **Fenêtre de contexte de 4096 tokens** : le reviewer reçoit l'explication et
  l'exercice entiers. Sur un sujet très long, le brouillon pourrait approcher cette
  limite.
- **Sortie non reproductible** : deux runs sur le même sujet ne produisent pas la
  même fiche. Le respect du format des titres dépend du modèle, et la validation
  peut signaler une section manquante sur un run et pas sur le suivant.
- **Aucune correction automatique** : les remarques du reviewer sont écrites dans
  la fiche, mais rien ne les applique. Le verdict « à réviser » n'entraîne ni
  reprise, ni second passage. Corriger reste à la charge du lecteur.
- **Validation non bloquante** : si une section manque, le programme le signale et
  enregistre la fiche quand même.
- **`data/topic_examples.json` est vide** : le sujet est saisi au clavier, aucun
  jeu de sujets d'exemple n'est chargé pour l'instant.

## Troubleshooting

**Le programme affiche « Configuration incomplète, variables d'environnement manquantes ».**
Le fichier `.env` est absent ou incomplet. Le créer à partir du modèle avec
`cp .env.example .env`, et vérifier qu'il définit bien `OLLAMA_API_BASE` et
`MODEL_NAME`.

**Le programme affiche « Sujet vide ».**
Aucun sujet n'a été saisi, ou seulement des espaces. Relancer et entrer un sujet,
par exemple `les boucles for en Python`.

**Le programme affiche « Le modèle local n'a pas répondu » avec `Cannot connect to host localhost:11434`.**
Le service Ollama ne tourne pas. Vérifier qu'il répond avec `ollama list`, ou
tester l'API directement avec `curl http://localhost:11434/api/tags`.

**Le programme affiche « Le modèle local n'a pas répondu » avec `model '...' not found`.**
Ollama tourne, mais le modèle nommé dans `MODEL_NAME` n'est pas téléchargé. Lancer
`ollama pull qwen2.5:3b`, et vérifier que le tag correspond à celui du `.env`.

**Plusieurs tracebacks s'affichent avant le message d'erreur lisible.**
C'est le logging interne de LiteLLM, qui imprime ses tentatives de reconnexion
avant que l'erreur soit attrapée. Le message utile est le dernier affiché : c'est
celui-là qu'il faut lire.

**Le programme affiche « Validation : sections requises manquantes ».**
Le modèle n'a pas produit un des 8 titres au format exact attendu. La fiche est
tout de même enregistrée. Relancer donne souvent une sortie correcte, puisque le
modèle varie d'un run à l'autre.

**Le programme affiche « Erreur d'écriture dans output/study_guide.md ».**
Le dossier `output/` n'est pas accessible en écriture, ou le disque est plein.
Vérifier les droits sur le dossier.

**L'installation d'Ollama échoue avec `This version requires zstd for extraction`.**
Installer `zstd` avec `sudo apt-get install zstd`, puis relancer la commande
d'installation.

**Le modèle part en boucle d'appels d'outils.**
Le préfixe de `MODEL_NAME` est probablement `ollama/` au lieu de `ollama_chat/`.
Corriger la valeur dans le `.env`.
