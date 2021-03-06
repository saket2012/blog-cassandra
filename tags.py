import json

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import articles_db
import db_connection
import tags_db

app = Flask(__name__)
api = Api(app)


class Tags(Resource):
    def post(self, id):
        data = request.get_json()
        tag_name = data['tag_name']
        url = data['url']
        username = request.authorization.username
        if tag_name == '' or url == '':
            response = app.response_class(response = json.dumps({"message": "BAD REQUEST"}, indent = 4),
                                          status=400,
                                          content_type='application/json')
            return response
        article = articles_db.get_article_by_id(id)
        if not article:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        tags_db.post_tag(id, username, tag_name, url)
        response = app.response_class(response = json.dumps({"message": "CREATED"}, indent = 4),
                                      status=201,
                                      content_type='application/json')
        return response

    def delete(self, id):
        data = request.get_json()
        url = data['url']
        if url == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tag = tags_db.get_tag_details(url)
        if not tag:
            response = app.response_class(response = json.dumps({"message": "NOT FOUND"}, indent = 4),
                                          status = 404,
                                          content_type = 'application/json')
            return response
        tags_db.delete_tag(url)
        response = app.response_class(response=json.dumps({"message": "OK"}, indent=4),
                                      status=200,
                                      content_type='application/json')
        return response

    def get(self, id):
        data = request.get_json()
        tag_name = data['tag_name']
        if tag_name == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tags = tags_db.get_tag_by_tag_name(tag_name)
        if not tags:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        return jsonify({"Tags": tags})


class TagsByURL(Resource):
    def get(self, url):
        data = request.get_json()
        if url == '':
            response = app.response_class(response=json.dumps({"message": "BAD REQUEST"}, indent=4),
                                          status=400,
                                          content_type='application/json')
            return response
        tags = tags_db.get_tags_by_url(url)
        if not tags:
            response = app.response_class(response=json.dumps({"message": "NOT FOUND"}, indent=4),
                                          status=404,
                                          content_type='application/json')
            return response
        return jsonify({"Tags": tags})


api.add_resource(Tags, '/tag/<id>')
api.add_resource(TagsByURL, '/tag-url/<url>')

if __name__ == '__main__':
    db_connection.create_tables()
    app.run(debug = True, host = '0.0.0.0', port = 5300)
