from scipy.spatial import Delaunay
import networkx as nx
import numpy as np
import requests
import json
import pprint

###########################################
#        GOOGLE API KEY(DISTANCE)         #
# AIzaSyD6U597d1z2sGEUTiWD6w6VcpT_lg4ou24 #
###########################################


###########################################
#        GOOGLE API KEY(COORDINATES)      #
# AIzaSyB1M2yE5eTC9Gd4Qtay8q_WjmqxojO7hcM #
###########################################

def getCoordinates(places,scale=1):
    coordinates=[]
    for place in places:
        result=requests.get("https://maps.googleapis.com/maps/api/geocode/json?address="+place+"&key=%20AIzaSyB1M2yE5eTC9Gd4Qtay8q_WjmqxojO7hcM")
        coordinate=(json.loads(result.content)['results'][0]['geometry']['location']['lng']*scale,json.loads(result.content)['results'][0]['geometry']['location']['lat']*scale)
        coordinates.append(coordinate)
    return coordinates

def getDistances(place1,place2):
    result = requests.get('https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins=' + place1 + '&destinations='  + place2 + '&key=AIzaSyD6U597d1z2sGEUTiWD6w6VcpT_lg4ou24')
    result = result.content
    distance = (json.loads(result)['rows'][0]['elements'][0]['distance']['text'])
    distance = float(distance.split('km')[0])
    return distance

# nodes and positions
nodes = list(range(19))

places=["Udupi","Surathkal","Mangalore","kasargod","Kannur","Karkala","Moodabidri","Manipal","Shivamogga","Bhadravati","Tiptur","Hassan","Madikeri","Tumkur","Kunigal","Mandya","Mysore","Bangalore"]

points = getCoordinates(places,100)

Map = np.zeros((len(points) , len(points)))

t = Delaunay(points)

#t = points
print(t.nsimplex)
print(t.convex_hull)
edges = []
m = dict(enumerate(nodes)) # mapping from vertices to nodes
for i in range(t.nsimplex):

    edges.append( (m[t.vertices[i,0]], m[t.vertices[i,1]]) )
    edges.append( (m[t.vertices[i,1]], m[t.vertices[i,2]]) )
    edges.append( (m[t.vertices[i,2]], m[t.vertices[i,0]]) )

for edge in edges:
    i = edge[0]
    j = edge[1]
    place1 = places[edge[0]]
    place2 = places[edge[1]]
    Map[i,j]=Map[j,i]=getDistances(place1,place2)

pp = pprint.PrettyPrinter(indent=20)
pp.pprint(Map)

# build graph
G = nx.Graph(edges)
pos = dict(zip(nodes,points))
# draw
import matplotlib.pyplot as plt
nx.draw(G,pos)
plt.show()
