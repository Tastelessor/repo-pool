import subprocess
import os

if __name__ == "__main__":
    backend_cmd = ("python backend/manage.py runserver")
    frontend_cmd = "cd frontend && npm run dev -- --host"
    subprocess.Popen(
        frontend_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    os.system(backend_cmd)