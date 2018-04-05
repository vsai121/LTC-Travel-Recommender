from Pathfinder.greedypick import greedyorder
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces
import matplotlib.pyplot as plt
import networkx as nx
from createMap import makeMap
from recommender import recommend

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
loader.loadEdges()
pos = dict(enumerate(loader.coordinates))
nx.draw(loader.Graph, pos, with_labels=True)
labels = nx.get_edge_attributes(loader.Graph,'weight')
nx.draw_networkx_edge_labels(loader.Graph,pos,edge_labels=labels)
plt.show()

start = input("Enter source:")
start=loader.places.index(start+'\n')
tovisit = input("Enter your desired destinations:").split()

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

print("allpaths",allPaths)
for i in allPaths:
	s=start
	finalPath=[]
	for j in i:
		for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight'):
			if k not in finalPath:

				finalPath.append(k)
		#print("final path",finalPath)
		
		s=j
	print("Final path is:",finalPath)
	validPlaces(start,i[-1],finalPath,loader)
	#recommend(finalPath)
	makeMap(finalPath)	
	print("*"*50)

