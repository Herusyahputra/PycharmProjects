import pyvista as pv

# Load the mesh from a file
mesh = pv.read('design/new-bowl.obj')

# Load the texture image from a file
texture = pv.read_texture('design/0223_114246.png')

# Create the texture map
tex_map = pv.Texture(texture)

# Apply the texture map to the mesh
mesh.set_texture(tex_map)

# Render the mesh with the texture map
plotter = pv.Plotter()
plotter.add_mesh(mesh)
plotter.show()

import pyvista as pv

# Load the mesh from a file
mesh = pv.read('mesh.stl')

# Load the texture image from a file
texture = pv.read_texture('texture.jpg')

# Create the texture map
tex_map = pv.Texture(texture)

# Get the mapper for the mesh
mapper = mesh.mapper

# Set the texture map for the mapper
mapper.texture_map = tex_map

# Render the mesh with the texture map
plotter = pv.Plotter()
plotter.add_mesh(mesh)
plotter.show()