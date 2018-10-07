
class Actor:
    def __init__(self):
        self.name = ""
        self.birthday = ""
        self.age = -1
        self.movies_edge = {}  # dict(movie_name: weight)


class Movie:
    def __init__(self):
        self.name = ""
        self.gross = -1
        self.year = ""
        self.actors_edge = {}  # dict(actor_name: weight)


class Graph:
    def __init__(self):
        self.actors = []
        self.movies = []

    def add_actor(self, actor):
        self.actors.append(actor)

    def add_movie(self, movie):
        self.movies.append(movie)

    def add_edges(self, actor, movie):
        weight = (200-actor.age)*10**4 + movie.gross * 0.00001
        if movie.name not in actor.movies_edge:
            actor.movies_edge[movie.name] = weight

        if actor.name not in movie.actors_edge:
            movie.actors_edge[actor.name] = weight
