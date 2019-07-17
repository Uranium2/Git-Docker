from utils import *

#persons =  [("antoine", "ACTOR"), ("nico", "DIRECTOR"), ("nico", "ACTOR")]
def getFilms(persons):
    request = "MATCH "
    for idx, person in enumerate(persons):
        request += "(n:MOVIE)-[:"+ person[1] + "]-(:PERSON{id:" + str(getIdFromName(person[0])) + "}),"
    request = request[:-1]
    request += " return n"
    return request

def getNearestPersonWithRole(collection, name, distance, role):
    request = "MATCH (o:PERSON{id:" + str(getIdFromName(collection, name))  + "})-[:" + role + "*0.." + str(distance) + "]-(p:PERSON) return p"
    return request

def getNearestPerson(collection, name, distance):
    request = "MATCH (o:PERSON{id:" + str(getIdFromName(collection, name)) + "})-[*0.." + str(distance) + "]-(p:PERSON) return p"
    return request

def getNearestFilms(collection, name, distance):
    request = "MATCH (o:MOVIE{id:" + str(getIdFromTitle(collection, name)) + "})-[*0.." + str(distance) + "]-(p:MOVIE) return p"
    return request

