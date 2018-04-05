import math

theta = 30
def getAngle(place1,place2,loader):
    dx = loader.coordinates[place2][0] - loader.coordinates[place1][0]
    dy = loader.coordinates[place2][1] - loader.coordinates[place1][1]
    angle = math.degrees(math.atan2(dy,dx))
    return angle

def validPlaces(source, final, destinations, loader):
    angle = getAngle(source,final,loader)
    valid = []
    if angle<0:
        angle = 360-angle

    for i in range(len(destinations)):
        if destinations[i] != final:
            A = getAngle(source,destinations[i],loader)
            if A<0:
                A = 360-A
            if A >= angle-theta and A <= angle+theta:
                valid.append(destinations[i])

    valid.append(final)
    return tuple(sorted(valid))