import maya.cmds as cmds

from vulcain.python.logger import Logger

logger = Logger(name="Maya Shared Modules")

def init_new_scene():
    pass

def create_groups_from_dict(groups:dict):
    """
    Create groups based on dictionnary with the group name as value and the parent group name as key.
    Already existing groups will be skipped.
    
    Args :
        groups (dict) : Input dictionnary with group name as value and parent group name as key.
                        'root' is reserved to specifie that the group should not be parented.
    
    Returns:
        Nothing.
    """

    logger.info("Creating groups in scene. Skipping for existing groups.")
    logger.debug(f"'groups' value is : '{groups}'.")
    
    for group_name, parent_group_name in groups.items():
        logger.debug(f"group_name value is : '{group_name}' ; variable type is '{group_name}'.")
        logger.debug(f"parent_group_name value is :'{parent_group_name}' ; variable type is '{parent_group_name}'.")

        # Skipping process if the group already exists.
        if cmds.ls(group_name):
            logger.debug(f"goup_name : '{group_name}' already exist. Continue")
            continue

        # Checking if the parent groups exists.
        # If it doesn't exists we can't parent the base group to the parent.
        # 'root' is reserved name and is not a group to create.
        if not cmds.ls(parent_group_name) and parent_group_name != "root":
            logger.debug(f"Creating parent_group_name : '{parent_group_name}'")
            cmds.group(name=parent_group_name, empty=True, world=True)
        else:
            logger.debug(f"Parent group : '{parent_group_name}' already exists.")

        logger.debug(f"Creating empty group : '{group_name}'.")
        cmds.group(name=group_name, empty=True, world=True)

        if parent_group_name != "root":
            logger.debug(f"Parenting group : '{group_name}' under parent : '{parent_group_name}'.")
            cmds.parent(group_name, parent_group_name)
        else:
            logger.debug("Didn't parent group.")
        
        logger.debug(f"End of creating group : '{group_name}' with parent group : '{parent_group_name}'")
    
    logger.info("End of creating groups in scene.")


def load_plugin(plugin_name):
    plugin_loaded = cmds.pluginInfo(plugin_name, query=True, loaded=True)
    logger.debug(f"plugin_loaded value is : '{plugin_loaded}' ; variable type is : '{type(plugin_loaded)}'")
    if not plugin_loaded:
        logger.debug(f"Loading plugin '{plugin_name}'.")
        cmds.loadPlugin(plugin_name)
    else:
        logger.debug(f"Plugin '{plugin_name}' is already loaded.")