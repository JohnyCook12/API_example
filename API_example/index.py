
"""
Making simple API based on Falcon.
Displays personal data and list of films (as JSON)

"""

import falcon, json


my_data_dict = {'name': 'Johny', 'surname': 'Cook', 'shoe_size': '46'}          # Data as dict
movies_list = [ {'name': 'Brave New World', 'year': '2020'},
                {'name': 'Papillon', 'year': '2017'},
                {'name': 'The Youth', 'year': '2015'}]                          # list of dicts


def filter_movies(movies, name):                            # filtering. E.G.: you write /movies?name=pap   -> "Papillon"
    if name == None:
        return movies

    for movie in movies_list:
        name_string = movie.get('name').lower()             # all to lowercase
        if name_string.find(str(name).lower()) != -1:       # if found:
            return movie.get('name')
    return None


class PersonalDetailsResource():                            # info class - ends with "Resource"
   def on_get(self, request, response):
       response.status = "200 OK"                                               # unnecessary
       response.set_header('Content-Type','text/plain')                         # unnecessary
       response.body = json.dumps(my_data_dict)                                 # display data (+ make string from dict)


class MoviesResource():                                     # info class - ends with "Resource"
   def on_get(self, request, response):
       name = request.get_param('name')                                         # reads PARAMETERS
       response.body = json.dumps(filter_movies(movies_list, name))


app = falcon.API()
app.add_route('/', PersonalDetailsResource())               # define ROUTE
app.add_route('/movies', MoviesResource())                  # define ROUTE
