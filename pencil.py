from tkinter import Tk, Canvas, Frame, BOTH
import customKochSnowflake as KochSnowflake
import recursiveKochSnowflake as newKochSnowflake 

class Example(Frame):
    def __init__(self):
        super().__init__()

        self.initUI()

    def iterateKochSnowflake(self, vertices):
        return KochSnowflake.iterate(vertices, KochSnowflake.iterationCounter, KochSnowflake.origSideLen)

    # n is amount of iterations
    def execCustomKochSnowflake(self, n):
        vertices = []
        for i in range(n):
            print(i)
            vertices = self.iterateKochSnowflake(vertices)
            print("VERTICES")
            print(vertices)
        self.connect_Vertices(vertices)

    def execRecursiveKochSnowflake(self, size, n):
        newKochSnowflake.flocon(size, n)
        self.connect_Vertices(newKochSnowflake.getVertices())

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        ##### The below commands each draw a Koch Snowflake
        #self.execRecursiveKochSnowflake(400, 6) # works on all iterations. First argument is length of the original triangle edges, second argument is number of iterations (starts at 0).
        #self.execCustomKochSnowflake(3) # Only works on the first three iterations, although the higher iterations are still pretty. Argument is number of iterations (starts at 1).

    def connect_Vertices(self, vertices):
        canvas = Canvas(self)
        #print(vertices)
        counter = 0
        for i in vertices:
            if counter+1 < len(vertices): # if not last element of vertices
                canvas.create_line(i[0], i[1], vertices[counter+1][0], vertices[counter+1][1])
            else: #if last element of vertices
                #print("last element")
                canvas.create_line(i[0], i[1], vertices[0][0], vertices[0][1]) # connect i (the last element of vertices) to the first vertex, thereby completing the fractal
            counter += 1
        canvas.pack(fill=BOTH, expand=1)

    def test_drawTriangle(self):
        # this is a test for the KochSnowflake.rotateBasis()
        canvas = Canvas(self)
        triangleVertices = KochSnowflake.getInitialVertices(KochSnowflake.origSideLen, KochSnowflake.startPos)
        v1 = triangleVertices[0]
        v2 = triangleVertices[1]
        v3 = triangleVertices[2]

        canvas.create_line(v1[0], v1[1], v2[0], v2[1])
        canvas.create_line(v2[0], v2[1], v3[0], v3[1])
        canvas.create_line(v3[0], v3[1], v1[0], v1[1])

        canvas.pack(fill=BOTH, expand=1)


def main():
    root = Tk()
    ex = Example()
    root.geometry("800x500+250+50")
    root.mainloop()

main()
