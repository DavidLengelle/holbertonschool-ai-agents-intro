## Topic  
Les boucles for en Python  

## Simple Explanation  
Les boucles `for` permettent de répéter un bloc de code pour chaque élément d'une liste, d'une chaîne de caractères, ou d'un autre objet iterable. Elles sont utiles quand on sait à l'avance combien de fois le code doit s'exécuter. Par exemple, on peut parcourir tous les éléments d'une liste ou afficher chaque caractère d'une phrase.  

## Key Concepts  
- Une boucle `for` itère sur chaque élément d'une séquence (liste, chaîne, etc.).  
- La syntaxe est : `for variable in séquence:` suivi d'un bloc de code indenté.  
- La variable de boucle représente l'élément courant de la séquence.  
- L'indentation (espaces ou tabulation) détermine les instructions incluses dans la boucle.  

## Example  
```python
fruits = ['apple', 'banana', 'cherry']
for fruit in fruits:
    print(fruit)
```

## Practice Exercise

Task: Écrivez un programme qui affiche chaque caractère de la chaîne `"Python est génial"` sur une ligne différente.  

Expected input: La chaîne `"Python est génial"`.  
Expected output:  
P  
y  
t  
h  
o  
n  
  
e  
s  
t  
  
g  
é  
n  
i  
a  
l  

Hints: Utilisez une boucle `for` avec la chaîne comme séquence. N'oubliez pas d'indenter correctement le code.

## Review Comments
- La section *Simple Explanation* pourrait être plus précise en soulignant que les boucles `for` itèrent sur des séquences (listes, chaînes, etc.), et non nécessairement en connaissant le nombre d'itérations à l'avance. L'explication actuelle peut être source de confusion entre les boucles `for` et les boucles `while`.
- La section *Practice Exercise* a un expected output incorrect : les espaces dans la chaîne `"Python est génial"` devraient être affichés comme des lignes avec des espaces, pas des lignes vides. L'output attendu doit refléter exactement chaque caractère, y compris les espaces.
- La section *Example* pourrait inclure un exemple avec une chaîne de caractères pour illustrer l'utilisation des boucles `for` avec des chaînes, ce qui renforcerait la compréhension des différents types d'itérables.

à réviser