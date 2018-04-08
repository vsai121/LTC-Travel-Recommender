import networkx as nx
import numpy as np

import math
from scipy.spatial import distance
loader = None
start = None

def findEuclideanDistance(place1,place2,loader):
    x1=loader.coordinates[place1][0]
    x2=loader.coordinates[place2][0]
    y1=loader.coordinates[place1][1]
    y2=loader.coordinates[place2][1]
    point1=[x1,y1]
    point2=[x2,y2]
    return distance.euclidean(point1,point2)


def cmpdist(i):
    global start
    disti = nx.shortest_path_length(loader.Graph, source=start,target=i,weight='weight')
    #distj = nx.shortest_path_length(loader.Graph, source=start, target=j, weight='weight')
    return disti#-distj


def greedyorder(s, destinations, l):
    global start
    global loader
    start = s
    loader = l

    left2visit = list(tuple(destinations))
    path = []
    tovisit = list(tuple(left2visit))
    try:
        tovisit = sorted(tovisit, key=cmpdist)
    except TypeError:
        print("caught")
    current = start
    for i in range(len(tovisit)):
        spaths = [math.inf] * len(left2visit)
        #eucledianDist = [math.inf] * len(left2visit)
        for j in range(1,len(left2visit)):
            spaths[j] = nx.shortest_path_length(loader.Graph, source=current, target=left2visit[j], weight='weight')
            #spaths[j] = findEuclideanDistance(i ,  j , l)
            print("Place1" , loader.places[i] , "Place2" , loader.places[j] , "Distance" , spaths[j])
        minind = spaths.index(min(spaths))
        path.append(left2visit[minind])
        current = left2visit[minind]
        del (left2visit[minind])

    return path