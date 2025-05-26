import os
from modules.exceptions import RatException
import sys 
import subprocess
import pkg_resources
from tqdm import tqdm


class Libs:
    def __init__(self) -> None:
        self.requirements = "requirements.txt"
        self.lib_list = None
        self.counter = 0
        self.done_counter = 0
    
    def __is_installed(self,package):
        with open("logs/install_logs.log", "w") as log_file:
            try:
                from modules.palette import Palette as p
                pkg_resources.get_distribution(package)
                self.done_counter += 1
                return True
            except pkg_resources.DistributionNotFound:
                self.counter += 1
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                        stdout=log_file, stderr=log_file)
                    return True
                except subprocess.CalledProcessError:
                    with open("logs/install_error.log", "w") as error_logs:
                        error_logs.write(f"Package {package} failed to install.\n")
                    return False
        
    def check(self):
        if not os.path.isfile(self.requirements):
            rat = RatException("Oh.... Requirements file got lost")
            rat.raiseDetail()
        with open(self.requirements,"r") as libraries_files:
            libraries = libraries_files.readlines()
        for library in tqdm(libraries, desc="Installing Libraries", unit="library"):
            self.__is_installed(library)
        
        from modules.palette import Palette as p
        if self.counter > 0:
            p.yellowTag("PREPARATOR",f"{self.counter} was not installed before,but installed now")
        elif self.done_counter > 0:
            p.cyanTag("PREPARATOR",f"All libraries was installed")
        else:
            p.redTag("PREPARATOR", f"SOMETHING GONE WRONG >> Nothung was not installed and nothings will be not installed")
