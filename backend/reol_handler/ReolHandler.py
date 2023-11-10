import os
import socketio
import json
from django.http import JsonResponse
from django.views import View

sio = socketio.Server(async_mode="eventlet", cors_allowed_origins="*")

@sio.event
def connect(sid, message):
    print("connect now...")

@sio.event
def modify_deployment_config(sid, message):
    print("I got the roots !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sio.emit("shutup", {"Content":"Je ne veux pas travailler"})
    
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