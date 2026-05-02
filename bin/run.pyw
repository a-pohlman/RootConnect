#import built-in modules
from subprocess import run
from sys import executable

#import internal modules
from tooling.__init__ import __base_dir__, __path_separator__

def run_script():
    while True:
        """Use below code if you have a compiled executable instead
        if run(args="main.exe", cwd=__base_dir__, shell=True).returncode != 5:
            break
        """
        
        """Use below code for darwin or linux distributions (darwin systems untested!)
        if run(args=executable+" "+__base_dir__+__path_separator__+"main.pyw", shell=True).returncode != 5:
            break
        """

        """Use below code for Windows systems"""
        if run(args=executable+" main.pyw", cwd=__base_dir__).returncode != 5:
            break
        
if __name__ == "__main__":
    run_script()
