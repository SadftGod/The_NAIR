import os
from modules.animations import Animations
import subprocess
from modules.palette import Palette as p

class Shark:
   def __init__(self,file):
      self.file = file
      self.libraries = None
      logs_dir = os.path.join(os.getcwd(), "logs")
      p.blue(logs_dir)
      os.makedirs(logs_dir, exist_ok=True)
      self.logs = os.path.join(logs_dir, "installing.log")    
      
      if not os.path.exists(self.file):
         raise Exception(f"{self.path} is not a file")


      
   def lines_to_arr(self, demeanor:str="return") -> list:

      with open(self.file, "r") as fuel:
         libraries = [line.strip() for line in fuel if line.strip() and not line.startswith("#")]
      
      match demeanor:
         case "return":
            return libraries
         case "next":
            self.libraries = libraries
            return self
         case _:
            raise Exception(f"Wrong demeanor: {demeanor}")

   
   @Animations.loading_animation(p.whiteBackReturn("Done with init"))
   def set_up(self):
      with open(self.logs, "a") as log_file:
            for lib in self.libraries:
                subprocess.run(
                    ["pip", "install", lib],
                    check=True,
                    stdout=log_file,
                    stderr=log_file
                )   
   
