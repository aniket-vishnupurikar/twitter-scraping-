import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime
import json
import pandas as pd
from pymongo import MongoClient
from streamlit_option_menu import option_menu

# connecting MongoDB-Database and creating a collection
conn = MongoClient("mongodb://localhost:27017/")
db = conn["snscrape_data"]
coll = db["twitter"]


# function to scrape the data from twitter using "snscrape"
def scraping_data(token, start, end, n_tweets):
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{token} since:{start} until:{end}', top = True).get_items()):
        if i > n_tweets - 1:
            break
        tweets.append(
            [tweet.date, tweet.id, tweet.user.username, tweet.url, tweet.rawContent, tweet.replyCount, tweet.likeCount,
             tweet.retweetCount, tweet.lang, tweet.source])
    tweets_df = pd.DataFrame(tweets,
                             columns=['Datetime', 'Tweet Id', 'User Name', 'URL', 'Content', 'ReplyCount', 'LikeCount',
                                      'Retweet-Count', 'Language', 'Source'])
    json_data = tweets_df.to_json()
    csv = tweets_df.to_csv()
    return tweets_df, csv, json_data

def upload_to_database(data, n_word = "user_data"):
    dt = datetime.datetime.today()
    coll.insert_many([{
            "Key-Word":n_word,
            "datetime":dt,
            "Data":data
            }])

st.header("Scrapping Twitter Using SNSCRAPER and Uploading the Data to MongoDb")
choice = option_menu(
    menu_title="Menu",
    options=["Scrape from twitter", "Upload to database"],
    icons=["search", "boxes"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "blue", "size": "cover"},
        "icon": {"color": "red", "font-size": "16px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#29BDE9 "},
        "nav-link-selected": {"background-color": "black"}, }
)


if choice == "Scrape from twitter":
    word = st.text_input("Enter Word to Search")
    if word:
        start = st.date_input("Start Date")
        if start:
            end = st.date_input("End Date")
            if end:
                n_tweets = st.number_input("Number of Tweets(Max 100)", 1, 100)
                if n_tweets:
                    check = st.button("Run")
                    if check:
                        df, csv, json_data = scraping_data(word, start, end, n_tweets)
                        # df['Datetime'] = df['Datetime'].astype(str)
                        st.dataframe(df)
                        #coll.insert_many(df.to_dict('records'))
                        st.download_button(label = 'Download CSV',data =  csv, file_name="output.csv",mime= 'text/csv')
                        st.download_button(label = 'Download JSON',data =  json_data,file_name="output.json",mime= 'application/octet-stream')

if choice == "Upload to database":
    uploaded_file = st.file_uploader("Upload a json file")
    if uploaded_file:
        json_file = json.load(uploaded_file)
        upload_to_database(json_file)
        st.success("Your DATA-BASE has been UPDATED SUCCESSFULLY :smiley:")
    else:
        print("Upload a valid JSON file!")




