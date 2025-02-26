from modules.default import Default as d
import sys 
import os


class Adjuster:
   def __init__(self):
      root = os.path.dirname(os.path.abspath(__file__))
      sys.path.append(root)
      os.chdir(root)
      
      self._require()
      self._configurate()
   
   def _require(self):
      try:
         d()
      except Exception as e:
        print(e)
        
   def _configurate(self):
      from nllb_200.configurator import Configurator 
      Configurator()
        
        
Adjuster()