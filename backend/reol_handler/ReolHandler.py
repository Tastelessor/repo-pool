import os
import socketio
import eventlet
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