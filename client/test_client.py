import requests



response = requests.get("http://Lenovo_X1Carbon:8080")                      # READ personal info
print(response.status_code)
print(response.headers)
print(response.text)                # display body as TEXT  (json)
print(response.json())              # display body as DICT  (dict from json)



response_movies = requests.get("http://Lenovo_X1Carbon:8080/movies")        # READ movies
movies = response_movies.json()     # READ body as DICT  (dict from json)
movies_name_list = []
for movie in movies:
    movies_name_list.append(movie['name'])
print(movies_name_list)