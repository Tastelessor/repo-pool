import os
import socketio
import json
import re
import threading
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .RepoPool import RepoPool
from .ReolConsts import *
from .ReolTools import *

sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*")
# RepoPool Instace
reol_ = None
# repo cfg
repo_cfg_ = None
settings_cfg_ = None
statistics_ = None

def init_reol():
    global settings_cfg_
    global reol_
    if reol_ == None:
        reol_ = RepoPool(workspace=settings_cfg_["workspace"], cfg_file=settings_cfg_["repo_cfg_path"])

def init_cfgs():
    global repo_cfg_
    global settings_cfg_
    global statistics_
    with open(REPO_CFG_FILE, 'r') as file:
        repo_cfg_ = json.loads(file.read())
    with open(SETTINGS_FILE, 'r') as file:
        settings_cfg_ = json.loads(file.read())
    with open(STATISTICS_FILE, 'r') as file:
        statistics_ = json.loads(file.read())
        
'''
Implementation for Panel board
'''
@sio.event
def connect(sid, message):
    print("connect now...")
    print("Loading configurations...")
    init_cfgs()
    print("Init RepoPool...")
    init_reol()

@sio.event
def request_load_repo_cfg(sid):
    # judge if cfg exists
    global repo_cfg_
    print(f"Try to transfer {REPO_CFG_FILE}")
    if os.path.exists(REPO_CFG_FILE):
        with open(REPO_CFG_FILE, 'r') as file:
            repo_cfg_ = json.loads(file.read())
    sio.emit("request_load_repo_cfg_ret", json.dumps(repo_cfg_, indent=4))

@sio.event
def request_store_repo_cfg(sid, message):
    # store previous cfg to cahce
    global repo_cfg_
    if repo_cfg_ is None:
        with open(REPO_CFG_FILE, 'r') as file:
            repo_cfg_ = json.loads(file.read())
    with open(os.path.join(CFG_CACHE, f"{str(datetime.now())}.json"), 'w') as file:
        json.dump(repo_cfg_, file, indent=4)
    repo_cfg_ = json.loads(message)
    with open(REPO_CFG_FILE, 'w') as file:
        json.dump(repo_cfg_, file, indent=4)
    sio.emit("request_store_repo_cfg_ret", True)
    
# Add new repo
@sio.event
def add_repo(sid, message):
    print(f"TRY TO ADD NEW REPO {message}")
    print(f"JSON data branch: {message['branch']}")
    sio.emit("add_repo_ret", {"ret": True})
    
# Update sync time
@sio.event
def request_update_sync_time(sid, message):
    print(f"Receive request update sync time to: {message}")
    if re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$').match(message):
        global settings_cfg_
        settings_cfg_["sync_time"] = message
        sio.emit("request_update_sync_time_ret", update_json_cfg(settings_cfg_, SETTINGS_FILE))
    else:
        sio.emit("request_update_sync_time_ret", False)

# Update now
update_lock = threading.Lock()
@sio.event
def update_now(sid):
    global reol_
    global statistics_
    print(f"Update now!!!")
    if update_lock.acquire(timeout=1):
        try:
            sio.emit("update_now_ret", True)
            start_time = datetime.now()
            def sync_all():
                reol_.sync_all()
                # update statistics of sync time
                timecost = (datetime.now() - start_time).total_seconds()/60
                print(f"Total timecost: {timecost} mins")
                statistics_["last_update_timecost"] = timecost
                statistics_["average_update_timecost"] = (statistics_["average_update_timecost"] * \
                    statistics_["synchronisation_times"] + timecost)/statistics_["synchronisation_times"] + 1
                statistics_["average_update_timecost"] += 1
                update_lock.release()
            update_thread = threading.Thread(target=reol_.sync_all)
            update_thread.start()
        finally:
            pass
    else:
        sio.emit("update_now_ret", False)
# Receive from: leave a message
@sio.event
def leave_message(sid, message):
    print(f"Message content: {message}")
    
'''
Implementation for Data board
'''
@sio.event
def request_statistics(sid):
    global statistics_
    print("received request statistics")
    sio.emit("request_statistics_ret", json.dumps(statistics_, indent=4))