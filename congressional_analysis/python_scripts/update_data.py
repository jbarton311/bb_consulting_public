from datetime import datetime
import os
import logging
import pandas as pd
from git import Repo
from RSS_feed_converter import RSSURLToDataFrame

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Adding a stream handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

LOGGER.addHandler(ch)

def push_data_to_github():
    """
    Automatically push changes in data/ to GitHub
    """

    repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    repo = Repo(repo_dir)

    # Add all data files
    file_list = ['congressional_analysis/data/']
    # Add and commit
    today = datetime.today().strftime('%Y-%m-%d')
    commit_message = f'Adding output data for {today}'
    repo.index.add(file_list)
    repo.index.commit(commit_message)

    # Push
    origin = repo.remote('origin')
    origin.push()        

# 1st Google Alert - Health Sharing
ok = RSSURLToDataFrame(url="https://www.google.com/alerts/feeds/02061760130182022939/16026963312871264927",
                       filepath="/Users/amlvt225/Code/GitHub/bb_consulting_public/congressional_analysis/data/google_alerts_health.xml")
ok.run()



push_data_to_github()