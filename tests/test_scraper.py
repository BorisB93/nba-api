import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))  # Enables running the test from parent dir.
from Scraper import Scraper
import unittest


class TestScraper(unittest.TestCase):

    def test_scraper_results(self):
        # A simple scraping test, comparing the results to actual scores from December 25th, 2019
        scraper = Scraper("https://www.espn.com/nba/scoreboard/_/date/20191205")
        scraper.scrape()
        results = [{'name': 'Philadelphia 76ers at Washington Wizards', 'date': '2019-12-06', 'time': '00:00',
                    'teams': {'teamA': 'Washington Wizards', 'teamAScore': '119',
                              'teamALogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/wsh.png',
                              'teamB': 'Philadelphia 76ers', 'teamBScore': '113',
                              'teamBLogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phi.png'}},
                   {'name': 'Houston Rockets at Toronto Raptors', 'date': '2019-12-06', 'time': '00:30',
                    'teams': {'teamA': 'Toronto Raptors', 'teamAScore': '109',
                              'teamALogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/tor.png',
                              'teamB': 'Houston Rockets', 'teamBScore': '119',
                              'teamBLogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/hou.png'}},
                   {'name': 'Denver Nuggets at New York Knicks', 'date': '2019-12-06', 'time': '00:30',
                    'teams': {'teamA': 'New York Knicks', 'teamAScore': '92',
                              'teamALogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/ny.png',
                              'teamB': 'Denver Nuggets', 'teamBScore': '129',
                              'teamBLogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/den.png'}},
                   {'name': 'Phoenix Suns at New Orleans Pelicans', 'date': '2019-12-06', 'time': '01:00',
                    'teams': {'teamA': 'New Orleans Pelicans', 'teamAScore': '132',
                              'teamALogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/no.png',
                              'teamB': 'Phoenix Suns', 'teamBScore': '139',
                              'teamBLogo': 'https://a.espncdn.com/i/teamlogos/nba/500/scoreboard/phx.png'}}]

        self.assertEqual(scraper.data, results)


if __name__ == '__main__':
    unittest.main()
