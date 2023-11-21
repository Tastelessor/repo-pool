import threading
import json
import time
import pytz
from datetime import datetime
from .RepoPool import RepoPool
from .ReolTools import *
from .ReolConsts import *

def init_reol(rp: RepoPool):
    if rp == None:
        print("Create RepoPool")
        settings = None
        with open(SETTINGS_FILE, 'r') as file:
            settings = json.load(file)
        rp = RepoPool(workspace=settings["workspace"], cfg_file=settings["repo_cfg_path"])
        start_task_schedule(rp)
    else:
        print("RepoPool already exists")
    return rp

update_lock = threading.Lock()
def try_sync(rp: RepoPool):
    print(f"Update now!!!")
    global update_lock
    if update_lock.acquire(timeout=1):
        try:
            def sync_all():
                rp.sync_all()
                update_lock.release()
            update_thread = threading.Thread(target=sync_all)
            update_thread.start()
            return True
        finally:
            pass
    return False
    
def start_task_schedule(rp: RepoPool):
    print("Start task scheduling")
    def wait_for_schedule():
        while(True):
            current_time = datetime.now(pytz.timezone('Asia/Shanghai'))
            target_time = rp.settings["sync_time"]
            if current_time.hour == int(target_time[0:2]) and current_time.minute == int(target_time[3:5]):
                try_sync(rp)
            time.sleep(60)
    schedule_task = threading.Thread(target=wait_for_schedule)
    schedule_task.start()