import json


# Actor class prepared for creating an Actor object
class Actor:
    def __init__(self, name, age, gross, movies):
        self.name = name
        self.age = age
        self.gross = gross
        self.movie_name = movies
        self.movies_edge = {}  # dict(movie_name: weight)


# Movie class prepared for creating a Movie object
class Movie:
    def __init__(self, name, gross, year, actors, url):
        self.name = name
        self.gross = gross
        self.year = year
        self.actor_name = actors
        self.actors_edge = {}  # dict(actor_name: weight)
        self.url = url


# Graph class prepared for creating a Graph object from scraped data
class Graph:
    def __init__(self):
        self.actors = []
        self.movies = []
        self.helper_set = {}
        self.helper_actor_set = {}

    # add an actor object to graph actor array
    # :param actor: actor object which to be added in graph
    def add_actor(self, actor):
        self.actors.append(actor)

    # add a movie object to graph movie array
    # :param movie: movie object which to be added in graph
    def add_movie(self, movie):
        self.movies.append(movie)

    # add edges between to linked actor and movie with weight
    # :param actor: actor object to be connected with a movie
    # :param movie: movie object to be connected with a actor
    def add_edges(self, actor, movie):
        weight = (200-actor.age)*10**4 + movie.gross * 0.00001
        if movie.name not in actor.movies_edge:
            actor.movies_edge[movie.name] = weight

        if actor.name not in movie.actors_edge:
            movie.actors_edge[actor.name] = weight

    # get data from json file
    def get_graph_data(self):
        f = open('data.json')
        graph_data = json.loads(f.read())
        return graph_data

    # construct whole graph structure
    def construct_graph(self):
        graph_data = self.get_graph_data()
        actor_data = graph_data[0]
        movie_data = graph_data[1]
        self.construct_actors(actor_data)
        self.construct_movies(movie_data)
        self.construct_edges()

    # put actor information into individual Actor object and insert into graph
    # :param actor_data: actor data part in json file
    def construct_actors(self, actor_data):
        for actor_name in actor_data:
            content = actor_data[actor_name]
            gross = content['total_gross']
            if content['total_gross'] < 10000:
                gross = content['total_gross'] * 10**6
            actor_obj = Actor(content['name'], content['age'], gross, content['movies'])
            self.actors.append(actor_obj)
            self.helper_actor_set[content['name']] = actor_obj

    # put movie information into individual Movie object and insert into graph
    # :param movie_data: actor movie part in json file
    def construct_movies(self, movie_data):
        for movie_name in movie_data:
            content = movie_data[movie_name]
            gross = content['box_office']
            if gross < 10000:
                gross *= 10**6
            movie_obj = Movie(content['name'], gross, content['year'], content['actors'], content['wiki_page'])
            self.movies.append(movie_obj)
            self.helper_set[content['name']] = movie_obj

    # generate edges between connected movies and actors
    def construct_edges(self):
        for actor in self.actors:
            movies_name_list = actor.movie_name
            for movie_name in movies_name_list:
                if movie_name in self.helper_set:
                    movie_obj = self.helper_set[movie_name]
                    self.add_edges(actor, movie_obj)


