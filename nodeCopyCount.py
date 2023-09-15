#razred vozlišča. Vozlišče ima vrednost, levi in desni kazalec ter dodatne kazalce
class Node:
    def __init__(self, key, version):
        self.key = key
        self.left = Pointer(None, version, 0)
        self.right = Pointer(None, version, 1)
        self.extraPointers = []
        self.leftCount = [CountField(0, version)]
        self.rightCount = [CountField(0, version)]


class CountField:
    def __init__(self, count, version):
        self.subCount = count
        self.version = version
        
#Polje kazalca je sestavljeno iz tarče na kero kaže, verzije in imena polja(smer)
class Pointer:
    def __init__(self, target, version, direction):
        self.target = target
        self.version = version
        self.direction = direction #0 za levi kazalec, 1 za desni kazalec

class PersistentTree:
    def __init__(self):
        self.E = 1
        self.accessArray = []

    #rekurzivna metoda za vnos nove vrednosti
    def recInsert(self ,key, version, node):
        if node is None:
            return (Node(key, version), True)
        
        #poiščemo kazalca za levo in desno z najvišjo oznako verzije
        latestLeftPointer = self.findLatestValidLeftPointer(node, version)
        latestRightPointer = self.findLatestValidRightPointer(node, version)

        if key <= node.key:
            #poiščemo kazalec levo z najvišjo verzijo
            newNode = self.recInsert(key, version, latestLeftPointer)
            if len(newNode) == 3:
                return (node, False, False)


            node.leftCount.append(CountField(node.leftCount[-1].subCount + 1, version))

            if newNode[1] == True:
                if len(node.extraPointers) < self.E:
                    node.extraPointers.append(Pointer(newNode[0], version, 0))
                    return (node, False)
                else:
                    copyNode = Node(node.key, version)
                    copyNode.right.target = latestRightPointer
                    copyNode.left.target = newNode[0]
                    copyNode.leftCount[0].subCount = node.leftCount[-1].subCount
                    copyNode.rightCount[0].subCount = node.rightCount[-1].subCount
                    return (copyNode, True)
            return (node, False)
            
                
        if key > node.key:
            # poiščemo kazalec desno z najvišjo verzijo
            newNode = self.recInsert(key, version, latestRightPointer)
            if len(newNode) == 3:
                return(node, False, False)
            node.rightCount.append(CountField(node.rightCount[-1].subCount + 1, version))

            if newNode[1] == True:
                if len(node.extraPointers) < self.E:
                    node.extraPointers.append(Pointer(newNode[0], version, 1))
                    return (node, False)
                else:
                    copyNode = Node(node.key, version)
                    copyNode.left.target = latestLeftPointer
                    copyNode.right.target = newNode[0]
                    copyNode.leftCount[0].subCount = node.leftCount[-1].subCount
                    copyNode.rightCount[0].subCount = node.rightCount[-1].subCount
                    return (copyNode, True)
            return (node, False)
        return (node, False, False)

    #metoda ki kliče rekurzivno metodo za vnos vrednosti in posodobi seznam kazalcev dostopa
    def insert(self, key):
        root = self.accessArray[-1] if len (self.accessArray) > 0 else None
        rootNodeTuple = self.recInsert(key, len(self.accessArray), root)
        rootNode = rootNodeTuple[0]
        self.accessArray.append(rootNode)

    #rekurzivna metoda za izpis vozlišč v dani verziji
    def inorderRec(self, node, version, result):
        if node is not None:
            #poiščemo levi kazalec z najvišjo verzijo ki je manjša ali enaka verziji po kateri poizvedujemo
            validLeftNode = self.findLatestValidLeftPointer(node, version)
            self.inorderRec(validLeftNode, version, result)
            result.append(node.key)
            #poiščemo desni kazalec z najvišjo verzijo ki je manjša ali enaka verziji po kateri poizvedujemo
            validrightNode = self.findLatestValidRightPointer(node, version)
            self.inorderRec(validrightNode, version, result)

    #metoda ki požene rekurzivno metodo za izpis vozlišč za dano verzijo
    def inorder(self, version):
        result = []
        self.inorderRec(self.accessArray[version], version, result)
        return result

    #metoda ki požene rekurzivno metodo za izbris in posodobi seznam kazalcev dostopa
    def delete(self, key):
        if len (self.accessArray) == 0:
            print("Obstojna podatkovna struktura je prazna")
            return
        root = self.accessArray[-1]
        rootNodeTuple = self.deleteRec(key, len(self.accessArray), root)
        rootNode = rootNodeTuple[0]
        self.accessArray.append(rootNode)

    #rekurzivna metoda za izbris vozlišča
    def deleteRec(self, key, version, node):
        if node is None:
            return (node, False, False)
        
        latestLeftPointer = self.findLatestValidLeftPointer(node, version)
        latestRightPointer = self.findLatestValidRightPointer(node, version)
        
        if key < node.key:
            recNode = self.deleteRec(key, version, latestLeftPointer)
            if len(recNode) == 3:
                return(node, False, False)

            node.leftCount.append(CountField(node.leftCount[-1].subCount - 1, version))
            if recNode[1] == True:
                if len(node.extraPointers) < self.E:
                    node.extraPointers.append(Pointer(recNode[0], version, 0))
                    return (node, False)
                else:
                    copyNode = Node(node.key, version)
                    copyNode.right.target = latestRightPointer
                    copyNode.left.target = recNode[0]
                    copyNode.leftCount[0].subCount = node.leftCount[-1].subCount
                    copyNode.rightCount[0].subCount = node.rightCount[-1].subCount
                    return (copyNode, True)
            return (node, False)
        elif key > node.key:
            recNode = self.deleteRec(key, version, latestRightPointer)
            if len(recNode) == 3:
                return(node, False, False)
            node.rightCount.append(CountField(node.rightCount[-1].subCount - 1, version))
            if recNode[1] == True:
                if len(node.extraPointers) < self.E:
                    node.extraPointers.append(Pointer(recNode[0], version, 1))
                    return (node, False)
                else:
                    copyNode = Node(node.key, version)
                    copyNode.left.target = latestLeftPointer
                    copyNode.right.target = recNode[0]
                    copyNode.leftCount[0].subCount = node.leftCount[-1].subCount
                    copyNode.rightCount[0].subCount = node.rightCount[-1].subCount
                    return (copyNode, True)
            return (node, False)
        else:
            #Vozilšče ima samo enega ali pa nobenega sina
            if latestLeftPointer is None:
                return (latestRightPointer, True)
            
            elif latestRightPointer is None:
                return (latestLeftPointer, True)

            #Vozlišče ima oba sinova
            inorderSuccessor = self.minNode(latestRightPointer, version)
            rightTarget = self.deleteRec(inorderSuccessor.key, version, latestRightPointer)[0]
            if len(inorderSuccessor.extraPointers) < self.E - 1:
                inorderSuccessor.extraPointers.append(Pointer(latestLeftPointer, version, 0))
                inorderSuccessor.extraPointers.append(Pointer(rightTarget, version, 1))
                inorderSuccessor.leftCount.append(CountField(node.leftCount[-1].subCount, version))
                inorderSuccessor.rightCount.append(CountField(node.rightCount[-1].subCount - 1, version))
                return (inorderSuccessor, True)
            else: 
                copyNode = Node(inorderSuccessor.key, version)
                copyNode.right.target = rightTarget
                copyNode.left.target = latestLeftPointer
                copyNode.leftCount[0].subCount = node.leftCount[-1].subCount
                copyNode.rightCount[0].subCount = node.rightCount[-1].subCount - 1
                return (copyNode, True)

    #metoda najde najnižjo vrednost poddrevesa z podanim začetkom, za določeno verzijo
    def minNode(self, node, version):
        currentNode = node
        while True:
            nextNode = self.findLatestValidLeftPointer(currentNode, version)
            if nextNode is None:
                break
            currentNode = nextNode
        return currentNode

    #metoda najde levi kazalec v vozlišču z najvišjo verzijo manjšo ali enako podani verziji
    def findLatestValidLeftPointer(self, node, version):
        leftExtraPointers = [ep for ep in node.extraPointers if ep.direction == 0 and ep.version <= version]
        leftPointers = [node.left]
        leftPointers.extend(leftExtraPointers)
        return max(leftPointers, key=lambda pointer: pointer.version).target

    #metoda najde desni kazalec v vozlišču z najvišjo verzijo manjšo ali enako podani verziji
    def findLatestValidRightPointer(self, node, version):
        rightExtraPointers = [ep for ep in node.extraPointers if ep.direction == 1 and ep.version <= version]
        rightPointers = [node.right]
        rightPointers.extend(rightExtraPointers)
        return max(rightPointers, key=lambda pointer: pointer.version).target

        
    def nodeRightCount(self, node, version):
        return self.findVersionCount(node.rightCount, version)
        
    
    def findVersionCount(self, arr, version):
        left, right = 0, len(arr) - 1
        versionCount = 0

        while left <= right:
            mid = left + (right - left) // 2
            obj = arr[mid]

            if obj.version <= version:
                versionCount = obj.subCount
                left = mid + 1
            else:
                right = mid - 1

        return versionCount


    # poišče število vozlišč večjih od prvega vozlišča večjega od tarče
    def findFirstGreaterNodeCount(self, root, target, version):
        closestNodeCount = 0
        closestNode = None
        while root:
            if root.key > target:
                closestNode = root
                closestNodeCount += self.nodeRightCount(root, version) + 1
                root = self.findLatestValidLeftPointer(root, version)
            else:
                root = self.findLatestValidRightPointer(root, version)

        return closestNodeCount + self.nodeRightCount(closestNode, version) if root == closestNode and closestNode else closestNodeCount
    
    # poišče število vozlišč večjih od prvega vozlišča manjšega od tarče
    def findFirstLowerNodeCount(self, root, target, version):
        closestNodeCount = 0
        currNodeCount = 0
        closestNode = None

        while root:
            if root.key < target:
                closestNodeCount = currNodeCount
                closestNode = root
                root = self.findLatestValidRightPointer(root, version)
            else:
                currNodeCount += self.nodeRightCount(root, version) + 1
                root = self.findLatestValidLeftPointer(root, version)

        return closestNodeCount + self.nodeRightCount(closestNode, version) if closestNode else currNodeCount
    

    def countIntervalNodes(self, low, high, version):
        return self.findFirstGreaterNodeCount(self.accessArray[version], low, version) - self.findFirstLowerNodeCount(self.accessArray[version], high, version)
