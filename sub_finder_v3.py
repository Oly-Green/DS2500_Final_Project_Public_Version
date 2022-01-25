import praw
from prawcore import Forbidden, NotFound
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime, timedelta

#Load API keys and connect to Reddit API
with open('client_secrets.json') as f:
    secrets = json.load(f)

reddit = praw.Reddit(
    user_agent=secrets['user_agent'],
    client_id=secrets["client_id"],
    client_secret=secrets["client_secret"],
    username=secrets["user_id"],
    password=secrets["user_password"],
)
print("Connection Established!")

#Read in University Data into df, keep only Names Column
print('Importing University Data')
df = pd.read_excel('IPEDS_data.xlsx', sheet_name='Data')
df = df[['Name']]

#Generate Acronyms and Simplified versions of the Name
acro = []
simple = []

print('Generating Acronyms and Simplified Names')
for name in df['Name']:

    #generate name acronyms
    acro_name = ''.join([word[0] for word in name.replace('-',' ').split(' ')])
    acro.append(acro_name)


    #generate simplified version of name
    if 'of' in name:
        simple_name = name.split('of')[1].strip(' ')
    elif 'University' in name:
        simple_name = name.split('University')[0].strip(' ')
    elif 'College' in name:
        simple_name = name.split('College')[0].strip(' ')

    simple.append(simple_name)


df['Acronym'] = acro
df['Simple'] = simple

#Generate another verison of the name with no spaces, essentially just the full name
noSpace_names = [name.replace(' ', '') for name in df['Name'].values.tolist()]
df["NoSpace"] = noSpace_names

#Create empty column for subreddit names
df['Subreddits'] = np.NAN

print("Finding Subreddits:")
#Check for subreddits matching NoSpace Name
for subreddit in reddit.info(subreddits=noSpace_names):
    df.loc[df['NoSpace'] == subreddit, 'Subreddits'] = subreddit.display_name

#Check for subreddits matching Acronym
'''
Since more than one University can have the same Acronym,
double check to find which university subreddit was found.

eg. ASU could be Arizona State University or Arkansas State University,
so we take the words Arizona and Arkansas and check which one appears
in the subreddit's description and then match the subreddit to the
correct univserity.
'''
for subreddit in tqdm(reddit.info(subreddits=acro)):
    #Search all unviversities with a given acronym
    for ind, row in df.loc[df['Acronym'] == subreddit].iterrows():

        simple_words = row['Simple'].split(' ')

        if "State" in simple_words:
            simple_words.remove("State")

        #Check if other words from the simplified name are in the description
        for word in simple_words:
            if word.lower() in subreddit.public_description.lower():
                df.loc[df.index[ind], 'Subreddits'] = subreddit.display_name


#Check for subreddits matching Simplified Name
'''
Since these names can be things like Illinois or Ottowa,
double check that the descriptions contain something university related.
'''
check_words = ["university", "college", "school", "student", "students"]
for subreddit in tqdm(reddit.info(subreddits=simple)):
    for ind, row in df.loc[df['Simple'] == subreddit].iterrows():

        simple_words = row['Simple'].split(' ')

        if "State" in simple_words:
            simple_words.remove("State")

        for word in simple_words:
            if word.lower() in subreddit.public_description.lower():

                #Weeds out towns/states/ect. that have similar names to Universities
                for check_word in check_words:
                    if check_word in subreddit.public_description.lower():
                        df.loc[df.index[ind], 'Subreddits'] = subreddit.display_name
                    '''
                    elif subreddit.description != None:
                        if check_word in subreddit.description.lower():
                            df.loc[df.index[ind], 'Subreddits'] = subreddit.display_name
                    '''

#Drop Universities that we couldn't find subreddits for
df.dropna(subset=['Subreddits'], inplace=True)

print("Dropping Dead/Private Subreddits")
#Filter out old/dead/private subreddits
for subreddit in tqdm(reddit.info(subreddits=df['Subreddits'].values.tolist())):
    try:
        for submission in subreddit.new(limit=1):
            if datetime.now() - datetime.utcfromtimestamp(submission.created_utc) > timedelta(days=365):
                index_names = df[ df['Subreddits'] == subreddit ].index
                df.drop(index_names, inplace = True)

    except Forbidden:
        index_names = df[ df['Subreddits'] == subreddit ].index
        df.drop(index_names, inplace = True)

    except NotFound:
        index_names = df[ df['Subreddits'] == subreddit ].index
        df.drop(index_names, inplace = True)

#Save the results
df.to_csv('subreddits.csv')
