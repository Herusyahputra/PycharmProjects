"""
Class to control manipulate image
"""


class ControlResultImage:

    @staticmethod
    def zoom_in(current_size):
        """
        Zoom in image on result label

        """
        if current_size > 6000:
            pass
        else:
            current_size += 100
        return current_size

    @staticmethod
    def zoom_out(current_size):
        """
        Zoom out image on result label

        """
        if current_size < 800:
            pass
        else:
            current_size -= 100
        return current_size

    @staticmethod
    def rotate_left(current_angle):
        """
        Rotate image in anti clockwise.

        """
        if current_angle == 180:
            pass
        else:
            current_angle += 10
        return current_angle

    @staticmethod
    def rotate_right(current_angle):
        """
        Rotate image in clockwise.

        """
        if current_angle == -180:
            pass
        else:
            current_angle -= 10
        return current_angle

