import os


class FileMaps(object):
    def __init__(self):
        self.__realpath = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
        self.folder_config = "cached"

    def change_folder_config(self, folder_config):
        self.folder_config = folder_config

    def get_maps_x_dash_front_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_dash_front_view.npy'

    def get_maps_y_dash_front_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_dash_front_view.npy'

    def get_maps_x_dash_driver_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_dash_driver_view.npy'

    def get_maps_y_dash_driver_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_dash_driver_view.npy'

    def get_maps_x_left_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_left_window_view.npy'

    def get_maps_y_left_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_left_window_view.npy'

    def get_maps_x_right_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_right_window_view.npy'

    def get_maps_y_right_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_right_window_view.npy'

    def get_maps_x_second_driver_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_second_driver_window_view.npy'

    def get_maps_y_second_driver_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_second_driver_window_view.npy'

    def get_maps_x_compare_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_compare_view.npy'

    def get_maps_y_compare_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_compare_view.npy'

    def get_maps_x_driver_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_image_driver_window_view.npy'

    def get_maps_y_driver_window_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_image_driver_window_view.npy'

    # birds view
    def get_maps_x_anypoint_image_1_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_anypoint_image_1_bird_view.npy'

    def get_maps_y_anypoint_image_1_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_anypoint_image_1_bird_view.npy'

    def get_maps_x_anypoint_image_2_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_anypoint_image_2_bird_view.npy'

    def get_maps_y_anypoint_image_2_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_anypoint_image_2_bird_view.npy'

    def get_maps_x_anypoint_image_3_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_anypoint_image_3_bird_view.npy'

    def get_maps_y_anypoint_image_3_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_anypoint_image_3_bird_view.npy'

    def get_maps_x_anypoint_image_4_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_x_anypoint_image_4_bird_view.npy'

    def get_maps_y_anypoint_image_4_bird_view(self):
        return self.__realpath + f'/{self.folder_config}/map_y_anypoint_image_4_bird_view.npy'