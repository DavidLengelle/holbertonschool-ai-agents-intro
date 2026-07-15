## Python f-strings  
## Simple Explanation  
Les f-strings (ou f-strings) permettent d'intégrer des variables ou des expressions directement dans une chaîne de caractères en Python. Cela rend le code plus simple et plus lisible. Au lieu de concaténer des chaînes ou d'utiliser la méthode format(), on utilise des accolades {} pour insérer des valeurs. Cette méthode est couramment utilisée pour afficher des messages dynamiques.  

## Key Concepts  
- Une f-string commence par le caractère `f` suivi d'une chaîne de caractères.  
- Les variables ou expressions sont placées entre accolades `{}` dans la chaîne.  
- On peut calculer des expressions directement dans les accolades (ex: `{2 + 2}`).  
- Les f-strings sont plus rapides et plus concises que les méthodes traditionnelles.  

## Example  
```python  
nom = "Alice"  
age = 25  
print(f"{nom} a {age} ans")  
# Sortie: Alice a 25 ans  
```