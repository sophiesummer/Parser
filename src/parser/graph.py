import json


class Actor:
    def __init__(self, name, birthday, age, movies):
        self.name = name
        self.birthday = birthday
        self.age = age
        self.movie_name = movies
        self.movies_edge = {}  # dict(movie_name: weight)


class Movie:
    def __init__(self, name, gross, year, actors):
        self.name = name
        self.gross = gross
        self.year = year
        self.actor_name = actors
        self.actors_edge = {}  # dict(actor_name: weight)


class Graph:
    def __init__(self):
        self.actors = []
        self.movies = []
        self.helper_set = {}
        self.helper_actor_set = {}

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

    def get_graph_data(self):
        f = open('data.json')
        graph_data = json.loads(f.read())
        return graph_data

    def construct_graph(self):
        graph_data = self.get_graph_data()
        actor_data = graph_data[0]
        movie_data = graph_data[1]
        self.construct_actors(actor_data)
        self.construct_movies(movie_data)
        self.construct_edges()

    def construct_actors(self, actor_data):
        for actor in actor_data:
            actor_obj = Actor(actor['name'], actor['birthday'], actor['age'], actor['movies'])
            self.actors.append(actor_obj)
            self.helper_actor_set[actor['name']] = actor_obj

    def construct_movies(self, movie_data):
        for movie in movie_data:
            movie_obj = Movie(movie['name'], movie['gross'], movie['year'], movie['actors'])
            self.movies.append(movie_obj)
            self.helper_set[movie['name']] = movie_obj

    def construct_edges(self):
        for actor in self.actors:
            movies_name_list = actor.movie_name
            for movie_name in movies_name_list:
                if movie_name in self.helper_set:
                    movie_obj = self.helper_set[movie_name]
                    self.add_edges(actor, movie_obj)

    def get_gross(self, movie_name):
        if movie_name in self.helper_set:
            movie_obj = self.helper_set[movie_name]
            return movie_obj.gross
        else:
            print("The movie not exists")

    def get_all_movie_of_actor(self, actor_name):
        if actor_name in self.helper_actor_set:
            actor_obj = self.helper_actor_set[actor_name]
            movies = actor_obj.movie_name
            for m in movies:
                print(m)
        else:
            print('The actor not exists')

    def get_all_actor_of_movie(self, movie_name):
        if movie_name in self.helper_set:
            movie_obj = self.helper_set[movie_name]
            actors = movie_obj.actor_name
            for a in actors:
                print(a)
        else:
            print('The movie not exists')

    def all_movie_given_year(self, year):
        count = 0
        for movie_obj in self.movies:
            if movie_obj.year == year:
                count += 1
                print(movie_obj.name)
        if count == 0:
            print('No movie in this year')

    def oldest_X_actors(self, number):
        self.actors.sort(key = lambda  x: x.age, reverse=True)
        for i in range(min(number,len(self.actors))):
            print(self.actors[i].name + ' : ' + str(self.actors[i].age))

    def actors_given_year(self, year):
        count = 0
        for actor in self.actors:
            for movie_name in actor.movie_name:
                if movie_name not in self.helper_set:
                    continue
                movie_obj = self.helper_set[movie_name]
                if movie_obj.year == year:
                    count += 1
                    print(actor.name + " : " + movie_obj.name)
        if count == 0:
            print('No actor had works in this year')

    def top_X_actors_with_most_gross(self, number):
        if number > len(self.actors):
            number = len(self.actors)
        actor_gross = []
        for actor in self.actors:
            ele = {}
            ele['total_gross'] = 0
            ele['actor_name'] = actor.name
            for movie in actor.movie_name:
                if movie in self.helper_set:
                    movie_obj = self.helper_set[movie]
                    if movie_obj.gross != -1:
                        ele['total_gross'] += movie_obj.gross
            actor_gross.append(ele)
        actor_gross.sort(key = lambda x: x['total_gross'], reverse=True)
        for i in range(number):
            print(actor_gross[i]['actor_name'] + " : " + str(actor_gross[i]['total_gross']))

    def start_query(self):
        self.construct_graph()
        num = 0
        while num != -1:
            print("Please input a query number: ")
            try:
                num = int(input())
            except:
                num = 0

            if num == 1:
                print('Please input a movie name: ')
                movie_name = input()
                result = self.get_gross(movie_name)
                if result is not None:
                    print(result)

            elif num == 2:
                print('Please input an actor name: ')
                actor_name = input()
                self.get_all_movie_of_actor(actor_name)

            elif num == 3:
                print('Please input a movie name: ')
                movie_name = input()
                self.get_all_actor_of_movie(movie_name)

            elif num == 4:
                print('Please input the number of actors: ')
                number = input()
                try:
                    number = int(number)
                except:
                    print('the number is invalid')
                else:
                    if number < 0 :
                        print('Please input a positive number: ')
                    else:
                        self.top_X_actors_with_most_gross(number)

            elif num == 5:
                print('Please input the number of actors: ')
                number = input()
                try:
                    number = int(number)
                except:
                    print('the number is illegal')
                else:
                    if number < 0 :
                        print('Please input a positive number: ')
                    else:
                        self.oldest_X_actors(number)

            elif num == 6:
                print('Please input a year: ')
                year = input()
                try:
                    year = int(year)
                except:
                    print('the year is illegal')
                else:
                    self.all_movie_given_year(year)

            elif num == 7:
                print('Please input a year: ')
                year = input()
                try:
                    year = int(year)
                except:
                    print('the year is illegal')
                else:
                    self.actors_given_year(year)


graph = Graph()
graph.start_query()