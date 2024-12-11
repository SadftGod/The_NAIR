import gc
import os
import time
import threading
import signal
from modules.palette import Palette as p 

class Module:
   @staticmethod
   def if_exist(parametr,default_value):
      if not parametr :
            return default_value
      return parametr

   @staticmethod
   def clean(*args):
      for arg in args:
            del arg
      gc.collect()

   @staticmethod
   def counter(folder:str)->int:
      """
      Returns count of files inside folder
      If folder doesn't exist - will create it
      """
      from colorama import Fore, Style
      if os.path.exists(folder):
            count = len(os.listdir(folder))
            print(f"[Checker] {Fore.CYAN}Folder {folder} has {count} files{Style.RESET_ALL}")
            return count

   @staticmethod
   def delete_replicates(folder1:str,folder2:str)->bool:
      """
      Delete the same files FROM FIRST FOLDER if it exists in SECOND FOLDER
      """
      dublicates = []
      for file1 in os.listdir(folder1):
            for file2 in os.listdir(folder2):
               if file1 == file2:
                  dublicates.append(file1)
      if len(dublicates) == 0:
            p.cyanTag("Checker","Folders haven't file's intertwining")
            return True
         
      p.red(f" You have {len(dublicates)} file's intertwining")
      p.yellow("Fixing")
      for dublicate in dublicates:
            if dublicate in os.listdir(folder1):
               remove_file = os.path.join(folder1, dublicate)
               os.remove(remove_file)
               p.pink(f"Removed {remove_file} from {folder1}")
      Module.clean(dublicates,remove_file,)
      return False

   def if_in(parametr:str,arr:list[str])-> bool:
      if not parametr in arr:
            return False
      return True

   @staticmethod
   def is_expired(exp:int):
      current_time = int(time.time())
      if current_time >= exp:
            True
      else:
            False
      
   @staticmethod
   def if_exist(parametr:str, default:any):
      if not parametr :
            return default
      return parametr
   
   @staticmethod
   def clean_up(file_path:str):
      with open(file_path, "w") as error_log:
            error_log.write("")

   def get_active_parallels():
      return threading.active_count()
   
   def as_terminator(port):
      import psutil
      for conn in psutil.net_connections():
            if conn.laddr.port == port:
               pid = conn.pid
               if pid is not None:
                  p.green(f"[PROCESS] Found process on port {port}  with PID {pid}, stopping...")
                  try:
                        os.kill(pid, signal.SIGTERM)  
                        p.green(f"[PROCESS] Successfully terminated process with PID {pid}.")
                  except OSError as e:
                        p.red(f"[ERROR] Could not terminate process {pid}: {e}")
               else:
                  p.red(f"[PROCESS] No PID found for port {port}")
      else:
            p.red(f"[PROCESS] No process found listening on port {port} .")
