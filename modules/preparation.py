from modules.scratch import Scratch

class Preparator:
    def __init__(self) -> None:
        pass
     
    def load(self):
         """
         Method to download necessariest libs for server works
         """
         Scratch.from_()
         from modules.exceptions import RatException
         try:

        
            from modules.libs import Libs
            libs = Libs()
        
            libs.check()
         except RatException as e:
            RatException.catcher(e)