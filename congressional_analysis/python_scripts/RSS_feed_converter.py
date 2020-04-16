from urllib.request import urlopen
from git import Repo
import pandas as pd
import xmltodict


class RSSURLToDataFrame():
    """ 
    Take in a URL to an RSS data feed
    And convert key elements of it to a DataFrame
    """
    
    def __init__(self, url, filepath):
        self.url = url
        self.filepath = filepath
        self.data = pd.DataFrame()

    def save_RSS_feed_to_file(self):
        """
        Take in a Google Alerts RSS URL and save
        the results to a file locally
        """
        f = urlopen(self.url)
        myfile = f.read()

        with open(self.filepath, 'w') as f:
            f.write(myfile.decode('utf-8'))

    def read_saved_XML_to_dict(self):
        """
        Read a local XML file into a dictionary
        """
        with open(self.filepath) as fd:
            doc = xmltodict.parse(fd.read())

        return doc

    def convert_doc_to_df(self):
        
        doc = self.read_saved_XML_to_dict()
        i = 0
        BIG_LIST = []

        # Loop thru every entry in the feed
        for item in doc['feed']['entry']:
            ENTRY_DICT = {}
            # Grab key attributes
            ENTRY_DICT['title'] = item['title']['#text']
            ENTRY_DICT['link'] = item['link']['@href']
            ENTRY_DICT['item_text'] = item['content']['#text']
            ENTRY_DICT['date_published'] = item['published']   

            # Convert to dataframe
            df = pd.DataFrame(ENTRY_DICT,
                                index=[i])
            BIG_LIST.append(df)
            i += 1

        # Compile results and save
        YAY = pd.concat(BIG_LIST)

        YAY['date_published'] = pd.to_datetime(YAY['date_published']).dt.date        
        self.data = YAY

    def save_to_CSV(self):
        CSV_PATH = self.filepath.replace('.xml','.csv')
        self.data.to_csv(CSV_PATH, index=False)
        
    def run(self):
        self.save_RSS_feed_to_file()
        self.convert_doc_to_df()  
        self.save_to_CSV()      