import os
import sys 
import signal
from modules.setup import SetUp
import asyncio

async def main():
   
   root = os.path.dirname(os.path.abspath(__file__))
   sys.path.append(root)
   os.chdir(root)
   print("SetUp",f"Root setted to {root}")
   
   su = SetUp()
   await su()

if __name__ == "__main__":
   asyncio.run(main())