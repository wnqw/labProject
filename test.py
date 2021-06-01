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
    # for person in people:
    #     person_dict = dbQuery(person)
    #     if person_dict == {}:
    #         print(person + " has empty dict")
    #     print(person_dict)
    #     people_result.append(person_dict)

    person_dict = dbQuery("Dragan Covic")

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


    # for i in response:
    #     if i["name"]["value"] != "":
    #         name_dict = {"name": name}
    #         person_dict.update(name_dict)


    #     else:
    #         print("{} is not listed".format(name))
    #         return person_dict

        # if i["occupation"]["value"] != "":
        #     occupation_dict = {"occupation": i["occupation"]["value"]}
        #     person_dict.update(occupation_dict)
        #     return person_dict
        # else:
        #     occupation_dict = {"occupation": ""}
        #     person_dict.update(occupation_dict)
        #     print("No occupation for {} is listed".format(name))
        #     return person_dict
    return person_dict


if __name__ == '__main__':
    main()
##########
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
        if person_dict == {}:
            print(person + " has empty dict")
        print(person_dict)
        people_result.append(person_dict)

    # person_dict = dbQuery("Melinda Gates")
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
    for i in nameQ:
        if i["name"]["value"] != "":
            name_dict = {"name": name}
            person_dict.update(name_dict)
            break
        else:
            print("{} name is not listed".format(name))
            return person_dict

    occupationQ = occupationQuery(name)
    for j in occupationQ:
        if j["occupation"]["value"] != "":
            occupation_dict = {"occupation": j["occupation"]["value"]}
            person_dict.update(occupation_dict)
            
            break
        break
    awardQ = awardQuery(name)
    for k in awardQ:
        if k["award"]["value"] != "":
            award_dict = {"award": k["award"]["value"]}
            person_dict.update(award_dict)
            break
        break

    return person_dict

if __name__ == '__main__':
    main()
