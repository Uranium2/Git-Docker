# Git-Docker

This project is a web application that help you getting similar actors or movies.
The data are taken from IMDB, then stored on MongoDB.
Neo4J creates link between entities (movie and person).
The web site queries Neo4J to get closest movies/actors IDs.
We retrives movies/actors names from MongoDB with the help of given IDs from Neo4J.

# How the run the project

## Build Images

    docker-compose build
    
## Run docker

    docker-compose up
    
## Change NEO4J Password

Connect to http://127.0.0.1:5000

User: neo4j
password: neo4j

A new password will be asked. Type `root`.
If you want to have a more secure password, you have to edit in `app.py` and `config.py`.
You have to change the variable `passwordNeo` to you new password.

## Init database

    py install -r requirements.txt
    cd app
    py main.py
   
## Connect to web site

http://127.0.0.1:5000
