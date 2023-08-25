import nodeCopy
import bisect

versionsXcoordinate = []


class Line:
    def __init__(self, startX, startY, length):
        self.startX = startX
        self.startY = startY
        self.length = length

class Point:
    def __init__(self, x, y, start):
        self.x = x
        self.y = y
        self.start = start
        
#metoda iz daljic izračuna točke in jih uredi po x koordinati in konce pred začetki
def getArrayOfPoints(arrayOfLines):
    arrayOfPoints = []
    for line in arrayOfLines:
        arrayOfPoints.append(Point(line.startX, line.startY, True))
        arrayOfPoints.append(Point(line.startX + line.length, line.startY, False))
    arrayOfPoints.sort(key=lambda obj: (obj.x, obj.start))
    return arrayOfPoints

#metoda ustvari obstojno drevo iz točk
def createPersistentTree(arrayOfPoints):
    pbst = nodeCopy.PersistentTree()
    for point in arrayOfPoints:
        if point.start:
            pbst.insert(point.y)
        else:
            pbst.delete(point.y)
    return pbst

#metoda pridobi število presečišč za podano vertikalno daljico
def getIntersections(line):
    lineVersion = -1
    for i, point in enumerate(arrayOfPoints):
        if point.x < line.startX:
            lineVersion = i - 1
        elif point.x == line.startX and not point.start:
            lineVersion = i - 1
        else: 
            break

    if lineVersion < 0:
        return 0
    yValues = persistentTree.inorder(lineVersion)
    interesctions = bisect.bisect_left(yValues, line.startY + line.length) - bisect.bisect_right(yValues, line.startY)
    return interesctions


horizontalLines = [Line(5, 9, 4), Line(1, 9, 1), Line(1, 3, 4), Line(3, 5, 6), Line(0, 4, 4), Line(4, 1, 7), Line(6, 3, 2),
                   Line(1, 2, 5), Line(5, 8, 3), Line(4, 6, 6), Line(1, 7, 10)]
arrayOfPoints = getArrayOfPoints(horizontalLines)
persistentTree = createPersistentTree(arrayOfPoints)

print("Vnesite vertikalne daljice v obliki: x_koordinata_začetka, y_koordinata_konca, dolžina")
while True:
    inputLine = input().split(', ')
    line = Line(int(inputLine[0]), int(inputLine[1]), int(inputLine[2]))
    print(getIntersections(line))
