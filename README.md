# gmsh-to-paticles

Gnerates nodes and volumes from gmsh grid for nodal or particle simulations

# Install

### Requirements

``sudo pip install -r requirements.txt`

### Development

Any changes made in the source file will immediately be changed in the installed package:

`sudo python setup.py develop`

### Production

`sudo python setup.py install`

# Usage

### Standalone 

```bash
python convert.py -i <inputfile> -o <outputfile> -t <type>
```

# Examples

### 2D

Mesh generated with gmesh | Nodes and volumes at the center of the cell
:------------------------:|:----------------------------------------:
![Mesh](./gmshtoparticles/examples/triangle_mesh.png?raw=true "Mesh generated with gmesh")|![Exodus](./gmshtoparticles/examples/triangle_nodes.png?raw=true "Mesh generated with gmesh")
