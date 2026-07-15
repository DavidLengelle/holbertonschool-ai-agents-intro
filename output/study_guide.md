## Python f-strings  
## Simple Explanation  
Les f-strings (ou f-strings) sont une façon facile de créer des chaînes de caractères en Python qui intègrent des variables ou des expressions directement. Elles commencent par un `f` suivi de guillemets, et permettent d'afficher des valeurs dynamiques sans utiliser de fonctions comme `format()`. C'est pratique pour créer des messages ou des calculs en temps réel.  

## Key Concepts  
- **Variables et expressions** : On peut insérer des variables ou des calculs entre accolades `{}`.  
- **Syntaxe simplifiée** : La structure est plus courte que les méthodes traditionnelles.  
- **Dynamisme** : Les valeurs changent automatiquement si les variables sont modifiées.  
- **Compatibilité** : Disponible à partir de la version Python 3.6.  
- **Lecture facile** : Le code reste clair et proche du langage naturel.  

## Example  
```python  
nom = "Alice"  
print(f"Bonjour, {nom}!")  
# Affiche : Bonjour, Alice!  
```