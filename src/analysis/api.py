from flask import Flask, jsonify, request, abort
import json
from src.analysis.data_into_graph import Graph, Actor, Movie

graph = Graph()
graph.construct_graph()

app = Flask(__name__)


# get actor information by actor_name
# delete actor object by actor_name
# update actor info by actor_name
@app.route('/api/a/actors/<actor_name>', methods=['GET', 'DELETE', 'PUT'])
def get_actor_info(actor_name):
    actor_name = actor_name.replace('_', ' ')

    if request.method == 'GET':
        count = 0
        for actor_obj in graph.actors:
            if actor_obj.name == actor_name:
                result = serialize_actor(actor_obj)
                count += 1
                return jsonify(result)
        if count == 0:
            abort(400)

    if request.method == 'DELETE':
        count = 0
        for actor_obj in graph.actors:
            if actor_obj.name == actor_name:
                graph.actors.remove(actor_obj)
                count += 1
                return jsonify({'message': 'delete successfully'})
        if count == 0:
            abort(400)

    if request.method == 'PUT':
        if actor_name not in graph.helper_actor_set:
            abort(400)
        update_actor_info(actor_name, json.loads(request.data.decode('ascii')))
        return jsonify({'message': 'update successfully'})


# get movie information by movie_name
# delete movie object by movie_name
# update movie info by movie_name
@app.route('/api/m/movies/<movie_name>', methods=['GET', 'DELETE', 'PUT'])
def get_movie_info(movie_name):
    movie_name = movie_name.replace('_', ' ')
    if request.method == 'GET':
        count = 0
        for movie_obj in graph.movies:
            if movie_obj.name == movie_name:
                result = serialize_movie(movie_obj)
                count += 1
                return jsonify(result)
        if count == 0:
            abort(400)

    if request.method == 'DELETE':
        count = 0
        if movie_name in graph.helper_set:
            graph.helper_set.pop(movie_name, None)
        for movie_obj in graph.movies:
            if movie_obj.name == movie_name:
                graph.movies.remove(movie_obj)
                count += 1
                return jsonify({'message': 'delete successfully'})
        if count == 0:
            abort(400)

    if request.method == 'PUT':
        if movie_name not in graph.helper_set:
            abort(400)
        update_movie_info(movie_name, json.loads(request.data.decode('ascii')))
        return jsonify({'message': 'update successfully'})


# get actors with arguments to filter out unqualified items
# create actors by json data
@app.route('/api/a/actors', methods=['GET', 'POST'])
def filter_actor_info():
    result = {}
    if request.method == 'GET':
        request_args = {}
        request_args['name'] = request.args.get('name')
        request_args['age'] = request.args.get('age')
        request_args['total_gross'] = request.args.get('total_gross')
        request_args['movies'] = request.args.get('movies')
        result["result"] = filter_actor(request_args)
        if len(result["result"]) == 0:
            abort(400)
        else:
            return jsonify(result)

    if request.method == 'POST':
        json_data = json.loads(request.data.decode('ascii'))
        if ('name' not in json_data) or (json_data['name'] in graph.helper_actor_set):
            abort(400)
        else:
            create_new_actor(json_data)
            return jsonify({'message': 'create a new actor successfully'})


# get movies with arguments to filter out unqualified items
# create movies by json data
@app.route('/api/m/movies', methods=['GET', 'POST'])
def filter_movie_info():
    result = {}
    if request.method == 'GET':
        request_args = {}
        request_args['name'] = request.args.get('name')
        request_args['year'] = request.args.get('year')
        request_args['box_office'] = request.args.get('box_office')
        request_args['actors'] = request.args.get('actors')
        result['result'] = filter_movie(request_args)
        if len(result["result"]) == 0:
            abort(400)
        else:
            return jsonify(result)

    if request.method == 'POST':
        json_data = json.loads(request.data.decode('ascii'))
        print(json_data)
        if ('name' not in json_data) or (json_data['name'] in graph.helper_set):
            abort(400)
        else:
            create_new_movie(json_data)
            return jsonify({'message': 'create a new movie successfully'})


