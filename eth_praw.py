import praw
import pandas as pd
import datetime

# set up public reddit viewer
reddit = praw.Reddit(client_id = 'Ga4Peq4acgStoA',
                     client_secret = '_9TbrrkNkbus8O-SAeGT5vfY2Yc',
                     user_agent = "?")

# initialize reddit submission // need to iteratively get back history
daily_alt = reddit.submission(url="https://www.reddit.com/r/ethtrader/comments/7ropdt/daily_altcoin_discussion_january_20_2018/")

# set limit to avoid more comments issue
daily_alt.comments.replace_more(limit=0)

# create lists for desired data points
parent_id = []
comment_id = []
comment_text = []
created_time = []

# iteratively populate lists
for comment in daily_alt.comments.list():
    parent_id.append(comment.parent())
    comment_id.append(comment.id)
    comment_text.append(comment.body)
    time = datetime.datetime.fromtimestamp(
        int(comment.created_utc)
        ).strftime('%Y-%m-%d')
    created_time.append(time)

# bind lists together to data frame
daily_data = pd.DataFrame(
    {'Parent_ID' : parent_id,
    'Comment_ID' : comment_id,
    'Comment_Text' : comment_text,
    "Comment_DateTime" : created_time}
)
