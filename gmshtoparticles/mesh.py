# -*- coding: utf-8 -*-
"""
@author: me@diehlpk.de
@author: ilyass.tabiai@gmail.com
"""
import os
import meshio
import numpy as np
import vtk


class GmshToParticles:
    def __init__(
        self,
        element_type="triangle",
        mesh_input="input.msh",
        output="output",
        print_id=True,
        norm=0,
        angle=0,
    ):
        self.angle = angle
        mesh = meshio.read(mesh_input)
        self.points = mesh.points
        self.cells = mesh.cells
        print("Successfully opened input mesh file")

        if norm == 1:
            self.normalize()

        vtu_output = output + "_grid.vtu"
        print(".vtu output file written at", vtu_output)

        if element_type == "triangle":
            csv_output = output + ".csv"
            self.text_file_triangle(csv_output, print_id)
            print(".csv output file written at", csv_output)
        elif element_type == "quad":
            csv_output = output + ".csv"
            self.text_file_square(csv_output, print_id)
            print(".csv output file written at", csv_output)
        else:
            print("Supported element_type are triangle or quad")

        vtk_output = output + ".vtu"
        self.vtk_file(vtk_output, element_type)
        print(".vtu output file written at", vtk_output)

    def center_triangle(self, node):
        x = self.points[node[0]]
        y = self.points[node[1]]
        z = self.points[node[2]]
        return np.array((x[0] + y[0] + z[0], x[1] + y[1] + z[1])) * (1.0 / 3.0)

    def center_square(self, node):
        a = self.points[node[0]]
        b = self.points[node[1]]
        c = self.points[node[2]]
        d = self.points[node[3]]
        return np.array((a + b + c + d) / 4.0)

    def area_triangle(self, node):
        a = self.points[node[1]] - self.points[node[0]]
        b = self.points[node[2]] - self.points[node[0]]
        return np.linalg.norm(np.cross(a[:], b[:])) / 2.0

    def area_square(self, node):
        a = self.points[node[1]] - self.points[node[0]]
        b = self.points[node[2]] - self.points[node[0]]
        return np.linalg.norm(a * b)

    def rotate(self, node):
        rad = self.angle * np.pi / 180
        rotating_matrix = np.array(
            [[np.cos(rad), -np.sin(rad)], [np.sin(rad), np.cos(rad)]]
        )
        return np.array(rotating_matrix.dot(np.array(node)))

    # For now renamed function text_file_triangle
    def text_file_triangle(self, out_file, print_id):
        with open(out_file, "w") as file:
            if print_id:
                file.write("#id x y vol\n")
            else:
                file.write("#x y vol\n")
            i = 0
            for cell in self.cells:
                if cell.type == "triangle":
                    for node in cell.data:
                        area = self.area_triangle(node)
                        center = self.center_triangle(node)
                        center = self.rotate(center)

                        if print_id:
                            line = "{:d}, {:.2e}, {:.2e}, {:.2e}".format(
                                i, center[0], center[1], area
                            )
                        else:
                            line = "{:.2e}, {:.2e}, {:.2e}".format(
                                center[0], center[1], area
                            )
                        file.write(line + os.linesep)
                        i += 1
            file.close()

    # For now renamed function text_file_square
    def text_file_square(self, out_file, print_id):
        with open(out_file, "w") as file:
            if print_id:
                file.write("#id x y vol\n")
            else:
                file.write("#x y vol\n")
            i = 0
            for cell in self.cells:
                if cell.type == "quad":
                    for node in cell.data:
                        area = self.area_square(node)
                        center = self.center_square(node)
                        center = self.rotate(center)

                        if print_id:
                            line = "{:d}, {:.2e}, {:.2e}, {:.2e}".format(
                                i, center[0], center[1], area
                            )
                        else:
                            line = "{:.2e}, {:.2e}, {:.2e}".format(
                                center[0], center[1], area
                            )
                        file.write(line + os.linesep)
                        i += 1
            file.close()

    # needs to be rewritten for square and triangle
    def vtk_file(self, out_file, type_):
        number = 0
        nodes = []
        for cell in self.cells:
            if cell.type == type_:
                number = len(cell.data)
                nodes = cell.data

        writer = vtk.vtkXMLUnstructuredGridWriter()
        writer.SetFileName(out_file)
        grid = vtk.vtkUnstructuredGrid()
        points = vtk.vtkPoints()
        points.SetNumberOfPoints(number)
        points.SetDataTypeToDouble()
        data_out = grid.GetPointData()

        array = vtk.vtkDoubleArray()
        array.SetName("Volume")
        array.SetNumberOfComponents(1)
        array.SetNumberOfTuples(number)

        if type_ == "triangle":
            for i in range(0, len(nodes)):
                center = self.center_triangle(nodes[i])
                center = self.rotate(center)
                area = self.area_triangle(nodes[i])
                points.InsertPoint(i, center[0], center[1], 0)
                array.SetTuple1(i, area)
        elif type_ == "quad":
            for i in range(0, len(nodes)):
                center = self.center_square(nodes[i])
                center = self.rotate(center)
                area = self.area_square(nodes[i])
                points.InsertPoint(i, center[0], center[1], 0)
                array.SetTuple1(i, area)

        grid.SetPoints(points)
        data_out.AddArray(array)

        writer.SetInputData(grid)

        writer.GetCompressor().SetCompressionLevel(0)
        writer.SetDataModeToAscii()
        writer.Write()

    def normalize(self):
        min_direction = np.zeros((3))
        min_direction[0] = min(self.points[:, 0])
        min_direction[1] = min(self.points[:, 1])
        min_direction[2] = min(self.points[:, 2])

        self.points -= min_direction
