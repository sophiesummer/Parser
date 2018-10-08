from src.parser.graph import Graph


# graph query interface entry
def start_query(graph):
    graph.construct_graph()
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
            result = graph.get_gross(movie_name)
            if result is not None:
                print(result)

        elif num == 2:
            print('Please input an actor name: ')
            actor_name = input()
            graph.get_all_movie_of_actor(actor_name)

        elif num == 3:
            print('Please input a movie name: ')
            movie_name = input()
            graph.get_all_actor_of_movie(movie_name)

        elif num == 4:
            print('Please input the number of actors: ')
            number = input()
            try:
                number = int(number)
            except:
                print('the number is invalid')
            else:
                graph.top_X_actors_with_most_gross(number)

        elif num == 5:
            print('Please input the number of actors: ')
            number = input()
            try:
                number = int(number)
            except:
                print('the number is illegal')
            else:
                graph.oldest_X_actors(number)

        elif num == 6:
            print('Please input a year: ')
            year = input()
            try:
                year = int(year)
            except:
                print('the year is illegal')
            else:
                graph.all_movie_given_year(year)

        elif num == 7:
            print('Please input a year: ')
            year = input()
            try:
                year = int(year)
            except:
                print('the year is illegal')
            else:
                graph.actors_given_year(year)


graph = Graph()
start_query(graph)