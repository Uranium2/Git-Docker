import time
import os

time.sleep(20)

from flask import Flask, request, render_template, send_from_directory, url_for
import sys
from flask_material import Material
#from config import *
from utils import *
from requestNeo4J import *
from py2neo import Graph
from pymongo import MongoClient

mongoServer = "mongodb://MONGO:27017/"
idMin = 12000
idMax = 12050

uriNeo = "http://NEO4J:7474"
passwordNeo = "root"

# #Instance variables mongoDB
# client = MongoClient('localhost', 27017)
# database = client.myMovies
# movies = database.movies
# persons = database.persons

app = Flask(__name__)
Material(app)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Connexion mongoDB
database = MongoClient(mongoServer).myMovies
print(database)

# Connection Neo4J
graph = Graph(uriNeo, password=passwordNeo)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/handle_movie/', methods=['POST'])
def handle_movie():
    movie_name = request.form['movie']

    myRequest = getNearestFilms(database.movies, movie_name, 4)

    result = {"movies": []}

    print(myRequest)
    myResult = graph.run(myRequest)
    print(myResult)

    allId = []
    result = {"movies": []}
    for id in myResult:
        for record in id:
            allId.append(record["id"])

    print(allId)
    for id in allId:
        name = getDocumentById(database.movies, id).get("title")
        result["movies"].append(name)

    print(result)

    print(movie_name)

    return render_template("result.html", data=result)

@app.route('/handle_actor/', methods=['POST'])
def handle_actor():
    actor_name = request.form['actor']
    myRequest = getNearestPersonWithRole(database.persons, actor_name, 4, "actor")

    result = {"actors":[]}

    print(myRequest)
    myResult = graph.run(myRequest)
    print(myResult)

    allId = []
    result = {"actors":[]}
    for id in myResult:
        for record in id:
            allId.append(record["id"])

    print(allId)
    for id in allId:
        name = getDocumentById(database.persons, id).get("name")
        result["actors"].append(name)

    print(result)

    return render_template("result2.html", data=result)
    

if __name__ == "__main__":
    app.run(debug=False, host= '0.0.0.0')