import json

from flask import Flask, request, Response
from flask_restful import Resource, Api

import articles_db
import db_connection

app = Flask(__name__)
api = Api(app)

class Post_Article(Resource):
    def post(self):
        data = request.get_json()
        text = data['text']
        title = data['title']
        username = request.authorization.username
        # Check NULL condition of all fields
        if text == "" or title == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        # Post an article
        data_id = articles_db.get_data_id()
        if data_id is None:
            data_id = 1
        else:
            data_id = data_id + 1
        url = "http://localhost/articles/" + str(data_id)
        articles_db.post_article(data_id, username, text, title, url)
        response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                      status = 201,
                                      content_type = 'application/json')
        return response

class Articles(Resource):
    # Update an article
    def patch(self, id):
        data = request.get_json()
        title = data['title']
        text = data['text']
        username = request.authorization.username
        # Check NULL condition of all fields
        if text == "" == "" or title == "":
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status = 400,
                                          content_type = 'application/json')
            return response
        article = articles_db.get_article_details(username, id)
        if not article:
            # Check if article exists or not
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        articles_db.edit_article(title, text, id)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response
#
    # Delete an article
    def delete(self, id):
        username = request.authorization.username
        article = articles_db.get_article_details(username, id)
        if not article:
            # Article not found
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        # Delete an article
        articles_db.delete_article(id)
        response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response

class Get_Article(Resource):
    def get(self, id):
        article = articles_db.get_article_by_id(id)
        if not article:
            # Article not found
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

        article = article[0]
        title = article[7]
        text = article[6]
        message = {'Title': title,
                   'Text': text}
        response = app.response_class(response = json.dumps(message, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class NArticles(Resource):
    def get(self, no_of_articles):
        n_articles = articles_db.get_n_articles(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        articles = []
        for row in n_articles:
            article = {}
            article['Title'] = row.title
            article['Text'] = row.text
            article['Author'] = row.username
            article['URL'] = row.url
            article['Post Time'] = row.post_time
            article['Last Updated Time'] = row.last_updated_time
            articles.append(article)
        response = app.response_class(response = json.dumps(articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


class ArticleMetadata(Resource):
    def get(self, no_of_articles):
        n_articles = articles_db.get_articles_metadata(no_of_articles)
        if not n_articles:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        articles = []
        for row in n_articles:
            article = {}
            article['Title'] = row.title
            article['Author'] = row.username
            article['URL'] = row.url
            artcle['Text'] = row.text
            article['Post Time'] = row.post_time
            articles.append(article)
        response = app.response_class(response = json.dumps(articles, indent = 4),
                                      status = 200,
                                      content_type = 'application/json')
        return response


api.add_resource(Articles, '/article/<id>')
api.add_resource(Get_Article, '/get-article/<id>')
api.add_resource(Post_Article, '/article')
api.add_resource(NArticles, '/articles-data/<no_of_articles>')
api.add_resource(ArticleMetadata, '/articles-metadata/<no_of_articles>')
#

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5100)
