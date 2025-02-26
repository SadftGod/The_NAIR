from modules.file_operator import Shark 
from modules.palette import Palette as p

class Default:
   def __init__(self):
         self.read_def()
         
   def read_def(self):
      libs_file = "./requirements_desetup.txt"
      Shark(libs_file).lines_to_arr("next").set_up()
      
      libs_second  = "./requirements.txt"
      Shark(libs_second).lines_to_arr("next").set_up()
      
      del libs_file , libs_second
      