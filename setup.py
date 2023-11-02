from setuptools import setup


setup(
    name="gmshtoparticles",
    version="0.1",
    description="Transforms a .msh file generated with Gmsh into a particles centered inside each triangle or quad element. Outputs a .csv file description and .vtk/.vtu visualization set of files",
    url="https://github.com/IaPCS/gmsh-to-nodes/",
    author="Patrick Diehl, Ilyass Tabiai",
    author_email="me@diehlpk.de, ilyass.tabiai@gmail.com",
    license="GPL-3.0",
    packages=["gmshtoparticles"],
    zip_safe=False,
)
