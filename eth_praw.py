import praw

reddit = praw.Reddit(client_id = 'Ga4Peq4acgStoA',
                     client_secret = '_9TbrrkNkbus8O-SAeGT5vfY2Yc',
                     user_agent = "?")

daily_alt = reddit.submission(url="https://www.reddit.com/r/ethtrader/comments/7ropdt/daily_altcoin_discussion_january_20_2018/")

daily_alt.comments.replace_more(limit=0)

for comment in daily_alt.comments.list():
    print(20*'-')
    print('Parent ID:', comment.parent())
    print('Comment ID:', comment.id)
    print(comment.body)
