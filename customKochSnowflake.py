import numpy as np

origSideLen = 200 # initial side length of the triangle. sidelen will be origSideLen / 4**iterationCounter, as the lengths of the edges are 100 to begin with, then 100/4, then 100/16, 100/64 and so on.
startPos = (250, 150) # position of the upper left vertex in the initial downward facing triangle
vertices = [] # list of coordinate tuples of the vertices. Should def use vectors instead of tuples though...
iterationCounter = 0 # iteration counter. Starts at 0, which is just the initial triangle

# increments the iterationCounter by 1
def incrIterationCounter():
    global iterationCounter
    iterationCounter = iterationCounter + 1
    print("incrIterationCounter(): " + str(iterationCounter))
# function that actually generates the fractal. Given a list of sorted/sequences vertices it will return a new list of sorted
# vertices one iteration above the vertices given
def iterate(vertices, iterationCounter, origSideLen):
    global startPos
    if iterationCounter == 0: # if first iteration, draw triangle
        incrIterationCounter()
        return getInitialVertices(origSideLen, startPos)

    newVertices = []
    counter = 0
    basis = np.array([[1,0],[0,1]]) # let it be the standard base before the loop
    for i in vertices:
        #v1 and v2 are the vertices on whose shared edge a new triangle will be generated
        v1 = i
        if counter + 1 < len(vertices):  # if i isn't the last vertex in vertices
            v2 = vertices[counter+1]
        else:  # if i is the last vertex in vertices (then v2 has to be first vertex)
            v2 = vertices[0]

        # get the rotated basematrix ONLY FIRST THREE ITERATIONS WORK (btw, seems like coeff is redundant)
        if iterationCounter == 1: # hvis 2. iteration
            if counter == 0: # første gang skal basen ikke skifte, da den første kant altid er vandret
                pass
                coeff = 1
            else: # hver gang skal rotationen være CW 120 grader (radian: -2*pi/3)
                basis = getRotatedBase(basis,  (-2 *np.pi / 3))
                coeff = 1
        elif iterationCounter > 1 : # tredje iteration
            if counter == 0: # første gang skal basen ikke skifte, da den første kant altid er vandret
                pass
                coeff = 1
            elif counter%2 == 1: # hver anden gang, skal rotationen være CCW 60 grader (radian: pi/3)
                basis = getRotatedBase(basis,  np.pi / 3)
                coeff = 1
            else: # hver anden gang skal rotationen være CW 120 grader (radian: -2*pi/3)
                basis = getRotatedBase(basis,  (-2 *np.pi / 3))
                coeff = 1

        # THE FOLLOWING IS A TEMPORARY SOLUTION TO MAKE THE SECOND ITERATION WORK ; PROBABLY WON'T WORK FOR HIGHER ITERATIONS
        #if counter == 2:  # if third iteration
        #    coeff = -1  # let the coefficient of genTriCoordsFromEdge() be -1
        #else:
        #    coeff = 1  # otherwise let coefficient be 1


        # change basis of v1 and v2
        v1_rotatedBase = np.dot(basis, v1)
        v2_rotatedBase = np.dot(basis, v2)
        sidelen = np.linalg.norm(v1_rotatedBase-v2_rotatedBase) # get the euclidian norm before v1 and v2 is made into tuples
        #make them tuples (because genTriCoordsFromEdge expects tuples, not arrays)
        v1_rotatedBase = (v1_rotatedBase[0], v1_rotatedBase[1])
        v2_rotatedBase = (v2_rotatedBase[0], v2_rotatedBase[1])
        print("v1: " + str(v1) + " , v2: " + str(v2))
        print("v1_rotatedBase: " + str(v1_rotatedBase) + " , v2_rotatedBase: " + str(v2_rotatedBase))
        print("sidelen: " + str(sidelen))
        # generate new triangle coordinates from the edge shared by v1 and v2
        newTriCoords_rotatedBase = genTriCoordsFromEdge(v1_rotatedBase, v2_rotatedBase, sidelen, coeff)  # the amount of edges is multiplied by 4 per iteration
        print("newTriCoords_rotatedBase: "+str(newTriCoords_rotatedBase))
        # switch the newTriCoords back to the old [1,0][0,1] base
        invRotatedBase = np.linalg.inv(basis) # HUSK: identitetsmatricen er sin egen inverse, så det her skaber ikke problemer i første iteration hvor basen slet ikke skal skiftes
        newTriCoords = (np.dot(invRotatedBase, newTriCoords_rotatedBase[0]), np.dot(invRotatedBase, newTriCoords_rotatedBase[1]), np.dot(invRotatedBase, newTriCoords_rotatedBase[2]))
        print("newTriCoords: " + str(newTriCoords))
        # sort the coords so that they're in sequence
        sortedNewVertices = sortVertices(v1, newTriCoords)
        print("sortedNewVertices: " + str(sortedNewVertices))

        for j in range(4): newVertices.append(sortedNewVertices[j]) # add the sorted new vertices to newVertices

        counter += 1

    incrIterationCounter() # increments the iteration counter
    return newVertices

