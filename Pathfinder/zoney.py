import math

import matplotlib.pyplot as plt
import networkx as nx

theta = 30
maxDeviation = 120

def getAngle(place1,place2,loader):
    dx = loader.coordinates[place2][0] - loader.coordinates[place1][0]
    dy = loader.coordinates[place2][1] - loader.coordinates[place1][1]
    angle = math.degrees(math.atan2((dy),(dx)))
    quadrant=1
    
    if dx>0:
        if dy<0:
            quadrant=4
            angle=-angle

    else :
        if dy>=0:
            angle-=180
            quadrant=2
        else:
            angle+=180
            quadrant=3
                
    return [angle,quadrant]

def validPlaces(source, final, destinations, loader):
    angle = getAngle(source,final,loader)[0]
    valid = []
    B=0
    if angle<0:
        angle = 180+angle

    for i in range(len(destinations)):
        if destinations[i] != final:
            A = getAngle(source,destinations[i],loader)[0]
            if A<0:
                A = 180+A
            if A >= angle-theta and A <= angle+theta:
                valid.append(destinations[i])

    valid.append(final)
    return tuple(sorted(valid))


def validate(source,path , loader):
    place1 = source
    place2=path[1]
    illegal=0
    for i in range(2 , len(path)):
        previousAngle=getAngle(place1 , place2 , loader)
        print("previousAngle",previousAngle[0])
        '''
        if previousAngle<0:
            previousAngle=180+previousAngle

        if previousAngle>90:
            previousAngle = 180 - previousAngle
        '''
        place1=place2
        place2=path[i]

        B=getAngle(place1 , place2 , loader)
        print("B",B[0])
        '''if B<0:
            B=180+B
    
        if B>90:
            C=180-B

        if B>90:    
            limit=previousAngle+C    
        
        else:'''
        if B[1]==1 or B[1]==3:
            limit = 180-previousAngle[0]+B[0]
        if B[1]==2 or B[1]==4:
            limit = B[0]+previousAngle[0]
        

     
        if limit<0:
            limit=180+limit
        print("\nb",B[0],"\nprev",previousAngle[0],"\nlimit",limit,"\nplace1",place1,"\nplace2",place2 , "quadrant" ,B[1])
        if limit < maxDeviation:
            illegal=1
            break

    if illegal:
        return 0

    return 1    
