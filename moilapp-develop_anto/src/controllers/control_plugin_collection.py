import inspect
import os
import pkgutil
import sys
sys.path.append("..")
from src.plugin_interface import PluginInterface


class PluginCollection(object):
    def __init__(self, plugin_package):
        """
        Upon creation, this class will read the plugins package for modules that contains
        a class definition that is inheriting from the Plugin class.

        Args:
            plugin_package (): The folder name of plugins directory. example is "plugins"
        """
        self.plugins = None
        self.name_application = None
        self.seen_paths = None
        self.path_folder = None
        self.plugin_package = plugin_package
        self.reload_plugins()

    def reload_plugins(self):
        """
        Reset the list of all plugins and initiate the walk over the main provided
        plugins package to load all available plugins.

        Returns:
            None
        """
        self.plugins = []
        self.name_application = []
        self.seen_paths = []
        self.path_folder = []
        self.walk_package(self.plugin_package)

    def get_widget(self, index, model):
        """
        Apply all the plugins on the argument supplied to this function.

        Args:
            model:
            index (): The index number from the list plugins available

        Returns:
            None
        """
        plugin = self.plugins[index]
        return plugin.set_plugin_widget(model)

    def get_icon_(self, index):
        path_file = os.path.dirname(os.path.realpath(__file__))
        icon_source = self.plugins[index].set_icon_apps()
        if icon_source is not None:
            if icon_source[0] == ".":
                icon_source.replace("./", "")
            elif icon_source[0] == "/":
                icon_source.replace("/", "")

            folder = self.path_folder[index]
            path = folder.split(".")[1]
            path = path_file + '/plugins/' + path + "/" + icon_source
        else:
            path = None
        return path

    def change_theme(self, index):
        if len(self.plugins) > 0:
            self.plugins[index].change_stylesheet()

    def get_description(self, index):
        return self.plugins[index].description

    def walk_package(self, package):
        """
        Recursively walk the supplied package to retrieve all plugins.

        Args:
            package (): The name folder e define. i.e "plugins"

        Returns:
            Create list plugins that find from plugins directory.
        """
        path_file = os.path.dirname(os.path.realpath(__file__))
        sys.path.insert(0, path_file)
        imported_package = __import__(package, fromlist=['blah'])

        for _, plugin_name, is_pkg in pkgutil.iter_modules(
                imported_package.__path__, imported_package.__name__ + '.'):
            if not is_pkg:
                try:
                    plugin_module = __import__(plugin_name, fromlist=['blah'])
                    cls_members = inspect.getmembers(plugin_module, inspect.isclass)
                    for (_, c) in cls_members:
                        # only add classes that are a subclass of plugins, but not
                        # plugins itself
                        if issubclass(c, PluginInterface) & (c is not PluginInterface):
                            # print(f'Found Plugin class: {c.__name__}')
                            self.path_folder.append(c.__module__)
                            self.name_application.append(c.__name__)
                            self.plugins.append(c())
                except ImportError as err:
                    print("Your will get problem because: " + str(err))

        # Now that we have looked at all the modules in the current package, start looking
        # recursively for additional modules in sub packages
        all_current_paths = []
        if isinstance(imported_package.__path__, str):
            all_current_paths.append(imported_package.__path__)
        else:
            all_current_paths.extend([x for x in imported_package.__path__])

        for pkg_path in all_current_paths:
            if pkg_path not in self.seen_paths:
                self.seen_paths.append(pkg_path)

                # get subdirectory of current package path directory
                child_pkgs = [
                    p for p in os.listdir(pkg_path) if os.path.isdir(
                        os.path.join(
                            pkg_path, p))]
                # For each subdirectory, apply the walk_package method
                # recursively
                for child_pkg in child_pkgs:
                    self.walk_package(package + '.' + child_pkg)
