import os
import subprocess
import json
import argparse
import schedule
import time
from datetime import datetime
from collections import namedtuple


# Define named-tuple structures
Repo = namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
Git = namedtuple("Git", ["name", "branch", "repos"])

class RepoPool:
    def __init__(self, workspace, cfg_file="repos.json"):
        self.workspace=os.path.join(workspace)
        self.log_file=str(os.path.join(workspace, "log.txt"))
        self.cfg = None
        self.repos = []
        self.gits = []
        self.dir_counts = 0
        
        os.chdir(workspace)
        self.init_cfg(cfg_file)
        
    def init_dirs(self):
        """Init dirs for repos and git repositories
        """
        for item in (self.repos + self.gits):
            print(f"Creating dir for {item.name}...")
            if not os.path.exists(item.name):
                os.mkdir(item.name)
            else:
                print(f"{item.name} already exists")
                
                
    def init_cfg(self, cfg_file):
        """Init repos & gits from the input cfg file

        Args:
            cfg_file (str): configuration file path

        Raises:
            ValueError: The attribute [repos] of the configuration file is empty
        """
        os.system(f"echo 'Hello, world!' > {self.log_file}")
        with open (cfg_file, 'r') as f:
            self.cfg = json.load(f)
        for key, value in self.cfg.items():
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
        os.system(f"git clone {git.get('url')} >> {self.log_file}")
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
    
    def sync_all(self):
        """Create dirs, update gits and repos
        """
        print(f"Synchronisation Start!")
        self.init_dirs()
        self.init_all_repos()
        self.init_all_gits()
    
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
    parser.add_argument('-t', '--time',         default="2:00", help='Time to run this program, format (HH:MM)')

    args = parser.parse_args()
    
    # Init basic configs
    config_file_path = args.config
    if config_file_path == "repos.json":
        config_file_path = os.path.join(args.workspace, config_file_path)
    repo_pool = RepoPool(workspace=args.workspace, cfg_file=config_file_path)
    
    if args.AtOnce:
        repo_pool.sync_all()
    if args.all:
        print(f"All repos configured in [{config_file_path}] will be run every single day at {args.time}")
        schedule.every().day.at(args.time, "Asia/Shanghai").do(repo_pool.sync_all)
        while 1:
            schedule.run_pending()
            time.sleep(60)