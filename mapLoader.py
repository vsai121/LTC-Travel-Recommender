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
                place = place.split()[0]
                self.places.append(place)

    def loadCoordinates(self):
        scale = self.scale
        for place in self.places:
            result = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address=" + place + "&key=%20AIzaSyB1M2yE5eTC9Gd4Qtay8q_WjmqxojO7hcM")

            result = result.content.decode('utf-8')
            coordinate = (json.loads(result)['results'][0]['geometry']['location']['lng'] * scale,
                          json.loads(result)['results'][0]['geometry']['location']['lat'] * scale)
            print(place + " " + str(coordinate))
            self.coordinates.append(coordinate)

    def loadDistances(self):
        pass

    def getDistances(self,place1, place2):
        result = requests.get(
            'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + place1 + '&destinations=' + place2 + '&key=AIzaSyD6U597d1z2sGEUTiWD6w6VcpT_lg4ou24')
        result = result.content.decode('utf-8')
        distance = (json.loads(result)['rows'][0]['elements'][0]['distance']['text'])
        distance = float(distance.split('km')[0])
        return distance

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
            map[i, j] = self.getDistances(place1, place2)
            map[j, i] = map[i, j]
            print(map[i,j])
            self.Graph.add_edge(i,j, weight=map[i,j])
        #self.Graph = nx.Graph(edges)

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
pos = dict(enumerate(loader.coordinates))
nx.draw(loader.Graph, pos)
labels = nx.get_edge_attributes(loader.Graph,'weight')
print(labels)
nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
plt.show()

#for i in nx.shortest_path(loader.Graph,source=0, target=17, weight='weight'):
#    print(i, loader.places[i])
