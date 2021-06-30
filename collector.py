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
from multiprocessing.pool import ThreadPool as Pool

def main():
    mypath = "/Users/wenqingwang/Downloads/data/lfw"
    people = getPeople(mypath)

    #race, gender:
    # rg_result = getRaceGender(mypath)

    #db pedia:
    poolSize= 1500
    pool = Pool(poolSize)
    db_result = list() 
    for person in people:
        pool.apply_async(dbQueries, (person, db_result,))
    pool.close()
    pool.join()
    
    #json, charts:
    with open("db_result.json", 'w') as f:
        json.dump(db_result, f, indent=4, sort_keys=False)

    # with open("rg_result.json", 'w') as f:
    #     json.dump(rg_result, f, indent=4, sort_keys=False)

    # person_dict = dbQueries("German Khan")
    # people_result.append(person_dict)
    # for i in db_result:
    #     print(i)


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


def dbQueries(name, db_result): 
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

    print(person_dict)
    db_result.append(person_dict)
    # print(db_result)


if __name__ == '__main__':
    main()
