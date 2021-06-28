#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import os
from os import walk
from os.path import isfile, join
from os import listdir
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from deepface import DeepFace
import threading
import matplotlib


def main():
    mypath = "/Users/wenqingwang/Downloads/data/lfw"
    people = getPeople(mypath)
    threadPoolSize= 100

    #race, gender:
    # rg_result = getRaceGender(mypath)

    #db pedia:
    db_result = list() 
    # makeThreads(threadPoolSize, dbQueries, "")
    for person in people:
        person_dict = dbQueries(person)
        print(person_dict)
        db_result.append(person_dict)
    
    #json, charts:
    
    # with open("raceGenderData.json", 'w') as f:
    #     json.dump(db_result, f, indent=4, sort_keys=False)

    # with open("raceGenderData.json", 'w') as f:
    #     json.dump(rg_result, f, indent=4, sort_keys=False)

    # person_dict = dbQueries("German Khan")
    # people_result.append(person_dict)
    # for i in people_result:
    #     print(i)


def makeThreads(poolSize, func, arg):
    pool = []
    for t in range (poolSize):
        if len(pool) == poolSize:
            for t in pool:
                if not t.is_alive():
                    try:
                        t.start()
                    except RuntimeError:
                        t = threading.Thread(target=dbQueries, args = arg)
                        t.start()
        else:
            thread = threading.Thread(target=dbQueries, args = arg)
            pool.append(thread)
            thread.start()


def getRaceGender(mypath):
    result = list()
    for (dirpath, dirnames, filenames) in walk(mypath):
        for filename in filenames:
            p = os.path.join(dirpath, filename)
            try:
                obj = DeepFace.analyze(img_path = p, actions = ['gender', 'race'])
                raceGenderDict = dict()
                raceGenderDict["name"] = filename
                raceGenderDict["gender"] = obj["gender"]
                raceGenderDict["race"] = obj["race"]
                result.append(raceGenderDict)
                print(obj["gender"], obj["race"])
            except:
                print("error")
    return result
        


def getPeople(mypath):
    people = list()
    for (dirpath, dirnames, filenames) in walk(mypath):
        for dirname in dirnames:
            dirname = dirname.split("_")
            dirname = " ".join(dirname)
            people.append(dirname)
        break
    return people


def nameQuery(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = '''
    SELECT *
    WHERE
    {
    ?name rdfs:label \"%s\"@en
    }
    ''' % name

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = ""
    try:
        response = sparql.query().convert()['results']['bindings']
    except:
        print("Query for {} name failed.".format(name))
    return response


def occupationQuery(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = '''
    SELECT *
    WHERE
    {
    ?name rdfs:label \"%s\"@en;
    dbo:occupation ?occupation .
    
    ?occupation dbo:title ?title .
    }
    ''' % name
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = ""

    try:
        response = sparql.query().convert()['results']['bindings']
    except:
        print("Query for {} occupation failed.".format(name))
    # print(response)
    return response


def awardQuery(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    query = '''
    SELECT *
    WHERE
    {
    ?name rdfs:label \"%s\"@en;
    dbo:award ?award .
    }
    ''' % name
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = ""
    try:
        response = sparql.query().convert()['results']['bindings']
    except:
        print("Query for {} award failed.".format(name))
    return response


def dbQueries(name): 
    person_dict = {"name": "", "occupation": "", "award": ""}

    nameQ = nameQuery(name)
    if nameQ != []:
        name_dict = {"name": name}
        person_dict.update(name_dict)
    else:
        print("{} name is not listed".format(name))
        return person_dict

    occupationQ = occupationQuery(name)
    if occupationQ != []:
        occupation_dict = {"occupation": occupationQ[0]["title"]["value"]}
        person_dict.update(occupation_dict)

    awardQ = awardQuery(name)
    if awardQ != []:
        award_dict = {"award": awardQ[0]["award"]["value"]}
        person_dict.update(award_dict)

    return person_dict




if __name__ == '__main__':
    main()
