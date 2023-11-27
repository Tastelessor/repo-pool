import os
import subprocess
import json
import argparse
import schedule
import time
from datetime import datetime
import shutil
from collections import namedtuple
from collections import defaultdict
from .ReolConsts import *
from .ReolTools import *
from .ReolLark import send_notification

# Define named-tuple structures
Repo = namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
Git = namedtuple("Git", ["name", "branch", "repos"])

class RepoPool:
    def __init__(self, workspace, cfg_file=REPO_CFG_FILE):
        self.workspace=os.path.join(workspace)
        self.log_file=str(os.path.join(workspace, "log.txt"))
        self.repos = []
        self.gits = []
        self.cfg_file = cfg_file
        self.repo_cfg = None
        self.settings = None
        self.statistics = None
        self.init_cfg()
        os.chdir(workspace)
        
    def init_dirs(self):
        """Init dirs for repos and git repositories
        """
        for item in (self.repos + self.gits):
            print(f"Creating dir for {item.name}...")
            if not os.path.exists(item.name):
                os.mkdir(item.name)
            else:
                print(f"{item.name} already exists")
                
    def init_cfg(self):
        """Init repos & gits from the input cfg file

        Args:
            cfg_file (str): configuration file path

        Raises:
            ValueError: The attribute [repos] of the configuration file is empty
        """
        # Init settings & statistics
        self.repo_cfg = init_json_cfg(self.repo_cfg, self.cfg_file)
        self.statistics = init_json_cfg(self.statistics, STATISTICS_FILE)
        self.settings = init_json_cfg(self.settings, SETTINGS_FILE)
        self.update_statistics()
        
        # Beautiful prints
        os.system(f"echo '### Synchronisation NO.{self.statistics['synchronisation_times']} Starts o(*￣▽￣*)ブ ###' > {self.log_file}")
        self.start_time = datetime.now()
        os.system(f"echo '### Synchronised at {self.start_time} ###' >> {self.log_file}")
        
        # Clear stored lists
        self.repos = [] 
        self.gits = []
        for _, value in self.repo_cfg.items():
            if value["type"] == "repo":
                self.repos.append(Repo(name=value["name"],
                                  type=value["type"],
                                  branch=value["branch"],
                                  manifest=value["manifest"],
                                  url=value["url"]))
            elif value["type"] == "git":
                if len(value["repos"]) < 1:
                    raise ValueError(f"Invalid git repos for {value['name']}")
                else:
                    # outer branch is the default branch
                    repos = []
                    default_branch = value.get("branch") if value.get("branch") is not None else "develop"
                    for item in value["repos"]:
                        # extract the git repo's name
                        url = item["url"]
                        name = url[url.rfind('/') + 1 : url.rfind(".git")]
                        
                        branch = item.get("branch") if item.get("branch") is not None else default_branch
                        repos.append({"name": name,
                                      "branch": branch,
                                      "url": item["url"]})
                            
                    self.gits.append(Git(name=value["name"],
                                         branch=default_branch,
                                         repos=repos))
                    
    def scan_workspace(self):
        self.previous_repos = []
        self.previous_gits = defaultdict(list)
        for root, dirs, _ in os.walk(self.workspace):
            base_root = os.path.basename(root)
            if '/.repo' in root or '/.git' in root:
                continue
            elif '.repo' in dirs:
                self.previous_repos.append(base_root)
            elif '.git' in dirs and not os.path.islink(os.path.join(root, '.git')):
                self.previous_gits[os.path.basename(os.path.dirname(root))].append(base_root)
    
    def remove_previous_repos(self):
        self.scan_workspace()
        # remove unmatched repos
        for p_repo in self.previous_repos:
            delete_repo_dir = True
            for repo in self.repos:
                print(f"* comparing {p_repo} with {repo.name}")
                if p_repo == repo.name:
                    delete_repo_dir = False
            if delete_repo_dir:        
                shutil.rmtree(os.path.join(self.workspace, p_repo))
        
        # remove unmatched gits
        if self.previous_gits != self.gits:
            print("gits list unmatch, start cleaning")
            for p_git in self.previous_gits.keys():
                delete_git_dir = True
                for git in self.gits:
                    print(f"* comparing {p_git} and {git.name}")
                    if p_git == git.name:
                        delete_git_dir = False
                        for p_git_repo in self.previous_gits[p_git]:
                            delete_git = True
                            for git_repo in git.repos:
                                print(f"** comparing {p_git_repo} and {git_repo['name']}")
                                # if two git repos share the same url, the previous would not be deleted
                                if p_git_repo == git_repo["name"]:
                                    delete_git = False
                            if delete_git:
                                print(f"unmatched! delete {p_git_repo}")
                                shutil.rmtree(os.path.join(self.workspace, p_git, p_git_repo))
                if delete_git_dir:
                    shutil.rmtree(os.path.join(self.workspace, p_git))
            
    def init_all_repos(self):
        """Init or sync all repo projects
        """
        for item in self.repos:
            os.chdir(self.workspace)
            try:
                os.chdir(item.name)
                subprocess.run(["repo", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
                print(f"{item.name} {item.branch} {item.manifest} exists, start synchronising...")
                self.update_repo(item)
            except Exception:
                print(f"{item.name} {item.branch} {item.manifest} does not exist, start initialising...")
                self.init_repo(item)

    def init_repo(self, repo):
        """Init a repo

        Args:
            repo (named_tuple): Repo = namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
        """
        repo_config_path = os.path.join(self.workspace, repo.name, ".repo")
        if os.path.exists(repo_config_path):
            os.chdir(self.workspace)
            shutil.rmtree(os.path.dirname(repo_config_path))
            os.mkdir(repo.name)
            os.chdir(repo.name)
        os.system(f"repo init -u {repo.url} -b {repo.branch} -m {repo.manifest} >> {self.log_file}")
        self.update_repo(repo)
    
    def update_repo(self, repo):
        """Sync a repo

        Args:
            repo (named_tuple): Repo = namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
        """
        os.system(f"repo sync -j 32 >> {self.log_file}")
        
        
    def init_all_gits(self):
        """Init or update all git repositories
        """
        for item in self.gits:
            os.chdir(self.workspace)
            os.chdir(item.name)
            for git_repo in item.repos:
                if os.path.exists(git_repo["name"]):
                    print(f"Updating {git_repo.get('name')} {git_repo.get('branch')}... Please kill me if you don't wanna wait")
                    self.update_git(git_repo)
                else:
                    print(f"Initialising {git_repo.get('name')} {git_repo.get('branch')}... Please kill me if you don't wanna wait")
                    self.init_git(git_repo)
            print(f"{item.name} update to date")
                
    def init_git(self, git):
        """Init a git repository
        Args:
            git (named_tuple): Git = namedtuple("Git", ["name", "branch", "repos"])
        """
        os.system(f"git clone --depth=5 {git.get('url')} >> {self.log_file}")
        os.chdir(git["name"])
        os.system(f"git checkout {git.get('branch')} >> {self.log_file}")
        os.chdir("../")
        
    def update_git(self, git):
        """Update a git repository

        Args:
            git (named_tuple): Git = namedtuple("Git", ["name", "branch", "repos"])
        """
        os.chdir(git["name"])
        os.system(f"git pull -f >> {self.log_file}")
        os.system(f"git checkout {git.get('branch')} >> {self.log_file}")
        os.chdir("../")

    
    def get_repo_by_name(self, repo_name):
        """return a repo by repo name (defined in the cfg json)

        Args:
            repo_name (str): repo's name

        Returns:
            named_tuple: namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
        """
        for item in self.repos:
            if item.name == repo_name:
                return self.repos
    
    def get_gits_by_name(self, git_name):
        """return a git obj by git repo's name (defined in the cfg json)

        Args:
            git_name (named_tuple): git repository's name

        Returns:
            named_tuple: Git = namedtuple("Git", ["name", "branch", "repos"])
        """
        for item in self.gits:
            for git_repo in item.repos:
                if git_repo.get("name") == git_name:
                    return git_repo

    def remove_empty_dirs(self):
        """remove empty dirs under workspace
        """
        with os.scandir(self.workspace) as entries:
            for entry in entries:
                if entry.is_dir():
                    if not any(True for _ in os.scandir(entry.path)):
                        print(f"Removed empty directory: {entry.path}")
                        os.rmdir(entry.path)
        
        self.update_statistics()
        
    def update_indices(self):
        """update indices via invoking an existing sh script
        """
        os.system("rm /data/layne/tools/opengrok-1.7.32/src/*")
        os.system("ln -s /data/layne/src/* /data/layne/tools/opengrok-1.7.32/src/")
        os.system(f"sh /data/layne/tools/index_restart.sh >> {self.log_file}")
        
    def update_statistics(self):
        print(f"Workspace: {self.workspace}, here's the result of os.listdir")
        print(os.listdir(self.workspace))
        self.settings["dirs"] = list(filter(lambda dir: os.path.isdir(os.path.join(self.workspace, dir)), os.listdir(self.workspace)))
        update_json_cfg(self.settings, SETTINGS_FILE)
        
        self.statistics["dir_count"] = len(self.settings["dirs"])
        print("HERE ARE THE DIRS:")
        print(list(filter(lambda dir: os.path.isdir(dir), os.listdir(self.workspace))))
        gits_count = 0
        for git in self.gits:
            gits_count += len(git.repos)
        self.statistics["git_project_num"] = gits_count
        self.statistics["repo_project_num"] = len(self.repos)
        update_json_cfg(self.statistics, STATISTICS_FILE)
        
    def calculate_time(self):
        timecost = (datetime.now() - self.start_time).total_seconds()/60
        print(f"Total timecost: {timecost} mins")
        self.statistics["last_update_timecost"] = round(timecost, 3)
        self.statistics["average_update_timecost"] = round((self.statistics["average_update_timecost"] * self.statistics["synchronisation_times"] + timecost)/(self.statistics["synchronisation_times"] + 1), 3)
        self.statistics["synchronisation_times"] += 1
        update_json_cfg(self.statistics, STATISTICS_FILE)
        
    def sync_all(self):
        """synchronise the workspace according to the cfg json file
        """
        print(f"Synchronisation Start!")
        os.chdir(self.workspace)
        self.init_cfg()
        # delete abandonned dirs
        self.remove_previous_repos()
        # init repositories
        self.init_dirs()
        self.init_all_repos()
        self.init_all_gits()
        # remove empty dirs & update indices
        self.remove_empty_dirs()
        self.update_indices()
        self.calculate_time()
        if send_notification(repos_num=(self.statistics["repo_project_num"] + self.statistics["git_project_num"]),
                          sync_time=self.settings["sync_time"],
                          time_cost=self.statistics["last_update_timecost"]):
            print("Synchronisation Success!")
        else:
            print("Failed to send lark notification")
        
    def twilight_of_the_gods(self):
        pass
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argument Parser Example")

    parser.add_argument('-w', '--workspace',    help='All operation', required=True)
    parser.add_argument('-c', '--config',       default="repos.json", help='All operation')
    parser.add_argument('-d', '--delete',       help='Delete certain repository')
    parser.add_argument('-u', '--update',       action='store_true', help='Update operation')
    parser.add_argument('-a', '--all',          action='store_true', help='Update all repos')
    parser.add_argument('-A', '--AtOnce',       action='store_true', help='Update all repos now')
    parser.add_argument('-t', '--time',         default="02:00", help='Time to run this program, format (HH:MM)')

    args = parser.parse_args()
    
    # Init basic configs
    config_file_path = args.config
    if config_file_path == "repos.json":
        config_file_path = os.path.join(args.workspace, config_file_path)
    if not os.path.exists(config_file_path):
        raise LookupError(f"I'm sorry but {config_file_path} doesn't appear to be a valid path :(")
    repo_pool = RepoPool(workspace=args.workspace, cfg_file=config_file_path)
    
    if args.AtOnce:
        repo_pool.sync_all()
    if args.all:
        print(f"All repos configured in [{config_file_path}] will be run every single day at {args.time}")
        schedule.every().day.at(args.time, "Asia/Shanghai").do(repo_pool.sync_all)
        # schedule.every(1).minutes.do(repo_pool.sync_all)
        while 1:
            schedule.run_pending()
            time.sleep(60)