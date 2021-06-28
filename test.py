#!/usr/local/bin/python3
import threading

# def foo():
#     print('x')

# if __name__ == '__main__':
#     pool = []
#     poolSize= 5



#     for i in range (poolSize):
#         if len(pool) == poolSize:
#             for i in pool:
#                 if not i.is_alive():
#                     try:
#                         i.start()
#                     except RuntimeError:
#                         i = threading.Thread(target=foo)
#                         i.start()
#         else:
#             thread = threading.Thread(target=foo)
#             pool.append(thread)
#             thread.start()

from deepface import DeepFace
# import json

obj = DeepFace.analyze(img_path = "/Users/wenqingwang/Downloads/data/lfw/Alicia_Keys/Alicia_Keys_0001.jpg", actions = ['gender', 'race'])
print(obj["gender"], obj["race"])

# result= list()
# raceGenderDict = dict()
# raceGenderDict["gender"] = obj["gender"]
# raceGenderDict["race"] = obj["race"]
# result.append(raceGenderDict)


# with open("raceGenderData.json", 'w') as f:
#     json.dump(result, f, indent=4, sort_keys=False)