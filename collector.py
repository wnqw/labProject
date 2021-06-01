#!/usr/bin/python
# -*- coding: utf-8 -*-

from os import walk
from os.path import isfile, join
from os import listdir
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def main():
    mypath = "/Users/wenqingwang/Downloads/data/lfw"
    people= getPeople(mypath)

    people_result = list()
    for person in people:
        person_dict = dbQuery(person)
        if person_dict == {}:
            print(person + " has empty dict")
        print(person_dict)
        people_result.append(person_dict)

    # person_dict = dbQuery("Aaron Eckhart")

    # for i in people_result:
    #     print(i)


def getPeople(mypath):
    people = list()
    for (dirpath, dirnames, filenames) in walk(mypath):
        for dirname in dirnames:
            dirname = dirname.split("_")
            dirname = " ".join(dirname)
            people.append(dirname)
        break
    return people 

# Dragan Covic 
def dbQuery(name):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")

    query = '''
    SELECT *
    WHERE
    {
    ?name rdfs:label \"%s\"@en;
    dbo:occupation ?occupation .

    } ORDER BY ?name
    ''' % name

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    response = ""
    try:
        response = sparql.query().convert()['results']['bindings']
    except:
        print("Query for {} failed.".format(name))
        return

    person_dict = dict()
    for i in response:
        if i["name"]["value"] != "":
            name_dict = {"name": name}
            person_dict.update(name_dict)
        else:
            print("{} is not listed".format(name))
            return person_dict
        if i["occupation"]["value"] != "":
            occupation_dict = {"occupation": i["occupation"]["value"]}
            person_dict.update(occupation_dict)
            return person_dict
        else:
            occupation_dict = {"occupation": ""}
            person_dict.update(occupation_dict)
            print("No occupation for {} is listed".format(name))
            return person_dict
    return person_dict


if __name__ == '__main__':
    main()
