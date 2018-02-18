import praw
import pandas as pd
from pandas.io import sql
import datetime
import sqlite3
from sqlalchemy import create_engine

# connect to database
engine = create_engine(
'sqlite:////Users/buchman/Documents/reddit_bot/data/comment_data.db'
)
conn = engine.connect()

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
created_date = []

# iteratively populate lists
for comment in daily_alt.comments.list():
    parent_id.append(comment.parent())
    comment_id.append(comment.id)
    comment_text.append(comment.body)
    time = datetime.datetime.fromtimestamp(
        int(comment.created_utc)
        ).strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.datetime.fromtimestamp(
        int(comment.created_utc)
        ).strftime('%Y-%m-%d')
    created_time.append(time)
    created_date.append(date)

# bind lists together to data frame
daily_data = pd.DataFrame(
    {'parent_id' : parent_id,
    'comment_id' : comment_id,
    'comment_text' : comment_text,
    'comment_time' : created_time,
    'comment_date' : created_date}
)



sql.to_sql(daily_data, 'comments', conn, if_exists='append')

# close connection
conn.close()
