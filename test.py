from Pathfinder.greedypick import greedyorder
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces , validate
import matplotlib.pyplot as plt
import networkx as nx
from createMap import makeMap
from recommender import recommend

def powerset(s):
	power=[]
	x = len(s)
	for i in range(1 << x):
		t=[s[j] for j in range(x) if (i & (1 << j))]
		if len(t)>0:
			power.append(t)

	return power


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
startPoint=start
start=loader.places.index(start+'\n')
tovisit = input("Enter your desired destinations:").split()
for i in range(len(tovisit)):
	tovisit[i] = loader.places.index(tovisit[i]+"\n")
allValid = []
allPaths = []

"""
recommendedVisits = [start]

for x in tovisit:
	recommendedVisits.append(x)

recommendedVisits = recommend(recommendedVisits)

"""

for i in tovisit:
	valid = validPlaces(start, i,tovisit,loader)
	print("i" , i , "Valid" , valid);

	if valid not in allValid:
		allValid.append(valid)
		path = greedyorder(start, valid, loader)

		allPaths.append(path)

print("allpaths", allPaths)
lastRoutes=[]

for x in allPaths:
	for i in powerset(x):
		finalPath=[]
		s=start
		print("powerset")
		if validate(start,i,loader):
			for j in i:
				for k in nx.shortest_path(loader.Graph,source=s, target=j, weight='weight'):
					if k not in finalPath:
						finalPath.append(k)

				s=j
			if finalPath not in lastRoutes:
				lastRoutes.append(finalPath)

bestPaths={}
for lastRoute in lastRoutes:
	currentRoute=(lastRoute)
	#legal = validate(start,currentRoute , loader)
	includedDestinations=[loader.places[x] for x in currentRoute if x in tovisit]
	bestPaths["".join(includedDestinations)]=currentRoute
	print("Final path is:",currentRoute," includes destinations:",includedDestinations)
	print("*"*50)

a=bestPaths
remainingPlaces=tovisit
bestPaths={}
numberOfPlaces=lambda s:s.count("\n")
sortedKeys=sorted(a,key=numberOfPlaces,reverse=True)
for key in sortedKeys:
	bestPaths[key]=a.get(key)
print(bestPaths)

for key in bestPaths:
	placesVisited=key.split("\n")
	placesRemoved=0
	for place in placesVisited:
		if place!='' and loader.places.index(place+'\n') in remainingPlaces:
			remainingPlaces.remove(loader.places.index(place+"\n"))
			placesRemoved+=1
	if placesRemoved:
		print(remainingPlaces)
		recommend(bestPaths,key,startPoint)
		currentRoute=bestPaths[key]
		makeMap(currentRoute)
	if len(remainingPlaces)==0:
		break

