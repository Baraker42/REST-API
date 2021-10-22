from flask import Flask
from flask import request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

movies = [
    {
        'id': 1,
        'name': 'The Last Boy Scout',
        'name_cs': 'Poslední skaut',
        'year': 1991,
        'imdb_url': 'https://www.imdb.com/title/tt0102266/',
        'csfd_url': 'https://www.csfd.cz/film/8283-posledni-skaut/',
    },
    {
        'id': 2,
        'name': 'Fight Club',
        'name_cs': 'Klub rváčů',
        'year': 1999,
        'imdb_url': 'https://www.imdb.com/title/tt0137523/',
        'csfd_url': 'https://www.csfd.cz/film/2667-klub-rvacu/prehled/',
    },
    {
        'id': 3,
        'name': 'Sharknado',
        'name_cs': 'Žralokonádo',
        'year': 2013,
        'imdb_url': 'https://www.imdb.com/title/tt2724064/',
        'csfd_url': 'https://www.csfd.cz/film/343017-zralokonado/',
    },
    {
        'id': 4,
        'name': 'Mega Shark vs. Giant Octopus',
        'name_cs': 'Megažralok vs. obří chobotnice',
        'year': 2009,
        'imdb_url': 'https://www.imdb.com/title/tt1350498/',
        'csfd_url': 'https://www.csfd.cz/film/258268-megazralok-vs-obri-chobotnice/',
    },
]

def filter_movies(movies, name):
    if name is not None:
        filtered_movies = []
        for movie in movies:
            if name in movie["name"].lower():
                filtered_movies.append(movie)
        return filtered_movies
    else:
        return movies

def get_movie_by_id(movies, id):
    for movie in movies:
        if movie["id"] == id:
            return movie


class Movies_filter(Resource):
    def get(self):
        name = request.args.get('name')
        resultado = filter_movies(movies, name)
        return resultado

class MovieDetailResource(Resource):
    def get(self,id):
        return get_movie_by_id(movies, id)

api.add_resource(Movies_filter, "/","/movies")
api.add_resource(MovieDetailResource,"/movies/<int:id>",endpoint="movies")
if __name__ == '__main__':
    app.run(debug=True)