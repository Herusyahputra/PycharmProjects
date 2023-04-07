# raspberry_pi_camera

**raspberry pi camera settings**

## Part1. In camera_module:
- move raspberry_pi4_socket_server.py to Raspberrypi
- move raspberry_pi4_streaming_server.py to Raspberrypi
- move startup.py to Raspberrypi

## Part2. In Raspberrypi
- move raspberry_pi4_socket_server.py to /home/pi
- move raspberry_pi4_streaming_server.py to /home/pi
- move startup.py to /home/pi

## Part3. Open rc.local
```commandline
$ sudo nano /etc/rc.local
```

## Part4. Add Commit on exit 0 top
```commandline
$ sudo python3 /home/pi/startup.py
```
- ctrl+x save and close

## Part5. Reboot
```commandline
$ sudo roboot
```
## Part6. Test Socket Server

- make sure client and server in the same network
- create test.py 

```python
from moilcam import MoilCam

print(MoilCam.scan_id(cam_type = 'raspberry_pi4_ip_cam'))
```
**Output**
```python
['http://10.42.0.31:8000/stream.mjpg',
 'http://10.42.0.151:8000/stream.mjpg',
 'http://10.42.0.183:8000/stream.mjpg',...]
```