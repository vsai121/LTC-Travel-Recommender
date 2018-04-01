import networkx as nx
import numpy as np

import math

loader = None
start = None
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
        for j in range(len(left2visit)):
            spaths[j] = nx.shortest_path_length(loader.Graph, source=current, target=left2visit[j], weight='weight')
        minind = spaths.index(min(spaths))
        path.append(left2visit[minind])
        current = left2visit[minind]
        del (left2visit[minind])

    return path