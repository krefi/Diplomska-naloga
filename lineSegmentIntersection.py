import nodeCopyCount
import bisect
from random import randrange
from sys import setrecursionlimit

setrecursionlimit(10**9)

n = 1000
a = 100000
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
    pbst = nodeCopyCount.PersistentTree()
    for index, point in enumerate(arrayOfPoints):
        # print(index)
        if point.start:
            pbst.insert(point.y)
        else:
            pbst.delete(point.y)
    return pbst

#metoda pridobi število presečišč za podano vertikalno daljico
def getIntersections(line):
    lineVersion = find_last_index(arrayOfPoints, line.startX)
    
    if lineVersion < 0 or line.length == 0:
        return 0
    return persistentTree.countIntervalNodes(line.startY, line.startY + line.length, lineVersion)


#metoda poišče zadno verzijo ki ustreza vertikalni daljici
def find_last_index(arr, target_x):
    left, right = 0, len(arr) - 1
    last_index = -1

    while left <= right:
        mid = left + (right - left) // 2
        obj = arr[mid]

        if obj.x <= target_x:
            if obj.x == target_x and obj.start:
                right = mid - 1
            else:
                last_index = mid
                left = mid + 1
        else:
            right = mid - 1

    return last_index

	
horizontalLines = []
for it in range(n):
    l = Line(randrange(a),randrange(a),randrange(a) + 1)
    horizontalLines.append(l)

arrayOfPoints = getArrayOfPoints(horizontalLines)
persistentTree = createPersistentTree(arrayOfPoints)


# Koda za testiranje pravilnosti algoritma v primerjavi z naivno metodo
# results = []
# bruteforce = []
# for it in range(n):
#     l = Line(randrange(a),randrange(a),randrange(a) + 1)
#     r = getIntersections(l)
#     results.append(r)

#     vx,vy,vd = l.startX, l.startY, l.length
#     cnt = 0
#     for hor in horizontalLines:
#         hx, hy, hd = hor.startX, hor.startY, hor.length
#         if hx<vx<hx+hd and vy<hy<vy+vd:
#             cnt += 1
#     bruteforce.append(cnt)

# assert bruteforce == results




print("Vnesite vertikalne daljice v obliki: x_koordinata_začetka, y_koordinata_konca, dolžina")
while True:
    inputLine = input().split(', ')
    line = Line(int(inputLine[0]), int(inputLine[1]), int(inputLine[2]))
    print(getIntersections(line))
