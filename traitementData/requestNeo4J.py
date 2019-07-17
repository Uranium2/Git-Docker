from utils import *

#persons =  [("antoine", "ACTOR"), ("nico", "DIRECTOR"), ("nico", "ACTOR")]
def getFilms(persons):
    request = "MATCH "
    for idx, person in enumerate(persons):
        request += "(n:MOVIE)-[:"+ person[1] + "]-(:PERSON{id:" + str(getIdFromName(person[0])) + "}),"
    request = request[:-1]
    request += " return n"
    return request

def getNearestPersonWithRole(name, distance, role):
    request = "MATCH (o:PERSON{id:" + str(1) + "})-[:" + role + "*0.." + str(distance) + "]-(p:PERSON) return p"
    return request

def getNearestPerson(name, distance):
    request = "MATCH (o:PERSON{id:" + str(getIdFromName(name)) + "})-[*0.." + str(distance) + "]-(p:PERSON) return p"
    return request

def getNearestFilms(name, distance):
    request = "MATCH (o:MOVIE{id:" + str(getIdFromTitle(name)) + "})-[*0.." + str(distance) + "]-(p:MOVIE) return p"
    return request

