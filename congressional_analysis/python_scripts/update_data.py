from datetime import datetime
import os
import logging
import pandas as pd
from git import Repo
from RSS_feed_converter import RSSURLToDataFrame, OSHRSSAggregator

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
    file_list = ['congressional_analysis/data/RSS_Health_Feed.csv']
    # Add and commit
    today = datetime.today().strftime('%Y-%m-%d')
    commit_message = f'Adding output data for {today}'
    repo.index.add(file_list)
    repo.index.commit(commit_message)

    # Push
    origin = repo.remote('origin')
    origin.push()        

# 1st Google Alert - Health Sharing
self = OSHRSSAggregator()
self.run()


push_data_to_github()