import numpy as np

vertices = [np.array([250, 150])] # start position

def getVertices():
    global vertices
    return vertices

def saveVertex(v):
    global vertices
    vertices.append(v)

# startcord should just be last element of global vertices[]
def vonkoch(l, n, basis):
    basis_inv = np.linalg.inv(basis)
    if n == 0:
        #move forward l pixels
        v = vertices[-1]
        print(v)
        v = np.dot(basis, v) # change basis
        v = np.array([v[0]+l, v[1]]) # add l to x-axis
        print(v)
        print(basis_inv)
        v = np.dot(basis_inv, v) # change back to old basis
        saveVertex(v) # save vertex to vertices[] list
    else:
        basis = vonkoch(l/3, n-1, basis)

        # turn left 60 degrees (pi/3 radians)
        basis = getRotatedBase(basis, np.pi/3)
        basis = vonkoch(l/3, n-1, basis)

        # turn right 120 degrees (-2*pi/3 radians)
        basis = getRotatedBase(basis, -2*np.pi/3)
        basis = vonkoch(l/3, n-1, basis)

        # turn left 60 degrees (pi/3 radians)
        basis = getRotatedBase(basis, np.pi/3)
        basis = vonkoch(l/3, n-1, basis)

    return basis

def flocon(l, n):
    global vertices
    idmatrix = np.array([[1,0], [0,1]])
    basis = vonkoch(l, n, idmatrix) # last arg is identity matrix

    # turn right 120 degrees
    basis = getRotatedBase(basis, -2*np.pi/3)
    basis = vonkoch(l, n, basis)

    # turn right 120 degrees
    basis = getRotatedBase(basis, -2*np.pi/3)
    vonkoch(l, n, basis)


# generates and returns new base matrix where the base is rotated by the amount of radians specified by parameter
# negative radian is clockwise rotation, positive is counter clockwise rotation
def getRotatedBase(origBaseMatrix, radians):
    rotationMatrix = np.array([[np.cos(radians), (-np.sin(radians))],[np.sin(radians), np.cos(radians)]])
    return np.dot(rotationMatrix, origBaseMatrix)