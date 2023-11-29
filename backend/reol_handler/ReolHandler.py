import os
import socketio
import json
import re
import threading
import schedule
import time
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from .ReolLogger import logger
from .RepoPool import RepoPool
from .ReolConsts import *
from .ReolTools import *
from .ReolOperations import *
from .ReolLark import *

sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*")
# RepoPool Instace
reol_ = None
        
'''
Implementation for Panel board
'''
@sio.event
def connect(sid, message):
    global reol_
    logger.debug("connect now...")
    logger.debug("Loading configurations...")
    logger.debug("Init RepoPool...")
    reol_ = init_reol(reol_)

@sio.event
def request_load_repo_cfg(sid):
    # judge if cfg exists
    global reol_
    logger.debug(f"Try to transfer {REPO_CFG_FILE}")
    sio.emit("request_load_repo_cfg_ret", json.dumps(reol_.repo_cfg, indent=4))
    
@sio.event
def request_settings(sid):
    global reol_
    logger.debug(f"HERE's the settings:{reol_.settings}")
    sio.emit("request_settings_ret", json.dumps(reol_.settings, indent=4))
    
@sio.event
def request_statistics(sid):
    global reol_
    logger.debug("received request statistics")
    sio.emit("request_statistics_ret", json.dumps(reol_.statistics, indent=4))

@sio.event
def request_store_repo_cfg(sid, message):
    # store previous cfg to cahce
    global reol_
    if reol_.repo_cfg is None:
        with open(REPO_CFG_FILE, 'r') as file:
            reol_.repo_cfg = json.load(file)
    with open(os.path.join(CFG_CACHE, f"{str(datetime.now())}.json"), 'w') as file:
        json.dump(reol_.repo_cfg, file, indent=4)
    reol_.repo_cfg = json.loads(message)
    with open(REPO_CFG_FILE, 'w') as file:
        json.dump(reol_.repo_cfg, file, indent=4)
    sio.emit("request_store_repo_cfg_ret", True)
    
# Add new repo
@sio.event
def add_repo(sid, message):
    logger.info(f"TRY TO ADD NEW REPO {message}")
    logger.debug(f"JSON data branch: {message['branch']}")
    sio.emit("add_repo_ret", {"ret": True})
    
# Update sync time
@sio.event
def request_update_sync_time(sid, message):
    logger.info(f"Receive request update sync time to: {message}")
    if re.compile(r'^(?:[01]\d|2[0-3]):[0-5]\d$').match(message):
        global reol_
        reol_.settings["sync_time"] = message
        update_json_cfg(reol_.settings, SETTINGS_FILE)
        sio.emit("request_update_sync_time_ret", update_json_cfg(reol_.settings, SETTINGS_FILE))
    else:
        sio.emit("request_update_sync_time_ret", False)

# Receive from: update_now
@sio.event
def update_now(sid):
    global reol_
    logger.info(f"Update now!!!")
    sio.emit("update_now_ret", try_sync(reol_))
        
# Receive from: leave a message
@sio.event
def leave_message(sid, message):
    logger.debug(f"Message content: {message}")
    send_notification(pray_sincerely(message))
    
'''
Implementation for Databoard
'''
# Receive from request_repos
@sio.event
def request_repos(sid):
    global reol_
    logger.info("Receive from request_repos")
    sio.emit("request_repos_ret", json.dumps(reol_.repo_cfg))
    
# Receive from requeust_branches
@sio.event
def request_branches(sid):
    global reol_
    logger.info("Receive from request_branches")
    branches = set()
    for repo in reol_.repos:
        logger.debug(f"Add {repo.branch}")
        branches.add(repo.branch)
    for git in reol_.gits:
        if git.branch is not None:
            logger.debug(f"Add {git.branch}")
            branches.add(git.branch)
        for git_repo in git.repos:
            logger.debug(f"Add {git_repo['branch']}")
            branches.add(git_repo["branch"])
    sio.emit("request_branches_ret", list(branches))