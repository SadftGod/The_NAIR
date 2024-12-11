import os
import sys 
import signal
from modules.setup import SetUp

if __name__ == "__main__":
   
   root = os.path.dirname(os.path.abspath(__file__))
   sys.path.append(root)
   os.chdir(root)
   print("SetUp",f"Root setted to {root}")
   
   su = SetUp()
   su()