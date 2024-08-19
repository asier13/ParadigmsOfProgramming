import requests

def get_movie_data(movie_title, api_key, on_success=None, on_error=None):
    omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"

    response = requests.get(omdb_url)
    data = response.json()

    if response.status_code == 200 and data.get("Response") == "True":
        if on_success:
            on_success(data)
    else:

        if on_error:
            on_error(data)

def show_movie_info(movie_data):
    print("Información de la película:")
    print(f"Título: {movie_data['Title']}")
    print(f"Año: {movie_data['Year']}")
    print(f"Género: {movie_data['Genre']}")
    print(f"Clasificacion: {movie_data['Rated']}")
    print(f"Director: {movie_data['Director']}")
    print(f"Sinopsis: {movie_data['Plot']}")
    print(f"Puntuacion IMDB: {movie_data['imdbRating']}")
    print(f"Duración: {movie_data['Runtime']}")
    print(f"Premios: {movie_data['Awards']}")
    

def show_error_message(error_data):
    if error_data.get("Error"):
        print(f"Error: {error_data['Error']}")
    else:
        print("Se produjo un error desconocido.")

def main():
    movie_title = input("Introduce el título de la película: ")
    api_key = "d2e223fb" 

    get_movie_data(
        movie_title,
        api_key,
        on_success=show_movie_info,
        on_error=show_error_message
    )
    
main()
    