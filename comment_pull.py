import praw
import pandas as pd
from pandas.io import sql
import datetime
import sqlite3
from sqlalchemy import create_engine

# need to refactor to automate link generation
daily_thread_list = ['https://www.reddit.com/r/ethtrader/comments/7ndoyu/daily_altcoin_discussion_january_1_2018/',
'https://www.reddit.com/r/ethtrader/comments/7nkmyv/daily_altcoin_discussion_january_2_2018/',
'https://www.reddit.com/r/ethtrader/comments/7nss0n/daily_altcoin_discussion_january_3_2018/',
'https://www.reddit.com/r/ethtrader/comments/7o12pz/daily_altcoin_discussion_january_4_2018/',
'https://www.reddit.com/r/ethtrader/comments/7o9bnn/daily_altcoin_discussion_january_5_2018/',
'https://www.reddit.com/r/ethtrader/comments/7ohk0d/daily_altcoin_discussion_january_6_2018/',
'https://www.reddit.com/r/ethtrader/comments/7op0pg/daily_altcoin_discussion_january_7_2018/',
'https://www.reddit.com/r/ethtrader/comments/7owmm1/daily_altcoin_discussion_january_8_2018/',
'https://www.reddit.com/r/ethtrader/comments/7p56w8/daily_altcoin_discussion_january_9_2018/',
'https://www.reddit.com/r/ethtrader/comments/7pdp4f/daily_altcoin_discussion_january_10_2018/',
'https://www.reddit.com/r/ethtrader/comments/7pm5bt/daily_altcoin_discussion_january_11_2018/',
'https://www.reddit.com/r/ethtrader/comments/7pupi1/daily_altcoin_discussion_january_12_2018/',
'https://www.reddit.com/r/ethtrader/comments/7q2uwo/daily_altcoin_discussion_january_13_2018/',
'https://www.reddit.com/r/ethtrader/comments/7qa9q0/daily_altcoin_discussion_january_14_2018/',
'https://www.reddit.com/r/ethtrader/comments/7qhtk6/daily_altcoin_discussion_january_15_2018/',
'https://www.reddit.com/r/ethtrader/comments/7qqd8g/daily_altcoin_discussion_january_16_2018/',
'https://www.reddit.com/r/ethtrader/comments/7qz1rk/daily_altcoin_discussion_january_17_2018/',
'https://www.reddit.com/r/ethtrader/comments/7r7qd4/daily_altcoin_discussion_january_18_2018/',
'https://www.reddit.com/r/ethtrader/comments/7rge8z/daily_altcoin_discussion_january_19_2018/',
'https://www.reddit.com/r/ethtrader/comments/7ropdt/daily_altcoin_discussion_january_20_2018/',
'https://www.reddit.com/r/ethtrader/comments/7rw4ji/daily_altcoin_discussion_january_21_2018/',
'https://www.reddit.com/r/ethtrader/comments/7s3vd8/daily_altcoin_discussion_january_22_2018/',
'https://www.reddit.com/r/ethtrader/comments/7scgc8/daily_altcoin_discussion_january_23_2018/',
'https://www.reddit.com/r/ethtrader/comments/7sl6xp/daily_altcoin_discussion_january_24_2018/',
'https://www.reddit.com/r/ethtrader/comments/7su5k9/daily_altcoin_discussion_january_25_2018/',
'https://www.reddit.com/r/ethtrader/comments/7t2q33/daily_altcoin_discussion_january_26_2018/',
'https://www.reddit.com/r/ethtrader/comments/7tazre/daily_altcoin_discussion_january_27_2018/',
'https://www.reddit.com/r/ethtrader/comments/7timqp/daily_altcoin_discussion_january_28_2018/',
'https://www.reddit.com/r/ethtrader/comments/7tqdoy/daily_altcoin_discussion_january_29_2018/',
'https://www.reddit.com/r/ethtrader/comments/7tz0w7/daily_altcoin_discussion_january_30_2018/',
'https://www.reddit.com/r/ethtrader/comments/7u7vxm/daily_altcoin_discussion_january_31_2018/',
'https://www.reddit.com/r/ethtrader/comments/7ugr9s/daily_altcoin_discussion_february_1_2018/',
'https://www.reddit.com/r/ethtrader/comments/7updvv/daily_altcoin_discussion_february_2_2018/',
'https://www.reddit.com/r/ethtrader/comments/7uxowm/daily_altcoin_discussion_february_3_2018/',
'https://www.reddit.com/r/ethtrader/comments/7v5551/daily_altcoin_discussion_february_4_2018/',
'https://www.reddit.com/r/ethtrader/comments/7vcvdo/daily_altcoin_discussion_february_5_2018/',
'https://www.reddit.com/r/ethtrader/comments/7vlevn/daily_altcoin_discussion_february_6_2018/',
'https://www.reddit.com/r/ethtrader/comments/7vu4bp/daily_altcoin_discussion_february_7_2018/',
'https://www.reddit.com/r/ethtrader/comments/7w2u3g/daily_altcoin_discussion_february_8_2018/',
'https://www.reddit.com/r/ethtrader/comments/7wbjoy/daily_altcoin_discussion_february_9_2018/',
'https://www.reddit.com/r/ethtrader/comments/7wjsjn/daily_altcoin_discussion_february_10_2018/',
'https://www.reddit.com/r/ethtrader/comments/7wr7ql/daily_altcoin_discussion_february_11_2018/',
'https://www.reddit.com/r/ethtrader/comments/7wyty1/daily_altcoin_discussion_february_12_2018/',
'https://www.reddit.com/r/ethtrader/comments/7x7gj4/daily_altcoin_discussion_february_13_2018/',
'https://www.reddit.com/r/ethtrader/comments/7xg1g5/daily_altcoin_discussion_february_14_2018/',
'https://www.reddit.com/r/ethtrader/comments/7xojvd/daily_altcoin_discussion_february_15_2018/',
'https://www.reddit.com/r/ethtrader/comments/7xwuul/daily_altcoin_discussion_february_16_2018/',
'https://www.reddit.com/r/ethtrader/comments/7y50dr/daily_altcoin_discussion_february_17_2018/']

# connect to database
engine = create_engine(
'sqlite:////Users/buchman/Documents/reddit_bot/data/comment_data.db'
)
conn = engine.connect()

# set up public reddit viewer
reddit = praw.Reddit(client_id = 'Ga4Peq4acgStoA',
                     client_secret = '_9TbrrkNkbus8O-SAeGT5vfY2Yc',
                     user_agent = "?")


for daily in daily_thread_list :

    # initialize reddit submission // need to iteratively get back history
    daily_alt = reddit.submission(url=daily)

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

    # convert all the types to string
    daily_data[["parent_id", "comment_id", "comment_text", "comment_time", "comment_date"]] = (
    daily_data[["parent_id", "comment_id", "comment_text", "comment_time", "comment_date"]].astype(str)
    )

    sql.to_sql(daily_data, 'comments', conn, if_exists='append')


# close connection
conn.close()
