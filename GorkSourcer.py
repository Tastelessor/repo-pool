import os
import subprocess
import json
import argparse
import schedule
import time
from datetime import datetime
from collections import namedtuple
from RepoPool import RepoPool

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Argument Parser Example")

    parser.add_argument('-w', '--workspace',    help='All operation', required=True)
    parser.add_argument('-c', '--config',       default="repos.json", help='All operation')
    parser.add_argument('-d', '--delete',       help='Delete certain repository')
    parser.add_argument('-u', '--update',       action='store_true', help='Update operation')
    parser.add_argument('-a', '--all',          action='store_true', help='Update all repos')
    parser.add_argument('-t', '--time',         default="2:00", help='Time to run this program')

    args = parser.parse_args()
    
    # Init basic configs
    config_file_path = args.config
    if config_file_path == "repos.json":
        config_file_path = os.path.join(args.workspace, config_file_path)
    repo_pool = RepoPool(workspace=args.workspace, cfg_file=config_file_path)
    
    if args.all:
        now = datetime.now()
        print(f"All repos configured in [{config_file_path}] will be run every single day at {args.time}")
        repo_pool.get_gits_by_name("A")
        repo_pool.get_repo_by_name("A")
        repo_pool.sync_all()
        # schedule.every().day.at("10:57", "Asia/Shanghai").do(repo_pool.sync_all)
        # while 1:
        #     schedule.run_pending()
        #     # schedule.every(1).minute.do(repo_pool.sync_all)
        #     time.sleep(10)
        #     print("1s passed")