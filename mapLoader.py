import networkx as nx
import numpy as np
import requests
import json
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay


class mapLoader:

    def __init__(self, scale=1):
        self.places = []
        self.coordinates = []
        self.scale = scale
        self.Graph = None

    def loadPlaces(self):
        with open('places.txt', 'r') as f:
            reader = f.readlines()
            for place in reader:
                print(place)
                self.places.append(place)

    def loadCoordinates(self):
        scale = self.scale
        with open('coordinates.txt') as results:  
            for result in (results.readlines()):
                try:
                    coordinate = (json.loads(result)['results'][0]['geometry']['location']['lng'] * scale,json.loads(result)['results'][0]['geometry']['location']['lat'] * scale)
                except:
                    coordinate=(-1,-1)
                print(coordinate)
                self.coordinates.append(coordinate)

    def loadDistances(self,place1, place2):
        distanceMatrix=[]
        with open('distances.txt') as results:  
            for result in (results.readlines()):
                distanceMatrix.append([float(i) for i in result.split()])
        return distanceMatrix[self.places.index(place1)][self.places.index(place2)]

    def loadGraph(self):
        t = Delaunay(self.coordinates)
        nodes = list(range(len(self.coordinates)))
        map = np.zeros((len(self.coordinates), len(self.coordinates)))
        edges = []
        m = dict(enumerate(nodes))  # mapping from vertices to nodes
        self.Graph = nx.Graph()
        for i in range(t.nsimplex):
            edges.append((m[t.vertices[i, 0]], m[t.vertices[i, 1]]))
            edges.append((m[t.vertices[i, 1]], m[t.vertices[i, 2]]))
            edges.append((m[t.vertices[i, 2]], m[t.vertices[i, 0]]))

        for edge in edges:
            i = edge[0]
            j = edge[1]
            place1 = self.places[edge[0]]
            place2 = self.places[edge[1]]
            map[i, j] = self.loadDistances(place1, place2)
            map[j, i] = map[i, j]
            print(map[i,j])
            if(map[i,j]>0 and map[i,j]<1000):
                self.Graph.add_edge(i,j, weight=map[i,j])

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
pos = dict(enumerate(loader.coordinates))
nx.draw(loader.Graph, pos, with_labels=True)
labels = nx.get_edge_attributes(loader.Graph,'weight')
print(labels)
nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
plt.show()

#for i in nx.shortest_path(loader.Graph,source=0, target=17, weight='weight'):
#    print(i, loader.places[i])
