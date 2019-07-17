import json

def createCleanDictionary(data):
    
    newMovies = {"allMovies":[]}

    for movie in data["allMovies"]:
        newMovie = {}
        try:
            newMovie["id"] = movie["movie"]["@id"]
            newMovie["title"] = movie["movie"]["title"]["do_"]
        except:
            print("no title or id")
            continue

        if "year" in movie["movie"]:
            newMovie["year"] = movie["movie"]["year"]["do_"]
        if "runtimes" in movie["movie"]:
            newMovie["runtime"] = movie["movie"]["runtimes"]["item"]["do_"]
        if "rating" in movie["movie"]:
            newMovie["rating"] = movie["movie"]["rating"]["do_"]
        if "plot-outline" in movie["movie"]:
            newMovie["plot"] = movie["movie"]["plot-outline"]["do_"]

        if "genres" in movie["movie"]:
            tmpList = []
            if type(movie["movie"]["genres"]["item"]) is dict:
                tmpList.append(movie["movie"]["genres"]["item"]["do_"])
            elif type(movie["movie"]["genres"]["item"]) is list:
                for genre in movie["movie"]["genres"]["item"]:
                    tmpList.append(genre["do_"])
            newMovie["genres"]  = tmpList

        if "color-info" in movie["movie"]:
            tmpList = []
            if type(movie["movie"]["color-info"]["item"]) is dict:
                tmpList.append(movie["movie"]["color-info"]["item"]["do_"])
            newMovie["color-info"]  = tmpList
        
        if "sound-mix" in movie["movie"]:
            tmpList = []
            if type(movie["movie"]["sound-mix"]["item"]) is dict:
                tmpList.append(movie["movie"]["sound-mix"]["item"]["do_"])
            newMovie["sound-mix"]  = tmpList
        
        if "countries" in movie["movie"]:
            tmpList = []
            if type(movie["movie"]["countries"]["item"]) is dict:
                tmpList.append(movie["movie"]["countries"]["item"]["do_"])
            elif type(movie["movie"]["countries"]["item"]) is list:
                for genre in movie["movie"]["countries"]["item"]:
                    tmpList.append(genre["do_"])
            newMovie["countries"]  = tmpList
        
        if "languages" in movie["movie"]:
            tmpList = []
            if type(movie["movie"]["languages"]["item"]) is dict:
                tmpList.append(movie["movie"]["languages"]["item"]["do_"])
            elif type(movie["movie"]["languages"]["item"]) is list:
                for genre in movie["movie"]["languages"]["item"]:
                    tmpList.append(genre["do_"])
            newMovie["languages"]  = tmpList

        newMovie["person"] = getUsers(movie)
        if "cast" in movie["movie"] and "person" in movie["movie"]["cast"]:    
            newMovies["allMovies"].append(newMovie)

    return newMovies


def getUsers(movie):

    ## get actors
    tmpPerson = []
    if "cast" in movie["movie"] and "person" in movie["movie"]["cast"]:
        if type(movie["movie"]["cast"]["person"]) is dict:
                tmpDico = {}
                tmpDico["id"] = movie["movie"]["cast"]["person"]["@id"]
                tmpDico["name"] = movie["movie"]["cast"]["person"]["name"]["do_"]
                if "current-role" in movie["movie"]["cast"]["person"]:
                    tmpDico["character"] = movie["movie"]["cast"]["person"]["current-role"]["character"]["name"]["do_"] 
                tmpDico["role"] = "actor"
                tmpPerson.append(tmpDico)       
        elif type(movie["movie"]["cast"]["person"]) is list:
            for p in movie["movie"]["cast"]["person"]:
                tmpDico = {}
                tmpDico["id"] = p["@id"]
                tmpDico["name"] = p["name"]["do_"]
                if "current-role" in p and type( p["current-role"]) is dict:
                    tmpDico["character"] = p["current-role"]["character"]["name"]["do_"]
                tmpDico["role"] = "actor"
                tmpPerson.append(tmpDico)
        ## get others
        tab = ["producers", "director", "writers", "assistant-directors"]
        for job in tab:
            if job in movie["movie"] and type(movie["movie"][job]["person"]) is dict:
                tmpDico = {}
                tmpDico["id"] = movie["movie"][job]["person"]["@id"]
                tmpDico["name"] = movie["movie"][job]["person"]["name"]["do_"]
                tmpDico["role"] = job.replace("-", "_")
                tmpPerson.append(tmpDico)       
            elif job in movie["movie"] and type(movie["movie"][job]["person"]) is list:
                for p in movie["movie"][job]["person"]:
                    tmpDico = {}
                    if not "@id" in p:
                        continue
                    tmpDico["id"] = p["@id"]
                    tmpDico["name"] = p["name"]["do_"]
                    tmpDico["role"] = job.replace("-", "_")
                    tmpPerson.append(tmpDico) 
        return (tmpPerson)
        
        ## get 


def getOldDictionary():
    with open("films.json", "r") as films:
        data = json.load(films)
        return data


if __name__ == "__main__":
    data = getOldDictionary()
    dico = createCleanDictionary(data)

    with open("output.json", "w") as out:
        json.dump(dico, out)