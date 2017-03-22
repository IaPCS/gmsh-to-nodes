import meshio
import numpy as np
import os
import vtk

def centerTriangle(node):
    x = points[node[0]]
    y = points[node[1]]
    z = points[node[2]]
    return np.array((x[0] + y[0] + z[0]  , x[1] + y[1] + z[1])) * (1./3.)

def areaTrinagle(node):
    a = points[node[1]] - points[0]
    b = points[node[2]] - points[0]
    return np.linalg.norm(np.cross(a[:] , b[:])) / 2.

def textFile(outFile):
    with open(outFile, "w") as file:
        file.write("#id x y vol\n")
        i = 0
        for node in cells['triangle']:
            area = areaTrinagle(node)
            center = centerTriangle(node)
            line = "{:d} {:.2e} {:.2e} {:.2e}".format(i ,center[0], center[1], area )
            file.write(line + os.linesep)
            i += 1
        file.close()

    
points, cells, point_data, cell_data, field_data = \
meshio.read("untitled.msh")

meshio.write('test.vtu', points, cells, cell_data=cell_data)


textFile("untitled.csv")

vtkFile("peri.vtk")
    



