import cv2
from Moildev import Moildev
from fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = 'input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)
# input param
param_path = 'input_narl_pyspin230_4000x3000_yuanman_andy.json'
moildev_narl = Moildev(param_path)


# point1 fill
point1 = (1257, 558)
color1 = (0, 255, 255)  # Yellow
img_out = Marker.point(img.copy(), point1, color=color1, fill=True)


# point2 non-fill
point2 = (2635, 1999)
color2 = (255, 0, 0)  # Blue
img_out = Marker.point(img_out, point2, color=color2, fill=False)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_2point.png', img_out)


# crosshair
crosshair_coord = (2000, 1200)
crosshair_color = (255, 0, 0)
img_out = Marker.crosshair(img.copy(), crosshair_coord, crosshair_color)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_crosshair.png', img_out)


# cross
cross_coord = (1500, 1500)
cross_color = (0, 255, 0)
img_out = Marker.cross(img.copy(), cross_coord, cross_color)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_cross.png', img_out)


# square
square_coord = (1500, 1500)
square_color = (0, 0, 255)
img_out = Marker.square(img.copy(), square_coord, square_color)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_square.png', img_out)


# triangle
triangle_coord = (2000, 1500)
triangle_color = (255, 0, 255)
img_out = Marker.triangle(img.copy(), triangle_coord, triangle_color)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_triangle.png', img_out)


# mark boundary of fov 90d
img_out = Marker.boundary_fov(img.copy(), moildev_narl, fov=90)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_boundary_fov_90d.png', img_out)

# draw line point to point distorted
img_out = Marker.line_p2p_distorted(img.copy(), moildev_narl, param_path, point1, point2)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_line_p2p_distorted.png', img_out)

# draw line horizontal vertical
point = (1200, 1500)
img_out = Marker.line_horizontal_vertical(img.copy(), point, color=(0, 0, 255), translucent=0.45)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_line_horizontal_vertical.png', img_out)