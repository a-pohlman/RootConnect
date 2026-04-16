#import built-in modules
from subprocess import run
from sys import executable

#import internal modules
from tooling.__init__ import __base_dir__

def run_script():
    while True:
        """Use below code if you have a compiled executable instead
        if run(args="main.exe", cwd=__base_dir__, shell=True).returncode != 5:
            break"""
        
        if run(args=executable+" main.pyw", cwd=__base_dir__).returncode != 5:
            break

if __name__ == "__main__":
    run_script()
