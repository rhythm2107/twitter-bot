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
cookies_value = "auth_token=e9c6d077fadb7f53354aee70cd0fec036df4d233; ct0=6fb113011cddadcf13413df8a3a968f4377b3a9aafa97a5637fc2969a00de54bb11432e31cfc50fbd41758914094ea0858869e6ceb60a50518a1564ab2485b77b7373799098e42e854c1660fb860b58b; dnt=1; g_state={\"i_l\":0}; guest_id=v1%3A173211936499429146; guest_id_ads=v1%3A173211936499429146; guest_id_marketing=v1%3A173211936499429146; kdt=qPI7KbtmvUzLygP2aLQYBZcnUAmkhRygSjM2rdHZ; lang=en; night_mode=2; personalization_id=\"v1_BM3XQTcjXg+o/gs4ztYjfA==\"; twid=u%3D2403922286"

# Log into Twitter
app = Twitter("session")
app.load_cookies(cookies_value)
print(app.me)

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the database file
database_file = os.path.join(script_dir, 'ids_database.db')

# Functions
def reset_database():
    if os.path.exists(database_file):
        os.remove(database_file)
def create_id_table():
    conn = sqlite3.connect(database_file)
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
    conn = sqlite3.connect(database_file)
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
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    cursor.execute('''
            INSERT INTO unique_ids (id)
            VALUES (?)
        ''', (id,))

    # Commit changes and close connection
    conn.commit()
    conn.close()
def fetch_home_timeline():
    try:
        tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    except:
        print("Internal Server Error. Sleeping for 10 seconds.")
        time.sleep(10)
    for tweet in tweets:  
        id_list.append(int(tweet.id))
        tweet_fx_embed = tweet.url.replace("twitter", "fxtwitter")
        id_dict[tweet.id] = {}
        id_dict[tweet.id]['url'] = tweet_fx_embed
        try:
            id_dict[tweet.id]['date'] = tweet.date.replace(tzinfo=None)
        except:
            continue
        id_dict[tweet.id]['text'] = tweet.text
        id_dict[tweet.id]['author'] = tweet.author
        id_dict[tweet.id]['is_quoted'] = tweet.is_quoted
        id_dict[tweet.id]['is_retweet'] = tweet.is_retweet
        id_dict[tweet.id]['is_reply'] = tweet.is_reply

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
                                url = value['url']
                                name = '@' + value['author'].name
                                message = value['text']
                                discord_notification.send_discord_notification(name, url, message)
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