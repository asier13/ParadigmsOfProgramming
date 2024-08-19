def edad_de_mi_mascota(func, num):
    return func(num)

def perro(num):
    return 7*num

def gato(num):
    return 5*num

def pez(num):
    return 12*num

# Crear un diccionario que asocie el nombre de la mascota con la función correspondiente
mascotas = {
    "perro": perro,
    "gato": gato,
    "pez": pez
}

masc = input("Introduce tu mascota: ").lower()  # Convertir a minúsculas para evitar errores de mayúsculas/minúsculas
num = int(input(f"Introduce la edad de tu {masc}: "))

# Verificar si la mascota ingresada está en el diccionario
if masc in mascotas:
    resultado = edad_de_mi_mascota(mascotas[masc], num)
    print(f'Edad de mi {masc} de {num} años: {resultado}')
else:
    print(f"No sé cuántos años humanos tiene un {masc}.")
