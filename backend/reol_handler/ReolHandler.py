import os
import socketio
import json
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .ReolConsts import *

sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*")
repo_cfg_file = None

@sio.event
def connect(sid, message):
    print("connect now...")

@sio.event
def request_load_repo_cfg(sid):
    # judge if cfg exists
    global repo_cfg_file
    print(f"Try to transfer {REPO_CFG_FILE}")
    if os.path.exists(REPO_CFG_FILE):
        with open(REPO_CFG_FILE, 'r') as file:
            repo_cfg_file = json.loads(file.read())
    sio.emit("request_load_repo_cfg_ret", json.dumps(repo_cfg_file, indent=4))

@sio.event
def request_store_repo_cfg(sid, message):
    # store previous cfg to cahce
    global repo_cfg_file
    if repo_cfg_file is None:
        with open(REPO_CFG_FILE, 'r') as file:
            repo_cfg_file = json.loads(file.read())
    with open(os.path.join(CFG_CACHE, f"{str(datetime.now())}.json"), 'w') as file:
        json.dump(repo_cfg_file, file, indent=4)
    repo_cfg_file = json.loads(message)
    with open(REPO_CFG_FILE, 'w') as file:
        json.dump(repo_cfg_file, file, indent=4)
    sio.emit("request_store_repo_cfg_ret", True)
    
# Add new repo
@sio.event
def add_repo(sid, message):
    print(f"TRY TO ADD NEW REPO {message}")
    print(f"JSON data branch: {message['branch']}")
    sio.emit("add_repo_ret", {"ret": True})

# Update now
@sio.event
def update_now(sid):
    print(f"Update now!!!")
    sio.emit("update_now_ret", True)
    
# Receive from: leave a message
@sio.event
def leave_message(sid, message):
    print(f"Message content: {message}")