# serialize actor object info in order to return jsonify
# :param actor_obj: actor object to be serialized
def serialize_actor(actor_obj):
    result = {}
    result['name'] = actor_obj.name
    result['age'] = actor_obj.age
    result['gross'] = actor_obj.gross
    result['movies'] = actor_obj.movie_name
    return result


# serialize movie object info in order to return jsonify
# :param movie_obj: movie object to be serialized
def serialize_movie(movie_obj):
    result = {}
    result['name'] = movie_obj.name
    result['year'] = movie_obj.year
    result['box_office'] = movie_obj.gross
    result['wiki_page'] = movie_obj.url
    result['actors'] = movie_obj.actor_name
    return result


# filter out unqualified actors objects according to arguments
# :param attr_args: arguments for filtering
def filter_actor(attr_args):
    qualified_actor = []
    name = []
    age = []
    gross = []
    movie = []
    if 'name' in attr_args:
        args_name = attr_args['name']
    else:
        args_name = None
    if 'age' in attr_args:
        args_age = attr_args['age']
    else:
        args_age = None
    if 'total_gross' in attr_args:
        args_gross = attr_args['total_gross']
    else:
        args_gross = None
    if 'movies' in attr_args:
        args_movie = attr_args['movies']
    else:
        args_movie = None

    if args_name is not None:
        if '|' in args_name:
            m = args_name.split('"')
            for i in range(len(m)):
                if i % 2 == 1:
                    m[i] = m[i].replace('_', ' ')
                    name.append(m[i])
        else:
            args_name = args_name.replace('"', '').replace('_',' ')
            name.append(args_name)

    if args_age is not None:
        if '|' in args_age:
            m = args_age.split('|')
            age.append(int(m[0]))
            if len(m) > 1:
                for i in range(1, len(m)):
                    start = m[i].find('=')
                    age.append(int(m[i][start + 1:]))
        else:
            age.append(int(args_age))

    if args_gross is not None:
        if '|' in args_gross:
            m = args_gross.split('|')
            gross.append(int(m[0]))
            if len(m) > 1:
                for i in range(1, len(m)):
                    start = m[i].find('=')
                    gross.append(int(m[i][start + 1:]))
        else:
            gross.append(int(args_gross))

    if args_movie is not None:
        if '|' in args_movie:
            m = args_movie.split('"')
            for i in range(len(m)):
                if i % 2 == 1:
                    m[i] = m[i].replace('_', ' ')
                    movie.append(m[i])
        else:
            args_movie = args_movie.replace('"', '').replace("_",' ')
            movie.append(args_movie)

    for actor_obj in graph.actors:
        if len(name) > 0 and actor_obj.name not in name:
            continue
        if len(gross) > 0 and actor_obj.gross not in gross:
            continue
        if len(age) > 0 and actor_obj.age not in age:
            continue
        if len(movie) == 0:
            qualified_actor.append(serialize_actor(actor_obj))
        else:
            for m in movie:
                if m in actor_obj.movie_name:
                    qualified_actor.append(serialize_actor(actor_obj))
                    break
    return qualified_actor


