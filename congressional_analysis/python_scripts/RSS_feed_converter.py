import os
from urllib.request import urlopen
from git import Repo
import pandas as pd
import xmltodict
import re


class RSSURLToDataFrame():
    """ 
    Take in a URL to an RSS data feed
    And convert key elements of it to a DataFrame
    """
    
    def __init__(self, url, save_directory='/Users/amlvt225/Code/GitHub/bb_consulting_public/congressional_analysis/data/'):
        
        self.save_directory = save_directory
        self.xml_loc = os.path.join(save_directory, 'temp_file_to_delete.xml')
        self.url = url
        
        self.TAG_RE = re.compile(r'<[^>]+>')
        self.html_clean = {'&nbsp;':'',
                           '&#39;':'"',
                           '&quot;':'"'}
        
        self.data = pd.DataFrame()
        self.google_alert_name = ''

    def remove_tags(self, text):
        """ REMOVE HTML TAGS from string """
        return self.TAG_RE.sub('', text)

    def save_RSS_feed_to_file(self):
        """
        Take in a Google Alerts RSS URL and save
        the results to a file locally
        """
        f = urlopen(self.url)
        myfile = f.read()

        with open(self.xml_loc, 'w') as f:
            f.write(myfile.decode('utf-8'))

    def read_saved_XML_to_dict(self):
        """
        Read a local XML file into a dictionary
        """
        with open(self.xml_loc) as fd:
            doc = xmltodict.parse(fd.read())

        # After we read the file to memory, let's delete it
        os.remove(self.xml_loc)

        return doc

    def convert_doc_to_df(self):
        
        doc = self.read_saved_XML_to_dict()
        i = 0
        BIG_LIST = []

        self.google_alert_name = doc['feed']['title']
        print(f"working on {self.google_alert_name}")

        # Loop thru every entry in the feed
        trimmed_doc = doc['feed']['entry']

        if type(trimmed_doc) != list:
            trimmed_doc = [trimmed_doc]

        for item in trimmed_doc:
            ENTRY_DICT = {}
            # Grab key attributes
            ENTRY_DICT['title'] = item['title']['#text']
            ENTRY_DICT['link'] = item['link']['@href']
            ENTRY_DICT['item_text'] = item['content']['#text']
            ENTRY_DICT['date_published'] = item['published']  
            ENTRY_DICT['google_alert_name'] =  self.google_alert_name 

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

    def clean_data(self):
        df = self.data.copy()
        print(f"Original pull is {self.data.shape[0]} rows")
        df['title'] = df['title'].apply(self.remove_tags)
        df['item_text'] = df['item_text'].apply(self.remove_tags)
        
        # Remove duplicate links
        df.drop_duplicates('link', inplace=True)
        self.data = df
        self.clean_html_tag_list()

        print(f"Final .data is {self.data.shape[0]} rows")


    def clean_html_tag_list(self):
        cols = ['item_text','title']

        # Loop thru each string to be cleaned
        for original, clean in self.html_clean.items():
            # Clean the string in each column
            for col in cols:
                self.data[col] = self.data[col].str.replace(original, clean)    
        
    def run(self):
        self.save_RSS_feed_to_file()
        self.convert_doc_to_df()
        self.clean_data()  
        #self.save_to_CSV()      

class OSHRSSAggregator():
    """
    Compiles a list of RSS Feed data
    """
    def __init__(self):
        self.save_loc = '/Users/amlvt225/Code/GitHub/bb_consulting_public/congressional_analysis/data/RSS_Health_Feed.csv'
        self.data = pd.DataFrame()
        self.url_list = ['https://www.google.com/alerts/feeds/02061760130182022939/3934712419000458439',
            'https://www.google.com/alerts/feeds/02061760130182022939/1798512041500117761',
            'https://www.google.com/alerts/feeds/02061760130182022939/15231506228995804698',
            'https://www.google.com/alerts/feeds/02061760130182022939/7231931892292406792',
            'https://www.google.com/alerts/feeds/02061760130182022939/7231931892292405905',
            'https://www.google.com/alerts/feeds/02061760130182022939/234813574414238216',
            'https://www.google.com/alerts/feeds/02061760130182022939/16026963312871264927',
            'https://www.google.com/alerts/feeds/02061760130182022939/18249854163104952117',
            'https://www.google.com/alerts/feeds/02061760130182022939/3557674685145924725',
            'https://www.google.com/alerts/feeds/02061760130182022939/3557674685145924725',
            'https://www.google.com/alerts/feeds/02061760130182022939/4511184026626632596']
        
    def pull_data(self):
        df_list = []
        for url in self.url_list:
            try:
                RSS = RSSURLToDataFrame(url=url)
                RSS.run()
                df_list.append(RSS.data)
            except:
                print(f"Issue with {RSS.google_alert_name}")

        self.data = pd.concat(df_list)
        
    def clean_data(self):
        self.data['google_alert_name'] = self.data['google_alert_name'].str.replace('Google Alert - ','')
        print(f"Aggregated pull is {self.data.shape[0]} rows")
        
    def save_data_to_disk(self):
        self.data.to_csv(self.save_loc, index=False)
        
    def run(self):
        self.pull_data()
        self.clean_data()
        self.save_data_to_disk()        