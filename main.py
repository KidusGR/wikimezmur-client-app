#!/usr/bin/python3

from flask import Flask
from flask_restful import Api, Resource
import scraper

app = Flask(__name__)
api = Api(app)


class WikiResource(Resource):
    def get(self):
        return {"data": "GET"}

    def post(self):
        return {"data": "POST"}


api.add_resource(WikiResource, "/home")

if __name__ == "__main__":
    app.run(debug=True)
