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
    people = getPeople(mypath)

    people_result = list()

    for person in people:
        person_dict = dbQueries(person)
        print(person_dict)
        people_result.append(person_dict)

    # with open("data.json", 'w') as f:
    #     json.dump(people_result, f, indent=4, sort_keys=False)

    # person_dict = dbQueries("German Khan")
    # people_result.append(person_dict)
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


def dbQueries(name): #O(1)
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



# def dbQueries(name): #O(n)
#     person_dict = {"name": "", "occupation": "", "award": ""}

#     nameQ = nameQuery(name)
#     for i in nameQ:
#         if i["name"]["value"] != "":
#             name_dict = {"name": name}
#             person_dict.update(name_dict)
#             break
#         else:
#             print("{} name is not listed".format(name))
#             return person_dict

#     occupationQ = occupationQuery(name)
#     for j in occupationQ:
#         if j["occupation"]["value"] != "":
#             occupation_dict = {"occupation": j["title"]["value"]}
#             person_dict.update(occupation_dict)
#             break
#         break
#     awardQ = awardQuery(name)
#     for k in awardQ:
#         if k["award"]["value"] != "":
#             award_dict = {"award": k["award"]["value"]}
#             person_dict.update(award_dict)
#             break
#         break

#     return person_dict


if __name__ == '__main__':
    main()