# returns coords of the three vertices of the initial downward facing triangle
def getInitialVertices(origSideLen, startPos):
    v2 = (startPos[0]+origSideLen, startPos[1])

    stdbase = np.array([[1, 0], [0, 1]])
    rotatedBase = getRotatedBase(stdbase, -2 * np.pi / 3)
    # skift v2 til rotatedBase, tilføj sidelen til dens x-akse, og det vil være det nye hjørne af trekanten, skift så tilbage til almindelig base og voila.
    v2_rotatedBase = np.dot(rotatedBase, v2)
    v3_rotatedBase = np.array([v2_rotatedBase[0] + origSideLen, v2_rotatedBase[1]])  # add sidelen to x-axis
    backwardsTransformationMatrix = np.linalg.inv(rotatedBase)
    v3 = np.dot(backwardsTransformationMatrix, v3_rotatedBase)  # gå fra v3 i roteret base til stdbase
    v3 = (v3[0], v3[1]) # change from vector to tuple

    return (startPos, v2, v3)
# generates coordinates for new triangle on an edge.
# args: v1 and v2 are the vertices at the ends of the edge
# returns tuple of 3 new vertices
# NEW STUFF (temporary): coeff parameter should be 1 or -1. At the second iteration of the snowflake
# it should be 1 for the first two edges, and then -1 for the third edge.
# Otherwise the third edge's triangle will point inwards and will stick out. This solution is temporary.
def genTriCoordsFromEdge(v1, v2, edgeLength, coeff):
    assert type(v1) == tuple and type(v2) == tuple

    b = (v1[0] + coeff * (edgeLength / 3), v1[1])
    a = (v1[0] + coeff * (edgeLength / 2), v1[1])
    c = (v1[0] + coeff * (2*edgeLength / 3), v1[1])
    d = (a[0], v1[1] - coeff * np.sqrt((edgeLength/3)**2 - (edgeLength/6)**2))

    return (b,d,c)
# v1 is the coordinate at the start of the edge, and triangleTuple consists of 3 coordinates (b,c,d) from the return
# value of genTriCoordsFromEdge(). The return value of sortVertices() is a tuple (v1,b,d,c). Note that v2, the coordinate at
# the end of the edge is not present - that's because of the way that the fractal is being iterated in iterate(). Had v2
# been included, there would have been duplicates, as v2 becomes v1 in the next edge and so on.
# the purpose of sorting the coordinates like this is to sort the global variable "vertices" to prepare for the next
# iteration. All the coordinates must be in sequence so that the vertices of the fractal are in sequence, allowing easy
# recognition of edges
def sortVertices(v1, triangleTuple):
    return (v1,triangleTuple[0], triangleTuple[1], triangleTuple[2])
# generates and returns new base matrix where the base is rotated by the amount of radians specified by parameter
# negative radian is clockwise rotation, positive is counter clockwise rotation
def getRotatedBase(origBaseMatrix, radians):
    rotationMatrix = np.array([[np.cos(radians), (-np.sin(radians))],[np.sin(radians), np.cos(radians)]])
    return np.dot(rotationMatrix, origBaseMatrix)



# TESTING AREA