import json

from flask import request, Flask
from flask_restful import Api, Resource

import articles_db
import comments_db
import db_connection

app = Flask(__name__)
api = Api(app)

class Comments(Resource):

    def post(self, id):
        data = request.get_json()
        comment = data['comment']
        username = request.authorization.username
        article = comments_db.get_article_id(id)
        if article:
            comments_db.post_comment(id, username, comment)
            response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                          status = 201,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response

class N_Comments(Resource):
    def get(self, id):
        # Retrieve the number of comments on a given article
        n_comments = comments_db.count_comments(id)
        n_comments = n_comments.count
        if n_comments:
            no_of_comments = {'Number of comments': n_comments}
            response = app.response_class(response = json.dumps(no_of_comments, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


class Delete_Comment(Resource):
    def delete(self, id):
        # Delete an individual comment
        data = request.get_json()
        comment = comments_db.get_comment(id)
        username = request.authorization.username
        if comment is not None:
            rowcount = comments_db.delete_comment(id, username)
            response = app.response_class(response = json.dumps({"message": "OK"}, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status=404,
                                          content_type='application/json')
            return response

class NComments(Resource):
    def get(self, id, recent_comments):
        # Retrieve the n most recent comments for an article
        n_comments = comments_db.get_comments(id, recent_comments)
        article = articles_db.get_article_by_id(id)
        title = article[0].title
        if n_comments:
            comments = []
            for row in n_comments:
                comment = {}
                comment['Title'] = title
                comment['Comment'] = row.comment
                comment['Post Time'] = row.post_time
                comment['Last Updated Time'] = row.last_updated_time
                comments.append(comment)
            response = app.response_class(response = json.dumps(comments, indent = 4),
                                          status = 200,
                                          content_type = 'application/json')
            return response
        else:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response


api.add_resource(Comments, "/comment/<id>")
api.add_resource(N_Comments, "/n-comment/<id>")
api.add_resource(Delete_Comment, "/delete-comment/<id>")
api.add_resource(NComments, "/n-comments/<id>/<recent_comments>")

if __name__ == "__main__":
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5200)
