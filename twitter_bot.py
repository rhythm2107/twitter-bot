from tweety import Twitter
from tweety.types import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING
import re
import time

cookies_value = "d_prefs=MjoxLGNvbnNlbnRfdmVyc2lvbjoyLHRleHRfdmVyc2lvbjoxMDAw; kdt=6AiSMptk8kIjrSMo0jixgNIWamG1sWb3y0ZGozJO; lang=en; dnt=1; gt=1777306845054431707; guest_id=v1%3A171257807717069422; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCDqrm72OAToMY3NyZl9p%250AZCIlYzVkYWQ3ZGExMDU3YTdiODNjMDk0ZmMxZjVmMTM1ZTY6B2lkIiUxMzYy%250AZDhmMDNkOTJiYmMzYzUxNWY4MTQwNjc1MWZiNw%253D%253D--51ed1e0b320cbf70b69826c4ccbaff1a2516ee33; auth_token=2a6b194ebd94dd55aa9dec4c5880be3f26cea6f0; ct0=1a0626206c3bcb5b128099fe162a0b15959922311525e5172235c021769bd34c3e5a388172ef5416d9d30ff6621b3905554354358a6ab616c74a64cfde1a38f82a068cc578bf5249e7175945da4ba3b8; twid=u%3D1171793020259373058; att=1-5KjVAqiulK9KA8TwifVgBYN8syrBvOLV6iIMllHk"

app = Twitter("session")
app.load_cookies(cookies_value)
print(app.me)


followings_ids = []

def fetch_current_followings():
    users = app.get_user_followings('GalleryPlay')
    for user in users:
        followings_ids.append(user.id)
    print(followings_ids)

def fetch_last_tweet():
    for id in followings_ids:
        tweets = app.get_tweets(id)
        for tweet in tweets:
            print(tweet)

def fetch_home_timeline():
    tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOLLOWING)
    print(tweets.tweets.id)

start_time = time.time()

n = 0
while True:
    fetch_home_timeline()
    n += 1
    print(f"Loops completed: {n}")
    time.sleep(15)