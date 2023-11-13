import os

# Const file's path
REPO_HANDLER_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(REPO_HANDLER_DIR, "../../"))
# Dir names
BACKEND = "backend"
FRONTEND = "frontend"

REPO_HANDLER = "reol_handler"
CFG = "configs"

# File names
SETTINGS = "settings.json"
STATISTICS = "statistics.json"
REPO_CFG = "repos.json"
TEST_CFG = "test.json"

# Dir relationships
BACKEND_DIR = os.path.join(BASE_DIR, BACKEND)
FRONTEND_DIR = os.path.join(BASE_DIR, FRONTEND)
CFG_DIR = os.path.join(BASE_DIR, CFG)