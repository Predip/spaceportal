import json
import nltk
import re
from collections import Counter
from nltk.corpus import stopwords

from spaceportal.settings import BASE_DIR


class WordCloudGenerator:
    nltk.data.path.append(BASE_DIR / 'spacetravel' / 'static')
    nltk.download('stopwords')

    def __init__(self):
        pass

    @staticmethod
    def get_data():
        path = BASE_DIR / 'spacetravel' / 'static' / 'space-news-data-all-2023-12-19T14.json'
        try:
            with open(path, 'r') as file:
                data = json.load(file)
                cleaned_data = []

                for news_type, news_items in data.items():
                    for item in news_items:
                        item['type'] = news_type
                        cleaned_data.append(item)

                return cleaned_data

        except FileNotFoundError:
            print(f"Error: File not found at {path}")
            return []

    def process_news(self):
        data = self.get_data()
        return json.dumps(data), self.extract_text_from_json(data)

    @staticmethod
    def extract_text_from_json(data):
        stop_words = set(stopwords.words('english'))
        exlude = [
            "techcrunch", "spaceflightinsider", "spacex", "elonx", "blueorigin", "spaceflightnow", "space.com",
            "teslarati", "virgingalactic", "planetarysociety", "phys", "nationalspacesociety", "thejapantimes",
            "nationalgeographic", "spacenews", "thenational", "jetpropulsionlaboratory", "nasa", "thespacereview",
            "theverge", "thedrive", "arstechnica", "esa", "thespacedevs", "americaspace", "thewallstreetjournal",
            "cnbc", "unitedlaunchalliance", "reuters", "thenewyorktimes", "nasaspaceflight", "syfy", "thelaunchpad",
            "euronews", "europeanspaceflight", "spacepolicyonline.com", "spacescout", "space"
        ]

        text = ' '.join(
            (item.get('title', '') + ' ' + item.get('summary', '')) for item in data
        )

        # Use regular expression to split the text into words
        word_list = re.findall(r'\b\w+\b', text.lower())  # Convert to lowercase for case-insensitive counting

        # Remove stop words from the word list
        filtered_words = [
            word for word in word_list
            if word not in stop_words and not any(char.isdigit() for char in word) and word not in exlude
        ]

        # Use Counter to count the occurrences of each remaining word
        word_counts = Counter(filtered_words)

        # Convert Counter to a list of dictionaries with 'text' and 'size' keys
        words = [{'text': word, 'size': count / 100} for word, count in word_counts.items() if count > 100]

        # Sort the list based on word frequencies (size) in descending order
        words.sort(key=lambda x: x['size'], reverse=True)
        return words
