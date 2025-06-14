from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("OMDB_API_KEY")

movie_title = "Matrix"
url = f"https://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print(data)
    print(f"Title: {data.get('Title')}")
    print(f"Year: {data.get('Year')}")
    print(f"Director: {data.get('Director')}")
    print(f"Genre: {data.get('Genre')}")
    print(f"IMDb Rating: {data.get('imdbRating')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
