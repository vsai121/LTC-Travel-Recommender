from Pathfinder.greedypick import greedyorder
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces
import matplotlib.pyplot as plt
import networkx as nx

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
pos = dict(enumerate(loader.coordinates))
nx.draw(loader.Graph, pos, with_labels=True)
labels = nx.get_edge_attributes(loader.Graph,'weight')
#print(labels)
nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
plt.show()

#for i in nx.shortest_path(loader.Graph,source=0, target=17, weight='weight'):
#    print(i, loader.places[i])
start = 10



tovisit = ["Bangalore","Mumbai","Ahmedabad","Mangalore", "Hyderabad"]
#print(loader.places)
for i in range(len(tovisit)):
    tovisit[i] = loader.places.index(tovisit[i]+"\n")
allValid = []
allPaths = []
for i in tovisit:
    valid = validPlaces(start, i,tovisit,loader)
    if valid not in allValid:
        allValid.append(valid)
        path = greedyorder(start, valid, loader)
        allPaths.append(path)

for i in allPaths:
    for j in i:
        print(loader.places[j].rstrip("\n"))
    print("*"*50)


#final = greedyorder(10,valid,loader)
#for i in final:
#   print(loader.places[i])