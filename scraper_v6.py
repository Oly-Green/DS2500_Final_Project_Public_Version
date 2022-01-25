import praw
import json
import pandas as pd
from datetime import datetime, timedelta
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import string
from tqdm import tqdm

nltk.download('stopwords')
nltk.download('wordnet')

with open("keywords.txt") as f:
    kwords = [line.strip('\n').lower() for line in f.readlines()]

def text_clean(text):
    clean = [char for char in text if char not in string.punctuation and
                                      char not in string.digits]

    text_words = ''.join(clean)
    text_words = [word.lower() for word in text_words.split() if word not in stopwords.words('english') and
                                                                      not word.startswith('http') and
                                                                      not word.startswith('www')]

    return [WordNetLemmatizer().lemmatize(word) for word in text_words]

with open('client_secrets.json') as f:
    secrets = json.load(f)

reddit = praw.Reddit(
    user_agent=secrets['user_agent'],
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    username=secrets["user_id"],
    password=secrets["user_password"],
)

df = pd.read_csv('subreddits_tweaked.csv')

posts = {}
for sub_name in df['Subreddits']: #['NEU']:
    print(f"Scraping r/{sub_name}")
    subreddit = reddit.subreddit(sub_name)
    posts[sub_name] = {}

    i = 0
    for submission in tqdm(subreddit.new(limit=None)):
        if datetime.now() - datetime.utcfromtimestamp(submission.created_utc) > timedelta(days=365) or i >= 30:
            break

        text_kwords = text_clean(submission.selftext)
        text_kwords += text_clean(submission.title)

        if submission.selftext != '' and [word in text_kwords for word in kwords].count(True) >= 3:
            posts[sub_name][submission.title] = {}
            posts[sub_name][submission.title]['Keywords'] = text_kwords
            posts[sub_name][submission.title]['Raw_Text'] = submission.selftext
            posts[sub_name][submission.title]['Date'] = datetime.utcfromtimestamp(submission.created_utc).strftime("%m/%d/%Y")
            i += 1

with open('posts.json', 'w') as f:
    f.write(json.dumps(posts, sort_keys=False, indent=4))
