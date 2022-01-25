# DS2500_Final_Project

1. Scraping subreddits 

- IPEDS_data.xlsx
    - "American University Data"
    - Excel Spreadsheet
    - https://www.kaggle.com/sumithbhongale/american-university-data-ipeds-dataset

- README.md
    - Basic Info
    - Markdown

- client_secrets.json
    - Headers and tokens for Reddit API
    - PRIVATE DO NOT SHARE
    - JSON

- data_merger.py
    - Merges subreddits.csv with original university excel data
    - Saves output to "merged_data.csv"
    - python script

- keywords.txt
    - Keyword search 

- merged_data.csv
    - Data from "American University Data" plus a column for the univerity's subreddit
    - CSV

- refreshtoken.py
    - Generates tokens for reddit api
    - not our code
    - python script
    - https://www.jcchouinard.com/get-reddit-api-credentials-with-praw/

- scraper_v6.py
    - pulls posts from reddit api and dumps them into "posts.json"
    - if 3 or more words from post in "keywords.txt"
    - python script

- sub_finder_v3.py
    - Finds subreddits for the universities in "American University Data"
    - Saves output to "subreddits.csv"
    - python script

- subreddits.csv
    - Name of university plus alternate versions and cooresponding subreddit
    - CSV

- subreddits_tweaked.csv
    - Manually tweaked version of subreddits.csv
    -   - Added Northeastern / NEU
        - Removed Northeastern Illinois University since it had Northern Illinois University's acryonym subreddit
        - Changed Milwaukee School of Engineering's subreddit from engineering to MSOE
    - CSV

- posts.json
    - JSON with all posts scraped by scraper_v6.py
    - orginized by
          - Subrredit
                - Post Title
                      - Raw Text
                      - Keywords
                      - Date
                      
2. Calcualting Vader sentiment score 

- kwords_catergories.json
    - json file that contains keywords in different topics: remote learning, socialization, mental health and covid

- Categorize_sentimentscore .ipynb
    - Using the posts.json file, calculate the Vader sentiment score for each university's subreddit post
    - Categorize the post into different topics: remote learning, socialization, mental health and covid
    - Generate a new json file called 'posts_cat_scores.json' that contains university name, all the subreddit posts and their categories and sentiment scores

- Categorize_sentimentscore_vis.ipynb
    - calculate dictionary of average sentiment scores for each topic category
    - visualize sentiment score across different topics  

- posts_cat_scores.json
    - Json with all posts categorized and scored by Categorize_sentimentscore .ipynb

3. Calculating correlation and apply Machine Learning models

- correlation .ipynb
    - scrape website using BeautifulSoup to get university's ranking, population and tuition
    - calculate correlation between Vader sentiment score and ranking, population, tuition using pearsonr
    - Apply ML models: KNN, LinearRegression, Lasso, Ridge
    - visualize Covid policies and Univeristy's sentiment score

- covid_policies.txt
    - covid policies we got from a website online
- jsonifier.py 
    - turing the covid_policies txt into json file
- covid_policies.json
    - json file containing universities with their covid policies
