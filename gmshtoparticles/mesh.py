# -*- coding: utf-8 -*-
"""
@author: me@diehlpk.de
@author: ilyass.tabiai@gmail.com
"""
import meshio
import numpy as np
import os
import vtk

class GmshToParticles():
    
    def __init__(self, element_type = 'triangle', mesh_input = 'input.msh', output = 'output',norm=0):
        self.points, self.cells, point_data, cell_data, field_data = \
        meshio.read(mesh_input)
        print "Successfully opened input mesh file"        
        
        if norm == 1:
            self.normalize()
        
        vtu_output = output + "_grid.vtu"
        meshio.write(vtu_output, self.points, self.cells, cell_data=cell_data)
        print ".vtu output file written at", vtu_output        
        
        if element_type == "triangle":
            csv_output = output + ".csv"
            self.textFile_triangle(csv_output)
            print ".csv output file written at", csv_output  
        elif element_type == "quad":
            csv_output = output + ".csv"
            self.textFile_square(csv_output)
            print ".csv output file written at", csv_output  
        else:
            print "Supported element_type are triangle or quad"
         
            
        vtk_output = output + ".vtu"
        self.vtkFile(vtk_output, element_type)
        print ".vtu output file written at", vtk_output

    def centerTriangle(self, node):
        x = self.points[node[0]]
        y = self.points[node[1]]
        z = self.points[node[2]]
        return np.array((x[0] + y[0] + z[0]  , x[1] + y[1] + z[1])) * (1./3.)
        
        
    def centerSquare(self, node):
        a = self.points[node[0]]
        b = self.points[node[1]]
        c = self.points[node[2]]
        d = self.points[node[3]]
        return np.array((a+b+c+d)/4.)
    
    def areaTriangle(self, node):
        a = self.points[node[1]] - self.points[node[0]]
        b = self.points[node[2]] - self.points[node[0]]
        return np.linalg.norm(np.cross(a[:] , b[:])) / 2.
        
    def areaSquare(self, node):
        a = self.points[node[1]] - self.points[node[0]]
        b = self.points[node[2]] - self.points[node[0]]
        return np.linalg.norm(a*b)
    
    #For now renamed function textfile_triangle
    def textFile_triangle(self, outFile):
        with open(outFile, "w") as file:
            file.write("#id x y vol\n")
            i = 0
            for node in self.cells['triangle']:
                area = self.areaTriangle(node)
                center = self.centerTriangle(node)
                line = "{:d} {:.2e} {:.2e} {:.2e}".format(i ,center[0], center[1], area )
                file.write(line + os.linesep)
                i += 1
            file.close()
            
    #For now renamed function textfile_square
    def textFile_square(self, outFile):
        with open(outFile, "w") as file:
            file.write("#id x y vol\n")
            i = 0
            for node in self.cells['quad']:
                area = self.areaSquare(node)
                center = self.centerSquare(node)
                line = "{:d} {:.2e} {:.2e} {:.2e}".format(i ,center[0], center[1], area )
                file.write(line + os.linesep)
                i += 1
            file.close()
    
    #needs to be rewritten for square and triangle
    def vtkFile(self, outFile, type_ ):
        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(outFile)
        grid = vtk.vtkUnstructuredGrid()
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(len(self.cells[type_]))
        points.SetDataTypeToDouble()
        dataOut = grid.GetPointData()
       
        array = vtk.vtkDoubleArray()
        array.SetName("Volume")
        array.SetNumberOfComponents(1)
        array.SetNumberOfTuples(len(self.cells[type_]))
       
        if type_ == "triangle":
            for i in range (0,len(self.cells[type_])):
                center = self.centerTriangle(self.cells[type_][i])
                area = self.areaTriangle(self.cells[type_][i])
                points.InsertPoint(i,center[0],center[1],0)
                array.SetTuple1(i,area)
        elif type_ == "quad":
            for i in range (0,len(self.cells[type_])):
                center = self.centerSquare(self.cells[type_][i])
                area = self.areaSquare(self.cells[type_][i])
                points.InsertPoint(i,center[0],center[1],0)
                array.SetTuple1(i,area)

       
        grid.SetPoints(points)
        dataOut.AddArray(array)
       
        writer.SetInputData(grid)
    
        writer.GetCompressor().SetCompressionLevel(0)
        writer.SetDataModeToAscii()
        writer.Write()

    def normalize(self):
        
        minDirection = np.zeros((3))    
        minDirection[0] = min(self.points[:,0])
        minDirection[1] = min(self.points[:,1])
        minDirection[2] = min(self.points[:,2])
        
        self.points -= minDirection
        
        
        
