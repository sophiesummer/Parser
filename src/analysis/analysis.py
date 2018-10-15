from src.analysis.data_into_graph import Graph, Actor, Movie


class DataAnalysis:
    graph = Graph()
    graph.construct_graph()

    # find hub actors which have most connections to other actors
    # :param k: return top k hub actors
    def hub_actor_connections(self, k):
        conn_info = []
        for actor_name in self.graph.helper_actor_set:
            ele = {}
            actor_obj = self.graph.helper_actor_set[actor_name]
            count = 0
            actor_connected = []
            for movie in actor_obj.movie_name:
                if movie not in self.graph.helper_set:
                    continue
                movie_obj = self.graph.helper_set[movie]
                for actor_in_movie in movie_obj.actor_name:
                    if actor_in_movie not in actor_connected:
                        actor_connected.append(actor_in_movie)
                        count += 1
            if count == 0:
                continue
            ele['name'] = actor_name
            ele['count'] = count
            conn_info.append(ele)

        conn_info.sort(key=lambda x: x['count'], reverse=False)
        conn_info = conn_info[-k:]
        result = {}
        for ele in conn_info:
            result[ele['name']] = ele['count']
        return result

    # find the age and total_gross value relationship
    def age_gross_relation(self):
        age_group = []
        age_gross = {}
        for actor_obj in self.graph.actors:
            actor_age = actor_obj.age
            if actor_age <= 0:
                continue
            if actor_age in age_group:
                age_gross[actor_age] += actor_obj.gross
            else:
                age_group.append(actor_age)
                age_gross[actor_age] = actor_obj.gross
        return age_gross

    # find the total box_office for each year
    def year_gross_relation(self):
        year_group = []
        year_gross = {}
        for movie_obj in self.graph.movies:
            movie_year = movie_obj.year
            if movie_year <= 1800:
                continue
            if movie_year in year_group:
                year_gross[movie_year] += movie_obj.gross
            else:
                year_group.append(movie_year)
                year_gross[movie_year] = movie_obj.gross
        return year_gross



