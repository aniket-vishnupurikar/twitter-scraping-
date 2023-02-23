# Twitter Scraping 
#### Scrape twitter data using python snscrape library and store the tweets in MongoDB using pymongo
## How to run :
- Create a Virtual environment using requirements.txt file
- Create a local mongodb database using pymongo
- Run the python script "twitter_scrape_app.py" using this command: streamlit run twitter_scrape_app.py
- You will get a link to launch the webapp.
- Once you upload data to mongodb, you can make a sanity check using the check_db.py script..

## Features

- You can give a keyword to search tweets about with start and end date and number of tweets you want
- You will have options to download the tweets data in either CSV or JSON format
- You will also have an option to upload your own json file with tweets to a mongodb database in your local system(you will have to create a mongodb database and a collection inside it first)
