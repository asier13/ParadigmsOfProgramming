
animals = ["ferret", "vole", "dog", "gecko"]
sorted(animals)
print(animals)

sorted(animals, key=len)
print(animals)

sorted(animals, key=len, reverse=True)
print(animals)

def reverse_len(cadena):
    return 1

    
animals = ["ferret", "vole", "dog", "gecko"]
print(sorted(animals, key=reverse_len))
