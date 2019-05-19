import requests
from requests.auth import HTTPBasicAuth
from cachecontrol import CacheControl
import datetime
from rfeed import *
from flask import Flask,request,g,jsonify


app = Flask(__name__)
sess = requests.session()
cached_sess = CacheControl(sess)

@app.route('/summary_feed')
def summary_feed():
    response = cached_sess.get('http://localhost/articles-data/10')
    response = response.json()
    count = len(response)
    Items = []
    for i in range(count):
        Items.append(Item(
            title=response[i]['Title'],
            description="Author is "+response[i]['Author'] + " and Body content is "+response[i]['Text']
        ))
    feed = Feed(
        title="RSS Feed",
        link="http://www.example.com/rss",
        description="This is an example of how to use rfeed to generate an RSS 2.0 feed",
        language="en-US",
        lastBuildDate=datetime.datetime.now(),
        items=Items)
    return feed.rss()

@app.route('/full_feed')
def full_feed():
    r = requests.get('http://localhost/articles-metadata/100')
    print(r)
    items = []
    if r is not None:
        r = r.json()
    count = len(r)
    for i in range(count):
        comment_tags = requests.get("http://localhost/tag-url/" + str(r[i]['url']))
        if comment_tags is not None and comment_tags != '':
            comment_tags = comment_tags.json()
        tags = []
        for tag in comment_tags:
            if 'tag_name' in tag:
                tags.append(tag['tag_name'])
        comment_count = requests.get("http://localhost:5200/comment/" + str(r[i]['article_id']))
        if comment_count == '':
            comment_count = "Number of comments for given article: 0"
        comment_count = comment_count.json()
        items.append(Item(
            title = r[i]['title'],
            description = comment_count,
            categories = tags
        ))
    feed = Feed(
        title = "Full Feed",
        link = "http://www.fullfeed.com/rss",
        description = "This is full feed",
        language = "en-US",
        lastBuildDate = datetime.datetime.now(),
        items = items)

    return feed.rss()

@app.route('/comment_feed')
def comment_feed():
    response = requests.get('http://localhost/n-comments/1/10')
    response = response.json()
    count = len(response)
    items = []
    for i in range(count):
        items.append(Item(
            title="Title is"+ str(response[i]['Title']),
            description="Comment is "+ response[i]['Comment']
        ))
    feed = Feed(
        title="RSS Feed",
        link="http://www.example.com/rss",
        description="This is an example of how to use rfeed to generate an RSS 2.0 feed",
        language="en-US",
        lastBuildDate=datetime.datetime.now(),
        items=items)
    return feed.rss()


if __name__ =='__main__':
   app.run(debug=True, port=5400)
