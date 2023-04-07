import os
import signal
import socket
import sys
import threading
import time
import warnings
from typing import Tuple, List

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'timeout;1000'
import cv2
import numpy as np

sys.path.append(os.path.dirname(__file__))
from abc_camera import AbstractMoilCamera
from netifaces import interfaces, ifaddresses, AF_INET


class CameraRaspberryPi4IpCam(AbstractMoilCamera):
    __ip = []

    @classmethod
    def scan(cls) -> List[int] or List[str]:
        ip_list = []
        cls.__is_raspberry_by_broadcast_0_255()
        for ip in cls.__ip:
            url = f'http://{ip}:8000/stream.mjpg'
            cv2_cap = cv2.VideoCapture(url)
            if cv2_cap.isOpened():
                ip_list.append(url)
                cv2_cap.release()
            else:
                continue
        return ip_list

    @classmethod
    def __is_raspberry_by_broadcast_0_255(cls):
        local_subnet_ip = CameraRaspberryPi4IpCam.__get_local_subnet_ip()

        if local_subnet_ip:
            for local_ip in local_subnet_ip:
                network_segment = '.'.join(local_ip.split('.')[:-1])
                # ex: network_segment = 192.168.100
                ip = [f'{network_segment}.{i}' for i in range(0, 255)]

                threads = [threading.Thread(target=cls._is_raspberry_pi, args=(i,)) for i in ip]
                for i in threads:
                    i.start()
                    i.join()
        else:
            print('no found local ip')

    @classmethod
    def _is_raspberry_pi(cls, ip):
        host = ip
        port = 12345
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.01)
        try:
            s.connect((host, port))
            s.send('is_raspberrypi'.encode())
            indata = s.recv(1024)
            s.close()
            if indata.decode() == 'raspberrypi':
                cls.__ip.append(ip)
        except Exception:
            s.close()

    @staticmethod
    def __get_local_subnet_ip():
        all_ip = [i['addr'] for j in interfaces() for i in ifaddresses(j).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        local_ip = [i for i in all_ip if '127.0.' not in i]
        return local_ip

    def __init__(self, url: str, resolution: Tuple[int, int] = None):
        self.__cam_url = url
        self.__cap = None
        self.__is_open: bool = False
        self.open()
        if resolution:
            self.set_resolution(resolution)

    def open(self) -> bool:
        if self.__cam_url not in self.scan():
            exception_msg = f'Invalid camera ID: "{self.__cam_url}", please check valid camera ID with "Moilcam.scan_id()"'
            raise Exception(exception_msg)

        if not self.__is_open:
            self.__cap = cv2.VideoCapture(self.__cam_url)
            self.__is_open = True

        return self.__is_open

    def frame(self) -> np.ndarray:
        _, frame = self.__cap.read()
        return frame

    def close(self) -> bool:
        if self.__cap.isOpened():
            self.__cap.release()
            self.__is_open = False

        return self.__is_open

    def is_open(self) -> bool:
        if self.__cap.isOpened():
            self.__is_open = True
        else:
            self.__is_open = False

        return self.__is_open

    def get_resolution(self) -> Tuple[int, int]:

        h, w = self.frame().shape[:2]
        res = (w, h)

        return res

    def set_resolution(self, resolution: Tuple[int, int]):
        warning_msg = '\nThe resolution of the Raspberry Pi camera must be set through the Raspberry Pi.'
        warnings.warn(warning_msg)
        return None, None
