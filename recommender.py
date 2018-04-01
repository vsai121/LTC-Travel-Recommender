import networkx as nx
from Pathfinder.greedypick import greedyorder
from Loader.mapLoader import mapLoader
from Pathfinder.ZoneAngle import validPlaces

loader = mapLoader(100)
loader.loadPlaces()
loader.loadCoordinates()
loader.loadGraph()
loader.loadEdges()
places=[]
allValid = []
with open('Loader/places.txt', 'r') as f:
	reader = f.readlines()
	for place in reader:
		places.append(place)
def recommend(paths):
	for i in range(0,len(paths)-1):
		for road in nx.all_simple_paths(loader.Graph, source=places.index(paths[i]), target=places.index(paths[i+1]), cutoff=3):

			for place in road:
				#print(places[place])

				valid = validPlaces(places.index(paths[i]),places.index(paths[i+1]),road,loader)
				for j in valid:
					print(places[j])
				if valid not in allValid:
					allValid.append(valid)
					path = greedyorder(places.index(paths[i]), valid, loader)				
					#for p in path:
						#print(places[p])
			print("--"*50)
