import sqlite3
from tweety import Twitter
from tweety.types import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING
import re
import time
import discord_notification
import os

id_list = []
id_dict = {}
cookies_value = "d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; lang=en; gt=1778505775091962322; guest_id=v1%3A171286402257360862; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCA7Tps6OAToMY3NyZl9p%250AZCIlMDVhYTIyMGNlOTE4NzQ0MmJhNzczMzJhNWRjN2Q5MDk6B2lkIiVlNmIy%250AMjY2N2I2NGE0ZDMwODNiNzMyNDk1ZjY4YTk1Yw%253D%253D--f181716dd4dc885166c379892df9fd21724196fa; kdt=S2RG1OTATl9kHpJGi3bNfYWbYJiahmspdeKSK2iI; auth_token=59f0a511212ac5205468aa267f4f0583c60ff337; ct0=520d4edb8c8bcc629504bce13b759361d08e07b2063eff9ce8a75abb3f52f0bf781693d791c4c569939e9e4023669b72f3929ba34c5cbede844b0c2de47b214a40480504345bdd52c696659d468f74e1; twid=u%3D1171793020259373058"

# Log into Twitter
app = Twitter("session")
app.load_cookies(cookies_value)
print(app.me)

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
        id_dict[tweet.id]['date'] = tweet.date
        id_dict[tweet.id]['text'] = tweet.text
        id_dict[tweet.id]['author'] = tweet.author
        id_dict[tweet.id]['is_quoted'] = tweet.is_quoted
    #     print(tweet.id, tweet.date, tweet.text, tweet.author, tweet.is_quoted, tweet.is_retweeted, tweet.url, tweet.source)
    # print(id_list)

reset_database()
create_id_table()
fetch_home_timeline()

print(id_dict)
for key, value in id_dict.items():
    print(key, value)

# Add a "if date is within last 2 minutes combined with if id not in databse -> discord notification"
# thats gonna be the solution to making it ignore older tweets and not spam at the very beginning too much with older stuff

# while True:
#     fetch_home_timeline()
#     for key, value in id_dict.items():
#         id_exist = check_if_id_exists(key)
#         if id_exist:
#             discord_notification.send_discord_notification(value)
#     time.sleep(15)