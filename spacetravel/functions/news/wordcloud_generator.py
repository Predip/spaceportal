import re
from collections import Counter

import nltk
from django.core.cache import cache
from nltk.corpus import stopwords

from spaceportal.settings import BASE_DIR

words_cache_key = 'word_cloud_data'


def get_wordcloud_data(data=None):
    cached_data = cache.get(words_cache_key)
    if cached_data:
        return cached_data

    nltk.data.path.append(BASE_DIR / 'spacetravel' / 'static')
    nltk.download('stopwords')

    stop_words = set(stopwords.words('english'))
    exclude = [
        "techcrunch", "spaceflightinsider", "spacex", "elonx", "blueorigin", "spaceflightnow", "space.com",
        "teslarati", "virgingalactic", "planetarysociety", "phys", "nationalspacesociety", "thejapantimes",
        "nationalgeographic", "spacenews", "thenational", "jetpropulsionlaboratory", "nasa", "thespacereview",
        "theverge", "thedrive", "arstechnica", "esa", "thespacedevs", "americaspace", "thewallstreetjournal",
        "cnbc", "unitedlaunchalliance", "reuters", "thenewyorktimes", "nasaspaceflight", "syfy", "thelaunchpad",
        "euronews", "europeanspaceflight", "spacepolicyonline.com", "spacescout", "space"
    ]

    text = ' '.join((item.news_id.title + ' ' + item.news_id.summary) for item in data)

    # Use regular expression to split the text into words
    word_list = re.findall(r'\b\w+\b', text.lower())  # Convert to lowercase for case-insensitive counting

    # Remove stop words from the word list
    filtered_words = [
        word for word in word_list
        if word not in stop_words and not any(char.isdigit() for char in word) and word not in exclude
    ]

    # Use Counter to count the occurrences of each remaining word
    word_counts = Counter(filtered_words)

    # Convert Counter to a list of dictionaries with 'text' and 'size' keys
    max_count = max(word_counts.values())
    min_count = min(word_counts.values())
    words = [{'text': word, 'size': ((count - min_count) / (max_count - min_count)) * 50}
             for word, count in word_counts.items() if count > 0]

    # Sort the list based on word frequencies (size) in descending order
    words.sort(key=lambda x: x['size'], reverse=True)

    return words
