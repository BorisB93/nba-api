import json
import re

import requests
from bs4 import BeautifulSoup


class Scraper:

    def __init__(self, url):
        self.url = url
        self.data = []

    def scrape(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.content, "html.parser")

        script = soup.find('script',
                           text=re.compile('window.espn.scoreboardData'))  # find relevant block with score information
        script = str(script)  # convert into string to edit the text
        start_location = script.index('{')
        end_location = script.index(';window.espn')
        script = script[start_location:end_location]  # cut unnecessary text from the script

        parsed_json_dict = json.loads(script)  # convert into JSON dict
        games_list, teams_list, scores_list, times_list, logos_list = self.parse_events(parsed_json_dict)

        database = []
        i = 0
        j = 0

        for game in games_list:
            database.append({"name": game, "date": times_list[j][:times_list[j].index('T')],
                             "time": times_list[j][times_list[j].index('T') + 1:times_list[j].index('Z')],
                             "teams": {"teamA": teams_list[i], "teamAScore": scores_list[i], "teamALogo": logos_list[i],
                                       "teamB": teams_list[i + 1], "teamBScore": scores_list[i + 1],
                                       "teamBLogo": logos_list[i + 1]}})
            i += 2
            j += 1

        self.data = database

    def parse_events(self, events_dict):
        games_list = []
        teams_list = []
        scores_list = []
        times_list = []
        logos_list = []

        for event in events_dict["events"]:
            games_list.append(event.get('name'))
            competitions_dict = event.get('competitions')[0]  # extract dictionary from list
            times_list.append(competitions_dict.get('date'))
            first_team = competitions_dict.get('competitors')[0]  # extract dictionaries to get team info
            logos_list.append(first_team.get('team').get('logo'))
            second_team = competitions_dict.get('competitors')[1]
            logos_list.append(second_team.get('team').get('logo'))
            first_team_name = first_team["team"].get('displayName')
            second_team_name = second_team["team"].get('displayName')
            teams_list.append(first_team_name)
            teams_list.append(second_team_name)
            scores_list.append(first_team.get('score'))
            scores_list.append(second_team.get('score'))

        return games_list, teams_list, scores_list, times_list, logos_list
