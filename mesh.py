import meshio
import numpy as np
import os
import vtk
import pdb

def centerTriangle(node):
    x = points[node[0]]
    y = points[node[1]]
    z = points[node[2]]
    return np.array((x[0] + y[0] + z[0]  , x[1] + y[1] + z[1])) * (1./3.)
    
    
def centerSquare(node):
    a = points[node[0]]
    b = points[node[1]]
    c = points[node[2]]
    d = points[node[3]]
    #pdb.set_trace()
    print a, b, c, d
    print np.array((a+b+c+d)/4.)
    print
    return np.array((a+b+c+d)/4.)

def areaTriangle(node):
    a = points[node[1]] - points[node[0]]
    b = points[node[2]] - points[node[0]]
    return np.linalg.norm(np.cross(a[:] , b[:])) / 2.
    
def areaSquare(node):
    a = points[node[1]] - points[node[0]]
    b = points[node[2]] - points[node[0]]
    return np.linalg.norm(a*b)

#For now renamed function textfile_triangle
def textFile_triangle(outFile):
    with open(outFile, "w") as file:
        file.write("#id x y vol\n")
        i = 0
        for node in cells['triangle']:
            area = areaTriangle(node)
            center = centerTriangle(node)
            line = "{:d} {:.2e} {:.2e} {:.2e}".format(i ,center[0], center[1], area )
            file.write(line + os.linesep)
            i += 1
        file.close()
        
#For now renamed function textfile_square
def textFile_square(outFile):
    with open(outFile, "w") as file:
        file.write("#id x y vol\n")
        i = 0
        for node in cells['quad']:
            area = areaSquare(node)
            center = centerSquare(node)
            line = "{:d} {:.2e} {:.2e} {:.2e}".format(i ,center[0], center[1], area )
            file.write(line + os.linesep)
            i += 1
        file.close()

#needs to be rewritten for square and triangle
def vtkFile(outFile, type_ = 'triangle'):
   writer = vtk.vtkXMLUnstructuredGridWriter()
   writer.SetFileName(outFile)
   grid = vtk.vtkUnstructuredGrid()
   points = vtk.vtkPoints()
   points.SetNumberOfPoints(len(cells[type_]))
   points.SetDataTypeToDouble()
   dataOut = grid.GetPointData()
   
   array = vtk.vtkDoubleArray()
   array.SetName("Volume")
   array.SetNumberOfComponents(1)
   array.SetNumberOfTuples(len(cells[type_]))
   
   for i in range (0,len(cells[type_])):
       center = centerSquare(cells[type_][i])
       area = areaSquare(cells[type_][i])
       points.InsertPoint(i,center[0],center[1],0)
       array.SetTuple1(i,area)
   
   grid.SetPoints(points)
   dataOut.AddArray(array)
   
   writer.SetInputData(grid)

   writer.GetCompressor().SetCompressionLevel(0)
   writer.SetDataModeToAscii()
   writer.Write()
    
points, cells, point_data, cell_data, field_data = \
meshio.read("regular_square.msh")

meshio.write('test.vtu', points, cells, cell_data=cell_data)


textFile_square("untitled.csv")
vtkFile("test.vtk", type_ = 'quad')

    



