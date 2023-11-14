import os

# Const file's path
REPO_HANDLER_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.abspath(os.path.join(REPO_HANDLER_DIR, "../../"))
# Dir names
BACKEND = "backend"
FRONTEND = "frontend"

# Cache names
CACHE = "cache"

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
CACHE_DIR = os.path.join(BASE_DIR, CACHE)

# File path
SETTINGS_FILE = os.path.join(CFG_DIR, SETTINGS)
STATISTICS_FILE = os.path.join(CFG_DIR, STATISTICS)
REPO_CFG_FILE = os.path.join(CFG_DIR, REPO_CFG)
TEST_CFG_FILE = os.path.join(CFG_DIR, TEST_CFG)

# Cache dir
CFG_CACHE = os.path.join(CACHE_DIR, CFG)