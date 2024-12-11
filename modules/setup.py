import os
import sys 
import signal

from modules.argparser import parse_args
class SetUp:
   def __call__(self):
      signal.signal(signal.SIGINT, self.signal_exit)
      self.check_venv()

      from modules.preparation import Preparator
      pre = Preparator()

      pre.load()

      from modules.palette import Palette as p



      args = parse_args()
      
      from modules.secret_coder import sc
      sc.generate_random_hash()
      
      try:
         self.start_grpc()
      finally:
         from modules.module import Module as m
         
         m.clean_up("logs/daemon_error.log")

      
   def start_grpc(self):
      from modules.palette import Palette as p
      p.red("Passed")
   
   def check_venv(self):
      """Check if running inside a virtual environment"""
      venv_path = os.getenv('VIRTUAL_ENV')
      venv_name = os.path.basename(venv_path) if venv_path else None

      if venv_name != 'envire':
         print(f"Error: The script is not running inside the 'envire' virtual environment.")
         sys.exit(1)

      if sys.prefix == sys.base_prefix:
         print(f"Error: The script is not running inside any virtual environment.")
         sys.exit(1)

      print(f"Current envire : {venv_name}")

   
   def signal_exit(self,sig, frame):
      from modules.palette import Palette as p
      from modules.module import Module as m
      
      p.redBack("Signal CTRL+C detected")
      p.red("Started to clean up logs,sir")
      m.clean_up("./daemon/daemon_error.log")
      parallels_count = m.get_active_parallels()
      
      p.yellowTag("Threads",f"{parallels_count} steal active")

