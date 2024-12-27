import importlib
import importlib.util
import subprocess
import sys 
import os

class Scratch:
    def from_():
        scratch_arr = ["setuptools","psutil","tqdm","colorama"]
        if not os.path.exists("logs"):
           os.mkdir("logs")
        with open("logs/install_logs.log", "w") as log_file:
            for i in scratch_arr:
                if not importlib.util.find_spec(i):
                    subprocess.check_call([sys.executable, "-m", "pip", "install", i], 
                                            stdout=log_file, stderr=log_file)
    
   