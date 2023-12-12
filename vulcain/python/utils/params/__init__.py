import os
import json

import vulcain.configs.vulcain as configs_path
import vulcain.python.utils.json as json_utils

VULCAIN_PARAMS_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(configs_path.__file__)), "params.json")
PROJECT_PARAMS_FILE_PATH = os.path.join(os.environ.get("VULCAIN_CONFIG_DIR_PATH"), "params.json")


def param(key):
    vulcain_params = load_vulcain_file_path()
    project_params = load_project_file_path()

    if key in project_params:
        return project_params.get(key)
    elif key in vulcain_params:
        return vulcain_params.get(key)
    else:
        raise ValueError(f"Param key : '{key}' does not exists.")


def load_vulcain_file_path():
    return json_utils.load_data(VULCAIN_PARAMS_FILE_PATH)


def load_project_file_path():
    if not PROJECT_PARAMS_FILE_PATH:
        return dict()
    return json_utils.load_data(PROJECT_PARAMS_FILE_PATH)

if __name__ == "__main__":
    print(VULCAIN_PARAMS_FILE_PATH)
    print(PROJECT_PARAMS_FILE_PATH)
    print(param('project.resolution.width'))
    print(param('project.resolution.height'))