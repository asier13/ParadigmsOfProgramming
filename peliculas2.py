import requests
import os

def get_movie_poster(movie_title, api_key, save_path):
    
    omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}&plot=short"

    response = requests.get(omdb_url)
    data = response.json()

    if response.status_code == 200 and data.get("Response") == "True" and data.get("Poster"):
        poster_url = data["Poster"]
        
        response = requests.get(poster_url)
        if response.status_code == 200:
            with open(save_path, "wb") as file:
                file.write(response.content)
                print(f"Póster guardado en {save_path}")
        else:
            print("No se pudo descargar el póster.")
    else:
        print("No se encontró el póster para esta película.")

def main():
    
    movie_title = input("Introduce el título de la película: ")
    api_key = "d2e223fb" 
    save_path = "image4.jpg"  

    get_movie_poster(movie_title, api_key, save_path)


main()