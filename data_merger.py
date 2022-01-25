import pandas as pd

ipeds = pd.read_excel('IPEDS_data.xlsx', sheet_name='Data')
subs = pd.read_csv('subreddits_tweaked.csv')

subs = subs[['Name', 'Subreddits']]

final = pd.merge(ipeds, subs, on='Name')

final.to_csv('merged_data.csv')
