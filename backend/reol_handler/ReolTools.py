import os
import json
from .ReolConsts import *

def update_json_cfg(json_obj, json_file):
    if json_obj is None:
        print(f"Why would you try to export an empty obj to your file :) ?")
        return False
    if os.path.exists(json_file):
        with open(json_file, 'w') as file:
            json.dump(json_obj, file, indent=4)
        return True
    return False