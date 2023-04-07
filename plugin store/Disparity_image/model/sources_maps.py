import os
import sys

sys.path.append(os.path.dirname(__file__))


class SourceFile(object):
    def __init__(self):
        super().__init__()

    @classmethod
    def path_maps_x_image(cls, camera_tag):
        """
        This function is for get path maps x for front and back camera

        Args:
            camera_tag: type of camera (front or back)

        Returns:
            path of maps x
        """
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_image_2.npy"

    @classmethod
    def path_maps_y_image(cls, camera_tag):
        """
        This function is for get path of maps y for front and back camera

        Args:
            camera_tag:  type of camera (front or back)

        Returns:
            path of maps y
        """
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_image_2.npy"

    @classmethod
    def path_maps_x_panorama_rt(cls, camera_tag):
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_panoramam_Rt_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_panoramam_Rt_image_2.npy"

    @classmethod
    def path_maps_y_panorama_rt(cls, camera_tag):
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_panoramam_Rt_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_panoramam_Rt_image_2.npy"

    @classmethod
    def path_maps_x_rev_panorama(cls, camera_tag):
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_revPanorama_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_x_revPanorama_image_2.npy"

    @classmethod
    def path_maps_y_rev_panorama(cls, camera_tag):
        if camera_tag == 0:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_revPanorama_image_1.npy"
        else:
            return "controllers/plugins/Disparity_image/model/maps/maps_y_revPanorama_image_2.npy"
