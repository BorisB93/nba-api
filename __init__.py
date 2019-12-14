from .api import app

with app.app_context():
    from .tests import test_scraper