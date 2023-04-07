# import pyvista as pv
#
# # Load the 3D model in OBJ format
# mesh = pv.read('/home/heru-demo/PycharmProjects/surounding_3D/3D Demensi/3d/Front.obj')
#
# # Load the texture image in PNG format
# texture = pv.read_texture('/home/heru-demo/PycharmProjects/surounding_3D/3D Demensi/image/front.png')
# print("update")
#
# # Create a texture map for the mesh
# mesh.texture_map_to_plane(inplace=True)
#
# # Set the texture for the mesh
# mesh.texture = texture
#
# # Show the mesh with the texture
# plotter = pv.Plotter()
# plotter.add_mesh(mesh)
# plotter.show()

import pyvista as pv
import numpy as np

# Load the 3D model in OBJ format
mesh = pv.read(/home/heru-demo/PycharmProjects/surounding_3D/3D Demensi/3d/Front.obj")

# Load the texture images and combine them into a texture atlas
atlas_size = 2048  # Size of the texture atlas
textures = []
for i in range(10):
    texture = pv.read_texture("/home/heru-demo/PycharmProjects/surounding_3D/3D Demensi/image/front.png".format(i))
    textures.append(texture)

# Create a new texture image with the combined textures
atlas = np.zeros((atlas_size, atlas_size, 3), dtype=np.uint8)
for i, texture in enumerate(textures):
    w, h, _ = texture.dimensions
    x = (i % 5) * (atlas_size // 5)
    y = (i // 5) * (atlas_size // 2)
    atlas[y:y+h, x:x+w, :] = texture.array

# Create a texture map for the combined texture image
texture_map = pv.Texture(atlas)

# Apply the texture map to the mesh
mesh.textures.append(texture_map)

# Display the mesh with the combined textures
p = pv.Plotter()
p.add_mesh(mesh, texture=True)
p.show()