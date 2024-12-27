try:
   import ast  
   import traceback        
   from modules.palette import Palette as p
except Exception as e:
   p.yellowFatTag("Exception Error",f"Can not import modules {e}")
   pass
            
class RatException(Exception):
   def __init__(self, error) -> None:
      super().__init__(error)
      self.error = error  
      
   def raiseRat(self):
      raise self  
   def detail():
      traceback.print_exc()
   
   def raiseDetail(self):
      traceback.print_exc()
      raise self 

   def catcher(e: Exception):
      tb = traceback.extract_tb(e.__traceback__)
      filename, linerNum , func , text = tb[-1]
      
      p.red(f"error {p.redBackReturn(e)}")
      with open('logs/thread_errors.log',"a") as log_file:
            log_file.write(f"Filename: {filename}, Line: {linerNum}, Function: {func}, Error: {e}\n")

   @staticmethod
   def fastRat(error):
      rat = RatException(error)
      rat.raiseRat()        

   @staticmethod
   def notAvailable():
      RatException.fastRat("Method not available now")
