
"""
Making simple API based on Falcon.
Displays personal data and list of films (as JSON)

"""

import falcon, json


my_data_dict = {'name': 'Johny', 'surname': 'Cook', 'shoe_size': '46', 'movies_watchlist': ''}          # Data as dict
movies_list = [ {'name': 'Brave New World', 'year': '2020', 'id': 1, 'csfd_url':'https://www.csfd.cz/film/850640-brave-new-world/prehled/'},
                {'name': 'Papillon', 'year': '2017', 'id': 2, 'csfd_url':'https://www.csfd.cz/film/535735-motylek/prehled/'},
                {'name': 'The Youth', 'year': '2015', 'id': 3, 'csfd_url':'https://www.csfd.cz/film/356139-mladi/prehled/'}]                          # Data as list of dicts

def id_exists(movies: list, id: int) -> bool:
    for movie in movies:
        if movie.get('id') == id:
            return True
    return False


def create_movie_id(movies: list) -> int:                   # return ID for new movie (current max ID + 1)
    all_id_list = []
    for movie in movies:
        all_id_list.append(movie['id'])
    return max(all_id_list)+1


def filter_movies(movies: list, name: str) -> list:                            # filtering. E.G.: you write /movies?name=pap   -> DICT of "Papillon"
    list_of_results = []
    if name == None:                                        # no parameter -> all movies
        # for movie in movies:
        #    list_of_results.append(movie.get('name'))
        return movies     # list_of_results

    for movie in movies:
        name_string = movie.get('name').lower()             # all to lowercase
        if name_string.find(str(name).lower()) != -1:       # if found:
            list_of_results.append(movie)                   # append the DICT
    return list_of_results


def get_movie_by_id(movies: list, id_input: int) -> dict:                      # id -> movie
    if id_input == None:
        return movies
    for movie in movies:
        if id_input == movie.get('id'):                     # if found:
            return movie
    response.status = "404 Not Found"
    return


def represent_movies(movies: list, base_url: str) -> str:                     # DICT of all movies info -> LIST of DICTS with only NAMEs + URLs (shorter!)
    local_movies_list = []
    for movie in movies:
        local_movies_list.append({
            'name': movie['name'],
            'url': '{0}/movies/{1}'.format(base_url, movie['id']),
        })
    return json.dumps(local_movies_list)                    # finally convert to JSON



"""=======   RESOURCES - classes with data - ends with "Resource"   ======="""

class PersonalDetailsResource():                            # My Personal details
   def on_get(self, request, response):

       my_data_dict['movies_watchlist'] = f'{request.prefix}/movies'            # adds some data to resource dict

       response.status = "200 OK"                                               # (unnecessary - header)
       response.set_header('Content-Type','text/plain')                         # (unnecessary - header)

       response.body = json.dumps(my_data_dict)                                 # display data (+ make string from dict)


class MoviesResource():                                     # Brief info about (all or selected) movies
   def on_get(self, request, response):
       name = request.get_param('name')                     # reads PARAMETERS
       base_url = request.prefix                            # get url of our current server

       filtered_movies = filter_movies(movies_list, name)   # filter movies we want
       response.body = represent_movies(filtered_movies, base_url)          # create "short info" - list of "NAME + URL"

   def on_post(self, request, response):
        movie = json.load(request.bounded_stream)           # reads the BODY. = content we want to add. And transfer it JSON -> DICT
        movie['id'] = create_movie_id(movies_list)          # add new ID
        movies_list.append(movie)

        movie_url = f'{request.prefix}/movies/{movie["id"]}'    #just create url for new movie
        movie_repr = dict(movie)
        movie_repr['url'] = movie_url

        response.status = '201 Created'                     # return correct HEADER
        response.set_header('Location', movie_url)          # return movie url
        response.body = json.dumps(movie_repr)







class MovieDetailsResource():                               # All movie info
   def on_get(self, request, response, id):                 # last param = id       -> movie
       if id_exists(movies_list, id) == True:               # returns movie only if ID exists

           movie = get_movie_by_id(movies_list, id)
           movie['self_url'] = f'{request.prefix}/{id}'     # add self_url to movie DICT

           response.body = json.dumps(movie)
       else:
           response.status = "404 Not Found"



app = falcon.API()
app.add_route('/', PersonalDetailsResource())               # define ROUTE      - for personal info
app.add_route('/movies', MoviesResource())                  # define ROUTE      - displays all movies with all info
app.add_route('/movies/{id:int}', MovieDetailsResource())   # define ROUTES      - TEMPLATE! - creates ROUTE for EACH movie! (based on it's ID)

