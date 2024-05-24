import maya.cmds as cmds

from vulcain.logger import Logger

logger = Logger("Maya Plugin Loader.")


def load_plugin(plugin_name):
    plugin_loaded = cmds.pluginInfo(plugin_name, query=True, loaded=True)
    logger.debug(f"plugin_loaded value is : '{plugin_loaded}' ; variable type is : '{type(plugin_loaded)}'")
    if not plugin_loaded:
        logger.debug(f"Loading plugin '{plugin_name}'.")
        cmds.loadPlugin(plugin_name)
    else:
        logger.debug(f"Plugin '{plugin_name}' is already loaded.")