import pyvista as pv

mesh = pv.read('design/new-bowl.obj')
mesh.plot()
mesh.plot(background='white', camera_position='xy', lighting='none')
