from unittest import TestCase
from pip._vendor import requests
from src.analysis.data_into_graph import Graph, Movie, Actor
from flask import Flask, jsonify, request, abort
import json
from src.analysis.api import *


class Test_API_Result(TestCase):
    graph = Graph()
    graph.construct_graph()

    def test_get_actor_info(self):
        response = requests.get('http://127.0.0.1:5000/api/a/actors/Malcolm_McDowell')
        self.assertEqual(response.json(), {"age": 73, "gross": 0,
                                           "movies": ["Malcolm McDowell"],
                                           "name": "Malcolm McDowell"
                                           })
        response = requests.get('http://127.0.0.1:5000/api/a/actors/Marrie')
        self.assertEqual(response.status_code, 400)

        response = requests.delete('http://127.0.0.1:5000/api/a/actors/Alan')
        self.assertEqual(response.status_code, 400)

        response = requests.delete('http://127.0.0.1:5000/api/a/actors/Alan_Rickman')
        self.assertEqual(response.json(), {'message': 'delete successfully'})

        response = requests.put('http://127.0.0.1:5000/api/a/actors/Edwards')
        self.assertEqual(response.status_code, 400)

        response = requests.put('http://127.0.0.1:5000/api/a/actors/Kim_Basinger',
                                data=json.dumps({"total_gross": 56202243})
                                )
        self.assertEqual(response.status_code, 200)

        response = requests.get('http://127.0.0.1:5000/api/a/actors/Kim_Basinger')
        self.assertEqual(response.json(), {"name": "Kim Basinger",
                                           "age": 63,
                                           "gross": 56202243,
                                           "movies": []
                                           })

    def test_get_movie_info(self):
        response = requests.get('http://127.0.0.1:5000/api/m/movies/The_Yards')
        self.assertEqual(response.json(), {"actors": [],
                                           "box_office": 889352,
                                           "name": "The Yards",
                                           "wiki_page": "https://en.wikipedia.org/wiki/The_Yards",
                                           "year": 2000
                                           })
        response = requests.get('http://127.0.0.1:5000/api/m/movies/Avengers')
        self.assertEqual(response.status_code, 400)

        response = requests.delete('http://127.0.0.1:5000/api/m/movies/Avengers')
        self.assertEqual(response.status_code, 400)

        response = requests.delete('http://127.0.0.1:5000/api/m/movies/The_Yards')
        self.assertEqual(response.json(), {'message': 'delete successfully'})

        response = requests.put('http://127.0.0.1:5000/api/m/movies/The_Yards')
        self.assertEqual(response.status_code, 400)

        response = requests.put('http://127.0.0.1:5000/api/m/movies/Drunks',
                                data=json.dumps({"box_office": 56202243})
                                )
        self.assertEqual(response.status_code, 200)

        response = requests.get('http://127.0.0.1:5000/api/m/movies/Drunks')
        self.assertEqual(response.json(), {"actors": [
            "Richard Lewis (comedian)",
            "Faye Dunaway",
            "Spalding Gray",
            "Amanda Plummer",
            "Dianne Wiest"
        ],
            "box_office": 56202243,
            "name": "Drunks",
            "wiki_page": "https://en.wikipedia.org/wiki/Drunks_(film)",
            "year": 1995
        })

    def test_filter_actor_info(self):
        response = requests.get('http://127.0.0.1:5000/api/a/actors?name="Faith_Ford"&age=52')
        self.assertEqual(response.json(), {"result": [
            {
                "age": 52,
                "gross": 7000000,
                "movies": [
                    "You Talkin' to Me?",
                    "For Goodness Sake",
                    "North",
                    "Sometimes They Come Back... for More",
                    "Beethoven's 5th",
                    "The Pacifier",
                    "Prom",
                    "Escapee"
                ],
                "name": "Faith Ford"
            }
        ]
        })

        response = requests.get('http://127.0.0.1:5000/api/a/actors?name="Faith_Ford"|name="Donald_Burton"')
        self.assertEqual(response.json(), {"result": [
            {
                "age": -1,
                "gross": 0,
                "movies": [
                    "stub",
                    "expanding it"
                ],
                "name": "Donald Burton"
            },
            {
                "age": 52,
                "gross": 7000000,
                "movies": [
                    "You Talkin' to Me?",
                    "For Goodness Sake",
                    "North",
                    "Sometimes They Come Back... for More",
                    "Beethoven's 5th",
                    "The Pacifier",
                    "Prom",
                    "Escapee"
                ],
                "name": "Faith Ford"
            }
        ]
        })

        response = requests.post('http://127.0.0.1:5000/api/a/actors', data=json.dumps({
            "name": "Tom Hiddleston",
            "total_gross": 50,
            "movies": ["Thor: Ragnarok", "Midnight in Paris", "Henry V"]
        }))
        self.assertEqual(response.status_code, 200)

    def test_filter_movie_info(self):
        response = requests.get('http://127.0.0.1:5000/api/m/movies?name="Pulp_Fiction"&year=1994')
        self.assertEqual(response.json(), {"result": [
            {
                "actors": [
                    "John Travolta",
                    "Samuel L. Jackson",
                    "Uma Thurman",
                    "Harvey Keitel",
                    "Tim Roth",
                    "Amanda Plummer",
                    "Maria de Medeiros",
                    "Ving Rhames",
                    "Eric Stoltz",
                    "Rosanna Arquette",
                    "Christopher Walken",
                    "Bruce Willis"
                ],
                "box_office": 213000000,
                "name": "Pulp Fiction",
                "wiki_page": "https://en.wikipedia.org/wiki/Pulp_Fiction",
                "year": 1994
            }
        ]})
        response = requests.get('http://127.0.0.1:5000/api/m/movies?name="Pulp_Fiction"&year=1990')

        self.assertEqual(response.status_code, 400)

        response = requests.get('http://127.0.0.1:5000/api/m/movies?name="Pulp_Fiction"|name="North"')
        self.assertEqual(response.json(), {"result": [
            {
                "actors": [
                    "Elijah Wood",
                    "Jon Lovitz",
                    "Jason Alexander",
                    "Alan Arkin",
                    "Dan Aykroyd",
                    "Kathy Bates",
                    "Faith Ford",
                    "Graham Greene (actor)",
                    "Julia Louis-Dreyfus",
                    "Reba McEntire",
                    "John Ritter",
                    "Abe Vigoda",
                    "Bruce Willis"
                ],
                "box_office": 7000000,
                "name": "North",
                "wiki_page": "https://en.wikipedia.org/wiki/North_(1994_film)",
                "year": 1994
            },
            {
                "actors": [
                    "John Travolta",
                    "Samuel L. Jackson",
                    "Uma Thurman",
                    "Harvey Keitel",
                    "Tim Roth",
                    "Amanda Plummer",
                    "Maria de Medeiros",
                    "Ving Rhames",
                    "Eric Stoltz",
                    "Rosanna Arquette",
                    "Christopher Walken",
                    "Bruce Willis"
                ],
                "box_office": 213000000,
                "name": "Pulp Fiction",
                "wiki_page": "https://en.wikipedia.org/wiki/Pulp_Fiction",
                "year": 1994
            }
        ]
        })

        response = requests.post('http://127.0.0.1:5000/api/m/movies', data=json.dumps({
            "name": "Thor",
            "box_office": 150,
            "actors": ["Chris Hemsworth", "Natalie Portman", "Tom Hiddleston"]
        }))
        self.assertEqual(response.status_code, 200)

    def test_serialize_actor(self):
        self.assertEqual({"name": "David Dukes",
                          "age": 55,
                          "gross": 0,
                          "movies": []}, serialize_actor(self.graph.helper_actor_set['David Dukes']))

    def test_serialize_movie(self):
        self.assertEqual({"name": "The Verdict",
                          "wiki_page": "https://en.wikipedia.org/wiki/The_Verdict",
                          "box_office": 53977250,
                          "year": 1982,
                          "actors": [
                              "Paul Newman",
                              "Charlotte Rampling",
                              "Jack Warden",
                              "James Mason",
                              "Milo O'Shea"
                          ]
                          }, serialize_movie(self.graph.helper_set['The Verdict']))

    def test_filter_actor(self):
        actor_qualified = filter_actor({"name": "Stacy Ferguson"})
        self.assertEqual('Stacy Ferguson', actor_qualified[0]['name'])
        actor_qualified = filter_actor({"name": "Stacy Ferguson", "age": "10"})
        self.assertEqual([], actor_qualified)
        actor_qualified = filter_actor({"name": '"Stacy Ferguson"|name="Colin Farrell"'})
        self.assertEqual('Colin Farrell', actor_qualified[0]['name'])
        actor_qualified = filter_actor({"name": "Stacy Ferguson", 'age': '41|age=39',
                                        'total_gross': '10', 'movies': 'Nine'})
        self.assertEqual([], actor_qualified)

    def test_filter_movie(self):
        movie_qualified = filter_movie({"name": "The Towering Inferno"})
        self.assertEqual('The Towering Inferno', movie_qualified[0]['name'])
        movie_qualified = filter_movie({"name": "The Towering Inferno", "year": "2019"})
        self.assertEqual([], movie_qualified)

    def test_update_actor_info(self):
        update_actor_info("Hayden Christensen", {"total_gross": 10})
        self.assertEqual(10, graph.helper_actor_set['Hayden Christensen'].gross)

    def test_update_movie_info(self):
        update_movie_info("Toys", {"total_gross": 23.3})
        self.assertEqual(23000000, graph.helper_set['Toys'].gross)

    def test_create_new_actor(self):
        create_new_actor({"name": "Natalie Portman",
                          "total_gross": 200,
                          "age": 33,
                          "movies": ["Black Swan", "Knight of Cups", "Thor"]})
        self.assertEqual(200, graph.helper_actor_set['Natalie Portman'].gross)
        self.assertEqual(33, graph.helper_actor_set['Natalie Portman'].age)
        self.assertEqual(["Black Swan", "Knight of Cups", "Thor"],
                         graph.helper_actor_set['Natalie Portman'].movie_name)

    def test_create_new_movie(self):
        create_new_movie({"name": "Your Highness",
                          "box_office": 28,
                          "year": 2011,
                          "actors": ["Danny McBride", "James Franco", "Natalie Portman"]})
        self.assertEqual(28, graph.helper_set['Your Highness'].gross)
        self.assertEqual(["Danny McBride", "James Franco", "Natalie Portman"],
                         graph.helper_set['Your Highness'].actor_name)