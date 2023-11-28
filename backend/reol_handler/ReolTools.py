import os
import json
from .ReolLogger import logger
from .ReolConsts import *

def init_json_cfg(json_obj, json_file):
    if not os.path.exists(json_file):
        logger.error(f"Shit, {json_file} doesn't eventn exist")
    else:
        with open(json_file, 'r') as file:
            json_obj = json.load(file)
    return json_obj

def update_json_cfg(json_obj, json_file):
    if json_obj is None:
        logger.error(f"Why would you try to export an empty obj to your file :) ?")
        return False
    if os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump(json_obj, file, indent=4)
        return True
    return False

def is_cmd_legal(cmd):
    # check if the command starts with '/'
    if cmd.startswith('/'):
        return False

    # check if the command contains '..' to prevent accessing parent directory
    if '..' in cmd:
        return False

    # check if the command contains dangerous operations
    dangerous_operations = ['rm', 'delete', 'format', 'destroy']
    for operation in dangerous_operations:
        if operation in cmd:
            return False

    return True