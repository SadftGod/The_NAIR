import os
from datetime import datetime
from modules.palette import Palette as p
import pytz


class Chronicle:
    def __init__(self,filename,dir:str="global") -> None:
        self.dir = dir
        self.filename = filename
        self.path = self.check_path()

        self.selected_tz = pytz.timezone('Europe/Kyiv')

        self.feather = self.Feather(self)


    def check_path(self):

        dir_map = {
            "global": "logs",
            "server": "server/logs",
            "daemon": "daemon/logs",
            "gateway": "gateway/logs"
        }

        if self.dir not in dir_map:
            p.red("Wrong Parameter")

        self.dir = dir_map[self.dir]

        
        if not os.path.exists(self.dir):
            if not os.path.isfile(self.dir):
                os.makedirs(self.dir)
            else:
                p.red(f"can not create directory {self.dir}")
        self.filename = self.filename.strip().replace(" ", "_")
        self.filename = self.filename.split(".")[0] + ".log"

        path = os.path.join(self.dir, self.filename)

        if not os.path.exists(path):
            with open(path,'w') as f:
                f.write("") 

        return path
    
    def clean(self):
        if not self.path or not os.path.exists(self.path):
            p.red("File does not exist, cannot clean")

        open(self.path, 'w', encoding='utf-8').close()
       
    def get_feather(self):
        return self.feather
    
    def get_path(self):
        return self.path

    
    class Feather:
        def __init__(self, chronicle:"Chronicle" ):
            self.path = chronicle.path
            self.selected_tz = chronicle.selected_tz

        def write(self,text):
            now_in_selected = datetime.now(self.selected_tz).strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.path,'a',encoding='utf-8') as f:
                f.write(f"\n [{now_in_selected}] " + text)
                f.flush()

        def rewrite(self,text):
            now_in_selected = datetime.now(self.selected_tz).strftime("%Y-%m-%d %H:%M:%S")
            
            with open(self.path,'w',encoding='utf-8') as f:
                f.write(f"[{now_in_selected}] " + text)
                f.flush()

        def erase(self,count:int=1):
            with open(self.path, 'r+', encoding='utf-8') as f:
                lines = f.readlines()
                if not lines:
                    return  

                count = min(count, len(lines))  
                f.seek(0)  
                f.writelines(lines[:-count])  
                f.truncate()
                if f.tell() == 0:
                    f.truncate(0)