# filter out unqualified movie objects according to arguments
# :param attr_args: arguments for filtering
def filter_movie(attr_args):
    qualified_movie = []
    name = []
    year = []
    gross = []
    actor = []

    if 'name' in attr_args:
        args_name = attr_args['name']
    else:
        args_name = None
    if 'year' in attr_args:
        args_year = attr_args['year']
    else:
        args_year = None
    if 'box_office' in attr_args:
        args_gross = attr_args['box_office']
    else:
        args_gross = None
    if 'actors' in attr_args:
        args_actor = attr_args['actors']
    else:
        args_actor = None

    if args_name is not None:
        if '|' in args_name:
            m = args_name.split('"')
            for i in range(len(m)):
                if i % 2 == 1:
                    m[i] = m[i].replace('_', ' ')
                    name.append(m[i])
        else:
            args_name = args_name.replace('"', '')
            args_name = args_name.replace('_', ' ')
            name.append(args_name)

    if args_year is not None:
        if '|' in args_year:
            m = args_year.split('|')
            year.append(int(m[0]))
            if len(m) > 1:
                for i in range(1, len(m)):
                    start = m[i].find('=')
                    year.append(int(m[i][start + 1:]))
        else:
            year.append(int(args_year))

    if args_gross is not None:
        if '|' in args_gross:
            m = args_gross.split('|')
            gross.append(int(m[0]))
            if len(m) > 1:
                for i in range(1, len(m)):
                    start = m[i].find('=')
                    gross.append(int(m[i][start + 1:]))
        else:
            gross.append(int(args_gross))

    if args_actor is not None:
        if '|' in args_actor:
            m = args_actor.split('"')
            for i in range(len(m)):
                if i % 2 == 1:
                    m[i] = m[i].replace('_', ' ')
                    actor.append(m[i])
        else:
            args_actor = args_actor.replace('"', '')
            args_actor = args_actor.replace('_', ' ')
            actor.append(args_actor)

    for movie_obj in graph.movies:
        if len(name) > 0 and movie_obj.name not in name:
            continue
        if len(gross) > 0 and movie_obj.gross not in gross:
            continue
        if len(year) > 0 and movie_obj.year not in year:
            continue
        if len(actor) == 0:
            qualified_movie.append(serialize_movie(movie_obj))
        else:
            for a in actor:
                if a in movie_obj.actor_name:
                    qualified_movie.append(serialize_movie(movie_obj))
                    break
    return qualified_movie


def update_actor_info(actor_name, json_data):
    actor_obj = graph.helper_actor_set[actor_name]
    for ele in json_data:
        if ele == "total_gross":
            actor_obj.gross = json_data[ele]
        elif ele == 'age':
            actor_obj.age = json_data[ele]
        elif ele == 'movies':
            actor_obj.movie_name = json_data[ele]


def update_movie_info(movie_name, json_data):
    movie_obj = graph.helper_set[movie_name]
    for ele in json_data:
        if ele == "box_office":
            movie_obj.gross = json_data[ele]
        elif ele == 'year':
            movie_obj.year = json_data[ele]
        elif ele == 'actors':
            movie_obj.actor_name = json_data[ele]
        elif ele == 'wiki_page':
            movie_obj.url = json_data[ele]


# create new actor object into graph according to json data
# :param json_data: the json data from post body
def create_new_actor(json_data):
    actor_obj_name = json_data['name']
    if 'age' in json_data:
        actor_obj_age = json_data['age']
    else:
        actor_obj_age = -1
    if 'total_gross' in json_data:
        actor_obj_gross = json_data['total_gross']
    else:
        actor_obj_gross = 0
    if 'movies' in json_data:
        actor_obj_movie_name = json_data['movies']
    else:
        actor_obj_movie_name = []
    actor_obj = Actor(actor_obj_name, actor_obj_age, actor_obj_gross, actor_obj_movie_name)
    graph.actors.append(actor_obj)
    graph.helper_actor_set[actor_obj.name] = actor_obj
    for m in actor_obj.movie_name:
        if m in graph.helper_set:
            graph.add_edges(actor_obj, graph.helper_set[m])


# create new movie object into graph according to json data
# :param json_data: the json data from post body
def create_new_movie(json_data):
    movie_obj_name = json_data['name']
    if 'year' in json_data:
        movie_obj_year = json_data['year']
    else:
        movie_obj_year = 0
    if 'box_office' in json_data:
        movie_obj_gross = json_data['box_office']
    else:
        movie_obj_gross = 0
    if 'wiki_page' in json_data:
        movie_obj_url = json_data['wiki_page']
    else:
        movie_obj_url = ""
    if 'actors' in json_data:
        movie_obj_actor_name = json_data['actors']
    else:
        movie_obj_actor_name = []

    movie_obj = Movie(movie_obj_name, movie_obj_gross, movie_obj_year,
                      movie_obj_actor_name, movie_obj_url)
    graph.movies.append(movie_obj)
    graph.helper_set[movie_obj_name] = movie_obj
    for a in movie_obj.actor_name:
        if a in graph.helper_actor_set:
            graph.add_edges(graph.helper_actor_set[a], movie_obj)
