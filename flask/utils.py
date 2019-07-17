def insert_one(collection, dictionnaire):
    collection.insert_one(dictionnaire)

def insert(collection, dictionnaire):
    collection.insert(dictionnaire)

def insertMovieInformation(database, movie):

   # print({ key:value for key, value in movie.items() if key != "person"})
    database.movies.insert({ key:value for key, value in movie.items() if key != "person"})


def insertPersonInformation(database, movie):

    #print({key: value for key, value in movie.items() if key == "person"})
    listPerson = { key:value for key, value in movie.items() if key == "person"}["person"]

    for person in listPerson:

        database.persons.update( {"id":person["id"]}, {"$set":person}, upsert=True )



# def add_movie(id):
#     graph.run("CREATE UNIQUE (a:Movie {id: $id})", id=id)

def getIdFromTitle(collection, name):
    return collection.find_one({"title": name}).get("id")
        
    
def getIdFromName(collection, name):
    return collection.find_one({"name": name}).get("id")

def getDocumentById(collection, id):
    return collection.find_one({"id": id})
