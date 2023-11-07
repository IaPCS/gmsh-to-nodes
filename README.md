# gmsh-to-paticles

Generates nodes and volumes from gmsh grid for nodal or particle simulations

# Install

### Requirements

``sudo pip3 install -r requirements.txt`

### Development

Any changes made in the source file will immediately be changed in the installed package:

`sudo python3 setup.py develop`

### Production

`sudo python3 setup.py install`

# Usage

### Standalone 

```bash
python3 convert.py -i <inputfile> -o <outputfile> -t <type> -d <index> -r <rotation>
```

Parameters:

* `-i` : Path to the mesh file
* `-o` : Path to the output file (Do not add any file extension)
* `-t` : Type of the mesh elements (Only quad and triangles are supported)
* `-d` : Add the index of each node to the CSV output (Default is True)
* '-r' : Rotate the nodes by the given degress (Default is zero degrees)

# Examples

### 2D

Mesh generated with gmesh | Nodes and volumes at the center of the cell
:------------------------:|:----------------------------------------:
![Mesh](./gmshtoparticles/examples/triangle_mesh.png?raw=true "Mesh generated with gmesh")|![Exodus](./gmshtoparticles/examples/triangle_nodes.png?raw=true "Mesh generated with gmesh")
