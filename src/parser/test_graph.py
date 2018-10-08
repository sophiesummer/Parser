from unittest import TestCase
from src.parser.graph import Graph


class TestGraph(TestCase):
    graph = Graph()
    graph.construct_graph()

    def test_get_gross(self):
        self.assertEqual(286200000.0, self.graph.get_gross('The Sound of Music'))
        self.assertEqual(-1, self.graph.get_gross('Triple Cross'))
        self.assertIsNone(self.graph.get_gross('CS 242'))

    def test_get_all_actor_of_movie(self):
        self.assertEqual(["Sophia Loren", "Stephen Boyd", "Alec Guinness", "James Mason",
                          "Christopher Plummer", "Mel Ferrer", "Omar Sharif"],
                         self.graph.get_all_actor_of_movie('The Fall of the Roman Empire'))
        self.assertEqual([], self.graph.get_all_actor_of_movie('CS 242'))

    def test_get_all_movie_of_actor(self):
        self.assertEqual([], self.graph.get_all_movie_of_actor('Melanie Griffith'))
        self.assertEqual(["Harry Potter and the Deathly Hallows \u2013 Part 2"],
                         self.graph.get_all_movie_of_actor('Alan Rickman'))
        self.assertEqual([], self.graph.get_all_movie_of_actor('CS 242'))

    def test_all_movie_given_year(self):
        self.assertEqual([], self.graph.all_movie_given_year(1800))
        self.assertEqual(['Nurse Betty', 'Under Suspicion', 'Body and Soul'],
                         self.graph.all_movie_given_year(2000))
        self.assertEqual([], self.graph.all_movie_given_year(-1))

    def test_actors_given_year(self):
        self.assertEqual([], self.graph.actors_given_year(-1))
        self.assertEqual([], self.graph.actors_given_year(1600))
        self.assertEqual(['Morgan Freeman'], self.graph.actors_given_year(2011))

    def test_top_X_actors_with_most_gross(self):
        self.assertEqual([], self.graph.top_X_actors_with_most_gross(-1))
        self.assertEqual(len(self.graph.actors),
                         len(self.graph.top_X_actors_with_most_gross(len(self.graph.actors))))
        self.assertEqual(['Morgan Freeman', 'Rod Steiger', 'Robert Duvall', 'Elijah Wood', 'Brad Pitt'],
                         self.graph.top_X_actors_with_most_gross(5))

    def test_oldest_X_actors(self):
        self.assertEqual([], self.graph.oldest_X_actors(-9))
        self.assertEqual(len(self.graph.actors), len(self.graph.oldest_X_actors(len(self.graph.actors))))
        self.assertEqual(['Jessica Tandy', 'Geraldine Fitzgerald', 'Jim Backus', 'Ossie Davis', 'Esther Rolle'],
                         self.graph.oldest_X_actors(5))
