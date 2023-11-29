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
    
    def __init__(self, element_type = 'triangle', mesh_input = 'input.msh', output = 'output', print_id = True, norm=0, angle=0, rotate_dir="x"):
        self.angle = angle
        self.rotate_dir = rotate_dir
        mesh = meshio.read(mesh_input)
        self.points = mesh.points
        self.cells = mesh.cells
        print("Successfully opened input mesh file" )       
        
        if norm == 1:
            self.normalize()
        
        vtu_output = output + "_grid.vtu"
        #meshio.write(vtu_output, self.points, self.cells, cell_data={"index": [np.arange(len(self.cells))}])
        print(".vtu output file written at", vtu_output)        
        
        if element_type == "triangle":
            csv_output = output + ".csv"
            self.textFile_triangle(csv_output, print_id)
            print(".csv output file written at", csv_output)  
        elif element_type == "quad":
            csv_output = output + ".csv"
            self.textFile_square(csv_output, print_id)
            print (".csv output file written at", csv_output)  
        elif element_type == "thetrahedon":
            csv_output = output + ".csv" 
            self.textfile_thetrahedon(csv_output, print_id)
            print (".csv output file written at", csv_output)   
        else:
            print ("Supported element_type are triangle or quad")
         
            
        vtk_output = output + ".vtu"
        self.vtkFile(vtk_output, element_type)
        print (".vtu output file written at", vtk_output)

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
   
    def rotate(self,node):
        rad = self.angle * np.pi / 180
        rotationMatrix = np.array([[np.cos(rad),-np.sin(rad)],[np.sin(rad),np.cos(rad)]])
        return np.array(rotationMatrix.dot(np.array(node)))
    
    def rotate3d(self,node):
        rad = self.angle * np.pi / 180
        rotationMatrix = np.array([[1,0,0],[0,np.cos(rad),-np.sin(rad)],[0,np.sin(rad),np.cos(rad)]])
        if self.rotate_dir == "y" :
            rotationMatrix = np.array([[np.cos(rad),0,np.sin(rad)],[0,1,0],[-np.sin(rad),0,np.cos(rad)]])
        if self.rotate_dir == "z":
            rotationMatrix = np.array([[np.cos(rad),-np.sin(rad),0],[np.sin(rad),np.cos(rad),0],[0,0,1]])
        return np.array(rotationMatrix.dot(np.array(node))) 


    #For now renamed function textfile_triangle
    def textFile_triangle(self, outFile, print_id):
        with open(outFile, "w") as file:
            if print_id:
                file.write("#id x y vol\n")
            else:
                file.write("#x y vol\n")
            i = 0
            for cell in self.cells:
                if cell.type == "triangle":
                    for node in cell.data:
                        area = self.areaTriangle(node)
                        center = self.centerTriangle(node)
                        center = self.rotate(center)
                        
                        if print_id:
                            line = "{:d}, {:.2e}, {:.2e}, {:.2e}".format(i ,center[0], center[1], area )
                        else:
                            line = "{:.2e}, {:.2e}, {:.2e}".format(center[0], center[1], area )
                        file.write(line + os.linesep)
                        i += 1
            file.close()
            
    #For now renamed function textfile_square
    def textFile_square(self, outFile, print_id):
        with open(outFile, "w") as file:
            if print_id:
                file.write("#id x y z vol\n")
            else:
                file.write("#x y z vol\n")
            i = 0
            for cell in self.cells:
                if cell.type == "quad":
                    for node in cell.data:
                        area = self.areaSquare(node)
                        center = self.centerSquare(node)
                        center = self.rotate(center)
                        
                        if print_id:
                            line = "{:d}, {:.2e}, {:.2e}, {:.2e},".format(i ,center[0], center[1], area )
                        else:
                            line = "{:.2e}, {:.2e}, {:.2e}".format(center[0], center[1], area )
                        file.write(line + os.linesep)
                        i += 1
            file.close()

    def textfile_thetrahedon(self, outFile, print_id):
        with open(outFile, "w") as file:
            if print_id:
                file.write("#id x y z vol\n")
            else:
                file.write("#x y z vol\n")
            i = 0
            for cell in self.cells:
            
                if cell.type == "tetra":
                    for node in cell.data:
                        center = self.centerSquare(node)
                        center = self.rotate3d(center)
                        volume = 1
                        if print_id:
                            line = "{:d}, {:.2e}, {:.2e}, {:.2e}, {:.2e}".format(i ,center[0], center[1], center[2], volume )
                        else:
                            line = "{:.2e}, {:.2e}, {:.2e}, {:.2e}".format(center[0], center[1], center[2], volume )
                        file.write(line + os.linesep)
                        i += 1
            file.close()

        
    
    #needs to be rewritten for square and triangle
    def vtkFile(self, outFile, type_ ):
        number = 0
        nodes = []
        for cell in self.cells:
            if cell.type == type_:
                number = len(cell.data)
                nodes = cell.data 

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(outFile)
        grid = vtk.vtkUnstructuredGrid()
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(number)
        points.SetDataTypeToDouble()
        dataOut = grid.GetPointData()
       
        array = vtk.vtkDoubleArray()
        array.SetName("Volume")
        array.SetNumberOfComponents(1)
        array.SetNumberOfTuples(number)
       
        if type_ == "triangle":
            for i in range (0,len(nodes)):
                center = self.centerTriangle(nodes[i])
                center = self.rotate(center)
                area = self.areaTriangle(nodes[i])
                points.InsertPoint(i,center[0],center[1],0)
                array.SetTuple1(i,area)
        elif type_ == "quad":
            for i in range (0,len(nodes)):
                center = self.centerSquare(nodes[i])
                center = self.rotate(center)
                area = self.areaSquare(nodes[i])
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
        
        
        
