from functools import reduce
from PIL import Image
import requests
from io import BytesIO

def es_palindromo(s: str) -> bool:
    return s == s[::-1]

def palindromos(lista: list) -> list:
    return list(map(es_palindromo, lista))

print(palindromos(["ana", "radar", "palabra", "otto", "python"]))
print(palindromos(["level", "world", "madam", "racecar", "hello"]))
print(palindromos(["refer", "deified", "civic", "rotator", "nonpalindrome"]))
print(palindromos(["abccba", "xyzzyx", "abcd", "a", "aa"]))
print(palindromos(["wow", "bob", "pop", "nope", "yes"]))

def impares_de(numeros: list) -> list:
    return list(filter(lambda x: x % 2 != 0, numeros))

print(impares_de([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
print(impares_de([11, 22, 33, 44, 55, 66, 77, 88, 99]))
print(impares_de([100, 101, 102, 103, 104, 105, 106, 107, 108, 109]))
print(impares_de([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
print(impares_de([23, 45, 67, 89, 12, 34, 56, 78, 91]))

def cuadrados_sumados(n: int) -> int:
    return sum(map(lambda x: x**2, range(1, n + 1)))

print("Cuadrados sumados: ", cuadrados_sumados(5))
print("Cuadrados sumados: ", cuadrados_sumados(10))
print("Cuadrados sumados: ", cuadrados_sumados(1))
print("Cuadrados sumados: ", cuadrados_sumados(0))
print("Cuadrados sumados: ", cuadrados_sumados(7))

def factorial(n: int) -> int:
    return reduce(lambda x, y: x * y, range(1, n + 1), 1)

print("Factorial: ", factorial(5))
print("Factorial: ", factorial(7))
print("Factorial: ", factorial(0))
print("Factorial: ", factorial(1))
print("Factorial: ", factorial(10))

def img_to_bw(image_source_function):
    def inner():
        try:
            img = image_source_function()
            img = img.convert("L")
        except Exception as e:
            print(f"Error: {e}")
            return None
        
        def show_result():
            if img:
                img.show()
            else:
                print("No se pudo obtener la imagen.")
        
        return show_result

    return inner

def get_local_image():
    return Image.open("C:/Users/asier/Documents/Parad. Prog/image3.jpg")

def get_web_image():
    response = requests.get('https://blockbrite.vercel.app/static/media/zeus.f9ae6f5b65451a91a350.png')
    return Image.open(BytesIO(response.content))

convert_local_image = img_to_bw(get_local_image)
result_local_image = convert_local_image()
result_local_image()

convert_web_image = img_to_bw(get_web_image)
result_web_image = convert_web_image()
result_web_image()
