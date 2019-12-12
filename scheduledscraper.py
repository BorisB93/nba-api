import time

import pymongo
import schedule

from Scraper import *

url = 'https://www.espn.com/nba/scoreboard'
mongo_url = 'mongodb+srv://dbBoris:dbm0ng0@boriscluster-khrr0.azure.mongodb.net/test?retryWrites=true&w=majority'
scraper = Scraper(url)
mongo_client = pymongo.MongoClient(mongo_url, maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo_client, 'games_database')
collection = pymongo.collection.Collection(db, 'games_collection')

schedule.every(1).minutes.do(scraper.scrape)


while 1:
    schedule.run_pending()
    time.sleep(30)

    current_games = []  # This list is used to check if the database currently contains the scraper's results
    for x in db.collection.find({}, {'_id': 0}).sort([('$natural', -1)]).limit(len(scraper.data)):
        current_games.append(x)

    if scraper.data != current_games:  # The scraper has new results - update the database
        for game in scraper.data:
            # New games enter the database, while existing games (match both name and date) are updated.
            if not db.collection.count_documents({'name': game.get('name'), 'date': game.get('date')}):
                db.collection.insert_one(game)
            else:
                db.collection.replace_one({'name': game.get('name'), 'date': game.get('date')}, game)
