from datetime import datetime, timedelta

import flask
import pymongo
from bson.objectid import ObjectId
from flask import json, jsonify, make_response, request
from flask_cors import CORS


class JSONEncoder(json.JSONEncoder):  # extend json-encoder class

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
app.json_encoder = JSONEncoder

mongo_url = 'mongodb+srv://dbBoris:dbm0ng0@boriscluster-khrr0.azure.mongodb.net/test?retryWrites=true&w=majority'
mongo_client = pymongo.MongoClient(mongo_url, maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo_client, 'games_database')
collection = pymongo.collection.Collection(db, 'games_collection')


@app.route('/', methods=['GET'])
def home():
    return '''<h1>NBA Scores</h1>
<p>A prototype API for displaying NBA scores.</p>'''


@app.route('/api/games/all', methods=['GET'])  # A route to return all games
def api_all():
    games_in_last_24_hours = get_games_from_last_24_hours()
    return jsonify(games_in_last_24_hours)


@app.route('/api/games', methods=['GET'])  # A route to return given team's games
def api_filter_by_name():
    if 'team' in request.args:
        team = str(request.args['team'])
    else:
        return "Error: No team name provided. Please specify a team name."

    results = []
    games_in_last_24_hours = get_games_from_last_24_hours()

    for game in games_in_last_24_hours:
        if team == game.get('teams').get('teamA') or team == game.get('teams').get('teamB'):
            results.append(game)

    return jsonify(results)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'Error': 'Not found'}), 404)


def get_games_from_last_24_hours():

    current_date = datetime.now()
    games_in_last_24_hours = []

    # Check the last 20 entries and return only the relevant games
    for game in db.collection.find({}, {'_id': 0}).sort([('$natural', -1)]).limit(20):
        game_date = game.get('date') + " " + game.get('time') + ":00.0"
        game_date_obj = datetime.strptime(game_date, '%Y-%m-%d %H:%M:%S.%f')
        if current_date-timedelta(hours=24) <= game_date_obj <= current_date:
            games_in_last_24_hours.append(game)

    return games_in_last_24_hours


app.run()

