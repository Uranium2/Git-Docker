from pymongo import MongoClient
from utils import *
from cleanIMBD import *
import json
from imdb import IMDb
import xmljson
from xml.etree.ElementTree import fromstring
from config import *
from py2neo import Graph

if __name__ == "__main__":

    # Connexion mongoDB
    database = MongoClient(mongoServer).myMovies
    print(database)

    # Connection Neo4J
    graph = Graph(uriNeo, password=passwordNeo)

    # Create BIG JSON
    ret = {"allMovies":[]}

    # Connection API
    ia = IMDb()
    base = None

    # Foreach movie id
    for i in range(idMin, idMax):
        try:
            print(i)
            film = ia.get_movie(i)
            film = film.asXML()

            xml = fromstring(film)

            tmpJSON = xmljson.badgerfish.data(xml)
            tmpSTR = json.dumps(tmpJSON).replace("$", "do_")
            tmpJSON = json.loads(tmpSTR)

            ret["allMovies"].append(tmpJSON)
            # insert(collection1, tmpJSON)

        except:
            print("erreur", i)

    # Save file
    with open('films_big.json', "w") as f:
        print(json.dumps(ret), file=f)

    cleanDico = createCleanDictionary(ret)

    # Save clean JSON
    with open("outputs.json", "w") as out:
        json.dump(cleanDico, out)


    allPersons = []
    for movie in cleanDico["allMovies"]:

        # Insert movie information in mongoDB
        insertMovieInformation(database, movie)

        # Insert person information in mongoDB
        insertPersonInformation(database, movie)

        # insert Movie
        if graph.evaluate("MATCH (a:MOVIE) WHERE a.id = %s RETURN a" % (movie["id"])) is None:
            graph.run("CREATE (a:MOVIE {id: $id})", id=movie["id"])

        # Insert genre
        if "genres" in movie:
            for genre in movie["genres"]:
                genre = genre.upper()
                if graph.evaluate("MATCH (a: %s) RETURN a" % genre) is None:
                    graph.run( "CREATE (a: %s)" % genre.upper())

                    # Create link
                    if graph.evaluate("MATCH (m:MOVIE)-[j]-(g:%s) WHERE m.id = %s return j" % (genre, movie["id"])) is None:
                        graph.run("MATCH (m:MOVIE),(g:%s) WHERE m.id = %s CREATE (m)-[:GENRE]->(g)" % (genre, movie["id"]))

        # insert Person
        for person in movie["person"]:
            if graph.evaluate("MATCH (a:PERSON) WHERE a.id = %s RETURN a" % (person["id"])) is None:
                graph.run("CREATE (a:PERSON {id: $id})", id=person["id"])

            # insert Link
            if graph.evaluate("MATCH (p:PERSON)-[j]-(m:MOVIE) WHERE p.id = %s AND m.id = %s RETURN j" % (person["id"], movie["id"])) is None:
                graph.run("MATCH (p:PERSON),(m:MOVIE) WHERE p.id = %s AND m.id = %s CREATE (p)-[:%s]->(m)" % (person["id"], movie["id"], person["role"] ))



