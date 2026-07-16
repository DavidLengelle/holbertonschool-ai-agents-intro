## les boucles for en Python  
## Simple Explanation  
Les boucles `for` en Python permettent de répéter un bloc de code pour chaque élément d'une liste, d'une chaîne de caractères ou d'un autre objet itérable. On utilise la syntaxe `for` suivi d'une variable qui représente chaque élément à chaque itération. Cela aide à automatiser des tâches comme afficher tous les éléments d'une liste sans écrire plusieurs fois le même code.  

## Key Concepts  
- **Itération** : Répétition d'une action pour chaque élément d'une collection.  
- **Séquence** : Liste, chaîne de caractères, ou autre objet pouvant être parcouru (ex: `range()`).  
- **Variable d'itération** : Variable qui stocke temporairement chaque élément pendant l'itération.  
- **Syntaxe** : `for variable in séquence:` suivi d'un bloc de code indenté.  
- **Indentation** : Obligatoire pour définir le bloc à exécuter à chaque itération.  

## Example  
```python  
fruits = [" pomme", " banane", " orange"]  
for fruit in fruits:  
    print(fruit)  
```  
Ce code affiche chaque élément de la liste `fruits` sur une ligne différente.

## Practice Exercise

Task: Créez une liste de 5 nombres entiers et affichez chaque nombre à l'aide d'une boucle for.

Expected input: Une liste de 5 nombres entiers, par exemple [10, 20, 30, 40, 50].

Expected output: Chaque nombre affiché sur une ligne différente, comme :
10
20
30
40
50

Hints: Assurez-vous de bien indenter le bloc de code après la boucle for. Utilisez la fonction print() pour afficher chaque élément.