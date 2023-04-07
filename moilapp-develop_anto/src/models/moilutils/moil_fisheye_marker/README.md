# moil_fisheye_marker
Python Module to draw the mark on image with moildev.

## Part1. Requirement
### Tested:
- Ubuntu > 20.04
- Python > 3.8
- opencv-python > 4.5.3.56
```commandline
$ pip install moildev
```

## Part2. Toturial

### Outline
- [2-1 Mark Point ( Fill / Non-Fill )](#2-1-mark-point--fill--non-fill-)
- [2-2. Mark Crosshair](#2-2-mark-crosshair)
- [2-3. Mark Cross](#2-3-mark-cross)
- [2-4. Mark Square](#2-4-mark-square)
- [2-5. Mark Triangle](#2-5-mark-triangle)
- [2-6. Mark Boundary ( Field Of View )](#2-6-mark-boundary--field-of-view-)
- [2-7. Draw Connecting Line Point to Point with Distorted](#2-7-draw-connecting-line-point-to-point-with-distorted)
- [2-8. Draw Vertical / Horizontal Line by point](#2-8-draw-vertical--horizontal-line-by-point)
----

### [2-1. Mark Point ( Fill / Non-Fill )](#outline)
```python
# point1 fill
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

p1 = (1257, 558)
color1 = (0, 255, 255) # Yellow
img_out = Marker.point(img.copy(), 
                       p1, 
                       color1, 
                       fill=True)

# point2 non-fill
p2 = (2635, 1999)
color2 = (255, 0, 0) # Blue
img_out = Marker.point(img_out, 
                       p2, 
                       color2, 
                       fill=False)

cv2.imwrite('output_2point.png', img_out)
```
![output_2point](./output_2point.png)
------

### [2-2. Mark Crosshair](#outline)
```python
# mark crosshair
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

crosshair_coord = (2000, 1200)
crosshair_color = (255, 0, 0)
img_out = Marker.crosshair(img.copy(), 
                           crosshair_coord, 
                           crosshair_color)

cv2.imwrite('output_crosshair.png', img_out)
```
![output_crosshair](./output_crosshair.png)
------

### [2-3. Mark Cross](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

# cross
cross_coord = (1500, 1500)
cross_color = (0, 255, 0)
img_out = Marker.cross(img.copy(), 
                       cross_coord, 
                       cross_color)

cv2.imwrite('output_cross.png', img_out)
```
![output_cross](./output_cross.png)
------

### [2-4. Mark Square](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

# square
square_coord = (1500, 1500)
square_color = (0, 0, 255)
img_out = Marker.square(img.copy(), 
                        square_coord, 
                        square_color)

cv2.imwrite('output_square.png', img_out)
```
![output_square](./output_square.png)
------

### [2-5. Mark Triangle](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

# triangle
triangle_coord = (2000, 1500)
triangle_color = (255, 0, 255)
img_out = Marker.triangle(img.copy(), 
                          triangle_coord, 
                          triangle_color)

cv2.imwrite('output_triangle.png', img_out)
```
![output_triangle](./output_triangle.png)
------

### [2-6. Mark Boundary ( Field Of View )](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

# input param
param_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_yuanman_andy.json'
moildev_narl = Moildev(param_path)

# mark boundary of fov 90d
img_out = Marker.boundary_fov(img.copy(), 
                              moildev_narl, 
                              fov=90)

cv2.imwrite('output_boundary_fov_90d.png', img_out)
```
![output_boundary_fov_90d](./output_boundary_fov_90d.png)
------

### [2-7. Draw Connecting Line Point to Point with Distorted](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)

# input param
param_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_yuanman_andy.json'
moildev_narl = Moildev(param_path)

point1 = (1257, 558)
point2 = (2635, 1999)

# draw a line in 3D to the image
img_out = Marker.line_p2p_distorted(img.copy(), 
                                    moildev_narl, 
                                    param_path, 
                                    point1, 
                                    point2)

cv2.imwrite('output_line_p2p_distorted.png', img_out)
```
![output_line_p2p_distorted](./output_line_p2p_distorted.png)

### [2-8. Draw Vertical / Horizontal Line by point](#outline)
```python
import cv2
from moil_fisheye_marker import MoilFisheyeMarker as Marker

# input img
img_path = './moil_fisheye_marker/input_narl_pyspin230_4000x3000_hall_mid.png'
img = cv2.imread(img_path)
point = (1200, 1500)
img_out = Marker.line_horizontal_vertical(img.copy(), point,
                                          color=(0, 0, 255),
                                          translucent=0.45)

img_out = cv2.resize(img_out, (800, 600))
cv2.imwrite('output_line_horizontal_vertical.png', img_out)
```
![output_line_p2p_distorted](./output_line_horizontal_vertical.png)