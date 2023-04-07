# raspberry_pi4_ip_cam

**raspberry pi camera settings**

## Part1. Requirement:
- Raspberry Pi4 OS > Raspbian GUN/linux 10
- Python > 3.7
- picamera > 1.13

```commandline
$ pip install picamera==1.13
```


## Part2. Setup Raspberry Pi4
### 2-1. Download Python File on Raspberry Pi4
#### Download and Save below file under: /home/[user]
1. raspberry_pi4_socket_server.py
2. raspberry_pi4_streaming_server.py
3. raspberry_pi4_startup.py
#### These python file could make raspberry pi4 be IP Cam.

### 2-2. Setup of auto startup python file

```commandline
$ sudo nano /etc/rc.local
```
```commandline
sudo python3 /home/pi/startup.py
```
- ctrl+x save and close
### 2-3. Reboot Raspberry Pi
```commandline
$ sudo roboot
```
## Part3. Test Socket Server

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