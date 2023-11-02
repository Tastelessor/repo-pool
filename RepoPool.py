import os
import subprocess
import json
import argparse
import schedule
import time
import datetime
import shutil
from collections import namedtuple


# Define named-tuple structures
Repo = namedtuple("Repo", ["name", "type", "branch", "manifest", "url"])
Git = namedtuple("Git", ["name", "branch", "repos"])

class RepoPool:
    def __init__(self, workspace, cfg_file="repos.json"):
        self.workspace=os.path.join(workspace)
        self.log_file=str(os.path.join(workspace, "log.txt"))
        self.repos = []
        self.gits = []
        self.dir_counts = 0
        self.synchronisation_times = 1
        self.cfg_file = cfg_file
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
                
                
    def init_cfg(self, cfg_file):
        """Init repos & gits from the input cfg file

        Args:
            cfg_file (str): configuration file path

        Raises:
            ValueError: The attribute [repos] of the configuration file is empty
        """
        previous_repos = self.repos    
        self.repos = [] 
        self.gits = []
        os.system(f"echo '### Synchronisation NO.{self.synchronisation_times} Starts o(*￣▽￣*)ブ ###' > {self.log_file}")
        os.system(f"echo '### Synchronised at {datetime.datetime.now()} ###' >> {self.log_file}")
        with open (cfg_file, 'r') as f:
            self.cfg = json.load(f)
        for _, value in self.cfg.items():
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
        # remove unmatched repos
        if previous_repos != self.repos:
            for repo in previous_repos:
                if repo not in self.repos:
                    shutil.rmtree(os.path.join(self.workspace, repo.name))
    
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
    
    def get_all_gits_name(self):
        """get the nmes of all git projects, and the common dirs where they are placed from the config file

        Returns:
            list[str]: dirs name
        """
        gits_name = []
        git_dirs_name = []
        for item in self.gits:
            git_dirs_name.append(item.name)
            for git_repo in item.repos:
                gits_name.append(git_repo.get("name"))
        return gits_name, git_dirs_name
    
    def get_all_repos_name(self):
        """get the names of all repo projects from the config file

        Returns:
            list[str]: names of all repo projects
        """
        repos_name = []
        for item in self.repos:
            repos_name.append(item.name)
        return repos_name
    
    def list_dirs(self, path, depth=2):
        """get all dirs of a specific path and depth

        Args:
            path (str): dir path where the search begins
            depth (int, optional): the depth to do the search. Defaults to 2.

        Returns:
            list[str]: all dirs in the searched location
        """
        if depth < 1:
            return []
        dirs = []
        try:
            with os.scandir(path) as entries:
                if depth == 1:
                    dirs = [str(entry.path) for entry in entries]
                else:
                    for entry in entries:
                        if entry.is_dir():
                            dirs.extend(self.list_dirs(entry.path, depth - 1))
        except PermissionError:
            print(f"Permission denied: {path}")
        # return list(filter(lambda dir: not dir.startswith('.'), map(lambda path: path[path.rfind('/') + 1:] , dirs)))
        return dirs

    def remove_empty_dirs(self):
        """remove empty dirs under workspace
        """
        with os.scandir(self.workspace) as entries:
            for entry in entries:
                if entry.is_dir():
                    if not any(True for _ in os.scandir(entry.path)):
                        print(f"Removed empty directory: {entry.path}")
                        os.rmdir(entry.path)
        
    def remove_abandonned_dirs(self, dirs, dirs_should_exist):
        """remove dirs that are not in dirs_should_exist

        Args:
            dirs (list[str]): dirs that shall be deleted
            dirs_should_exist (list[str]): dirs that shall be kept
        """
        for dir in dirs:
            dir_name = dir[dir.rfind('/')+1 :]
            if dir_name.startswith('.'):
                continue
            elif dir_name not in dirs_should_exist:
                print(f"Delete {dir} since it's not configured anymore")
                try:
                    print(f"Deleted empty directory: {dir}")
                    shutil.rmtree(dir)
                except OSError as e:
                    print(f"Error: {e}")
        
    def update_indices(self):
        """update indices via invoking an existing sh script
        """
        os.system("rm /data/layne/tools/opengrok-1.7.32/src/*")
        os.system("ln -s /data/layne/src/* /data/layne/tools/opengrok-1.7.32/src/")
        os.system(f"sh /data/layne/tools/index_restart.sh >> {self.log_file}")
        
    def sync_all(self):
        """synchronise the workspace according to the cfg json file
        """
        print(f"Synchronisation Start!")
        os.chdir(self.workspace)
        self.init_cfg(self.cfg_file)
        # delete abandonned dirs
        gits_name, git_dirs_name = self.get_all_gits_name()
        repos_name = self.get_all_repos_name()
        self.remove_abandonned_dirs(self.list_dirs(path=self.workspace, depth=2), gits_name)
        self.remove_abandonned_dirs(self.list_dirs(path=self.workspace, depth=1), repos_name + git_dirs_name)
        # init repositories
        self.init_dirs()
        self.init_all_repos()
        self.init_all_gits()
        # remove empty dirs & update indices
        self.remove_empty_dirs()
        self.update_indices()
        
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