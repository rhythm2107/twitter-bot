import sqlite3
from tweety import Twitter
from tweety.types import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING
import re
import time
import discord_notification
import discord_statistic
import os
import datetime

id_list = []
id_dict = {}
cookies_value = "d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; kdt=S2RG1OTATl9kHpJGi3bNfYWbYJiahmspdeKSK2iI; lang=en; dnt=1; guest_id=v1%3A171319706116288525; gt=1779903600241651920; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNGhgOKOAToMY3NyZl9p%250AZCIlMzM3MDhlZDIzYzA2NDFkZTViOWI5NDQ5ZDMyNjkyYzM6B2lkIiU0NWE5%250ANTUwNTQ1ZGVjOGFiNDkxMjVhNmUzNTE5YTBhZg%253D%253D--d5e38cccbf4e9eca8df616d29d7961da1f706953; auth_token=14249c18a260d202da0b3e2f3824d5840b895e65; ct0=289ad9a9cbcbe142c076f32d00fcd21d3841787e9485d6ba32b7168190691b657962d322b49d46d2d33c5f82a6efa3172b244b4753944fb87a598396c3effdc1660c5231dbb2fc2396f9b2178f25dd37; twid=u%3D2403922286; att=1-zHg87l7326miiqMmuuqGC876ScfOvaT7zuPWehpj"

# Log into Twitter
app = Twitter("session")
app.load_cookies(cookies_value)
print(app.me)

# Functions
def reset_database():
    database_file = 'ids_database.db'
    if os.path.exists(database_file):
        os.remove(database_file)
def create_id_table():
    conn = sqlite3.connect('ids_database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unique_ids (
            id INTEGER PRIMARY KEY,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
def check_if_id_exists(id):
    # Connect to SQLite database
    conn = sqlite3.connect('ids_database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM unique_ids WHERE id = ?', (id,))
    existing_id = cursor.fetchone()

    if existing_id:
        print("ID already exists in the database.")
    else:
        insert_id_into_db(id)
        print("New ID:", id)
        return True

    # Close connection
    conn.close()
def insert_id_into_db(id):
    conn = sqlite3.connect('ids_database.db')
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO unique_ids (id)
            VALUES (?)
        ''', (id,))

    # Commit changes and close connection
    conn.commit()
    conn.close()
def fetch_home_timeline():
    tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    for tweet in tweets:  
        id_list.append(int(tweet.id))
        id_dict[tweet.id] = {}
        id_dict[tweet.id]['url'] = tweet.url
        id_dict[tweet.id]['date'] = tweet.date.replace(tzinfo=None)
        id_dict[tweet.id]['text'] = tweet.text
        id_dict[tweet.id]['author'] = tweet.author
        id_dict[tweet.id]['is_quoted'] = tweet.is_quoted
        id_dict[tweet.id]['is_retweet'] = tweet.is_retweet
        id_dict[tweet.id]['is_reply'] = tweet.is_reply
    #     print(tweet.id, tweet.date, tweet.text, tweet.author, tweet.is_quoted, tweet.is_retweeted, tweet.url, tweet.source)
    # print(id_list)

script_start_time = datetime.datetime.now()
tweet_count = 0

# Main Code
reset_database()
create_id_table()
fetch_home_timeline()

# Add a "if date is within last 2 minutes combined with if id not in databse -> discord notification"
# thats gonna be the solution to making it ignore older tweets and not spam at the very beginning too much with older stuff

while True:
    try:
        current_time = datetime.datetime.utcnow()
        fetch_home_timeline()
        for key, value in id_dict.items():
            id_exist = check_if_id_exists(key)
            if id_exist:
                time_difference = current_time - value['date']
                if time_difference.total_seconds() <= 120:
                    if value['is_quoted'] == False:
                        if value['is_retweet'] == False:
                            if value['is_reply'] == False:
                                discord_notification.send_discord_notification(value['url'])
                                tweet_count += 1
                                time.sleep(1)
        time.sleep(15)
    except KeyboardInterrupt:
        script_end_time = datetime.datetime.now()
        duration = script_end_time - script_start_time
        
        # Extract days, hours, minutes, and seconds from the duration
        days = duration.days
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        duration_in_sec = duration.total_seconds()
        tweets_per_min = round(tweet_count / (duration_in_sec / 60), 2)

        if days != 0:
            duration_print = f"{days} d, {hours} h, {minutes} m, {seconds} s"
        else:
            duration_print = f"{hours} h, {minutes} m, {seconds} s"
        
        discord_statistic.send_discord_notification(f"Bot stopped.\nRuntime: {duration_print}\nTweet Count: {tweet_count:n}\nTweet/min: {tweets_per_min:n}")
        break

    