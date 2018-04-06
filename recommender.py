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
    print("path is ", paths)
    for i in range(0,len(paths)-1):

        print("Start=",paths[i],"end=",paths[i+1])
        for road in nx.all_simple_paths(loader.Graph, source=paths[i], target=paths[i+1], cutoff=3):
            print("road is :", road)

            valid = validPlaces(paths[i],paths[i+1],road,loader)
            print("valid=",valid)

            for j in valid:
                #print("valid=",places[j], "all=",allValid)
                if (j not in allValid) and (j not in paths):
                    allValid.append(j)
            '''if valid not in allValid:
                allValid.append(valid)
                path = greedyorder(places.index(paths[i]), valid, loader)
                #for p in path:
                    #print(places[p])'''
        #print("--"*50)
    return allValid