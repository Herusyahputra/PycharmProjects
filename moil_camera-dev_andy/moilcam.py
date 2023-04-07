import inspect
import sys
from typing import Tuple, List

from camera_module.abc_camera import AbstractMoilCamera
from camera_module.camera_opencv_usb_cam import CameraOpencvbUsbCam
from camera_module.camera_raspberry_pi4_ip_cam import CameraRaspberryPi4IpCam
from camera_module.camera_intel_t265 import CameraIntelT265


class MoilCam(object):
    def __new__(cls, cam_type: str, cam_id: int or str, resolution: Tuple[int, int] = None) -> AbstractMoilCamera:
        """

        :param cam_type: str
        :param cam_id: int or str
        :param resolution: Tuple[width: int, height: int]

        :return: AbstractMoilCamera
        """

        MoilCam.__raise_exception_invalid_cam_type(cam_type)

        if cam_type == 'opencv_usb_cam':
            return CameraOpencvbUsbCam(cam_id, resolution)

        if cam_type == 'raspberry_pi4_ip_cam':
            return CameraRaspberryPi4IpCam(cam_id, resolution)

        if cam_type == 'intel_t265':
            return CameraIntelT265(cam_id, resolution)

    @staticmethod
    def supported_cam_type():
        """ List all supported camera type

        :return: list
        """

        # Other camera type under developing
        supported_cam_type = [
            'opencv_usb_cam',
            'raspberry_pi4_ip_cam',
            'intel_t265'
        ]

        return supported_cam_type

    @staticmethod
    def valid_resolution(cam_type: str) -> list or dict:
        """
        Valid resolution info by cam_type

        :param cam_type: str
        :return: resolution: dict or warning_msg: str
        """

        if cam_type == 'opencv_usb_cam':
            usb_cam_resolution = {
                'twarm_usb210': [(3264, 2448),
                                 (2592, 1944),
                                 (2048, 1536),
                                 (1920, 1080),
                                 (1600, 1200),
                                 (1280, 720),
                                 (800, 600),
                                 (640, 480)],
                'endoscope_ometop': [(1920, 1080)],
                'endoscope_tioent': [(1920, 1080)],
            }
            return usb_cam_resolution

        if cam_type == 'raspberry_pi4_ip_cam':
            return 'The resolution of the Raspberry Pi camera must be set through the Raspberry Pi.'

        if cam_type == 'intel_t265':
            return 'Intel T265 cannot change the resolution.'

    @staticmethod
    def scan_id(cam_type: str):
        """
        Detect valid camera ID by cam_type

        :param cam_type: str
        :return: list
        """
        MoilCam.__raise_exception_invalid_cam_type(cam_type)

        list_uab_cam_type = MoilCam.supported_cam_type()

        for usb_cam_type_name in list_uab_cam_type:
            if usb_cam_type_name in cam_type.lower():
                if cam_type == 'opencv_usb_cam':
                    return CameraOpencvbUsbCam.scan()

                if cam_type == 'raspberry_pi4_ip_cam':
                    return CameraRaspberryPi4IpCam.scan()

                if cam_type == 'intel_t265':
                    return CameraIntelT265.scan()

    @staticmethod
    def __raise_exception_invalid_cam_type(cam_type):
        if cam_type not in MoilCam.supported_cam_type():
            exception_msg = f'Invalid cam_type "{cam_type}", ' \
                            f'please check valid cam_type with "MoilCam.supported_cam_type()"'
            raise Exception(exception_msg)


# from moilcam import MoilCam
#
#
# print(MoilCam.supported_cam_type())
#
# print(MoilCam.scan_id('intel_t265'))
#
# print(MoilCam.valid_resolution('intel_t265'))
#
# cam = MoilCam('intel_t265', 1, (2592, 1944))
#
# print(cam.get_resolution())
