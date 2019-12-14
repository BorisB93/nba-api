import logging
import pymongo
import schedule
import time

from Scraper import *

logging.basicConfig(filename='scheduledscraperlog.log', format='%(asctime)s %(levelname)s %(name)s %(threadName)s : '
                                                            '%(message)s', level=logging.INFO)
url = 'https://www.espn.com/nba/scoreboard'
scraper = Scraper(url)

mongo_url = 'mongodb+srv://dbBoris:dbm0ng0@boriscluster-khrr0.azure.mongodb.net/test?retryWrites=true&w=majority'
mongo_client = pymongo.MongoClient(mongo_url, maxPoolSize=50, connect=False)
db = pymongo.database.Database(mongo_client, 'games_database')
collection = pymongo.collection.Collection(db, 'games_collection')

scraper.scrape()  # Initial scraping
logging.info("Scheduled scraper initialized.")
schedule.every(1).minutes.do(scraper.scrape)

while 1:
    schedule.run_pending()

    for game in scraper.data:
        # New games enter the database, while existing games (match both name and date) are updated (only if needed).
        if not db.collection.count_documents({'name': game.get('name'), 'date': game.get('date')}):
            db.collection.insert_one(game)
            logging.info("Added a game to the database.")
        else:
            if game != db.collection.find_one({'name': game.get('name'), 'date': game.get('date')}, {'_id': 0}):
                db.collection.replace_one({'name': game.get('name'), 'date': game.get('date')}, game)
                logging.info("Updated a game in the database.")

    time.sleep(60)
