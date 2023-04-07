import yaml
import os


class ConfigFileApps(object):
    def __init__(self, main_ui):
        """Initializes a new instance of the class.

        Args:
            main_ui: The main user interface instance.

        Attributes:
            ui: The main user interface instance.
            __cached_file: The path to the configuration file.
            __cache_config: A dictionary containing the configuration data.

        Returns:
            None
        """
        self.ui = main_ui
        path_file = os.path.dirname(os.path.realpath(__file__))
        self.__cached_file = path_file + "/cached/cache_config.yaml"
        self.__cache_config = {}
        self.__init_config_file()

    def __init_config_file(self):
        """Initializes the configuration data and writes it to the cached file.

        This function creates the initial configuration data using default values or values
        from the UI double spin boxes. The configuration data includes paths to media files,
        parameter names, coordinates, and other settings for Modes 1 and 2, Pano tube, Pano car,
        and image saving. The zoom values for Modes 1 and 2, and the min/max alpha values for
        Pano tube are rounded to three decimal places. The configuration data is then written
        to the cached file using YAML format.

        Returns:
            None
        """
        if not os.path.exists(self.__cached_file):
            config = {
                "Media_path": None,
                "Parameter_name": None,
            }
            with open(self.__cached_file, "w") as outfile:
                yaml.dump(config, outfile, default_flow_style=False)