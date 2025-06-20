import os
import sys 
import signal
import subprocess


class SetUp:
   async def __call__(self):
      signal.signal(signal.SIGINT, self.signal_exit)
      self.check_venv()

      from modules.preparation import Preparator
      pre = Preparator()

      pre.load()

      from modules.palette import Palette as p
      
      from modules.secret_coder import GCoder
      gc = GCoder()
      gc()
      
      try:
         await self.fill_databases()
      finally:
         from modules.module import Module as m
         
         m.clean_up("logs/daemon_error.log")


   async def fill_databases(self):
      from app.database.configurators.configurator import Configurator ,DefaultDataCreature
      await Configurator().fill_admin()
      await Configurator().fill_subtables()
      await Configurator().fill_users()
      
      await DefaultDataCreature().create_roles()
      await DefaultDataCreature().create_plans()
      await DefaultDataCreature().create_themes()
      await DefaultDataCreature().create_languages()
      await DefaultDataCreature().create_users()
      
      from app.servers.grpc import GRPC_server
      port = 50526
      server = GRPC_server()()
      server.add_insecure_port(f'[::]:{port}')
      await server.start()

      from modules.palette import Palette as p
    
      p.cyanTag("gRPC Server",f"Started on {p.whiteBackReturn(port)}")
      await server.wait_for_termination() 

   
   def check_venv(self):
      """Check if running inside a virtual environment"""
      venv_path = os.getenv('VIRTUAL_ENV')
      venv_name = os.path.basename(venv_path) if venv_path else None
      default_venv = 'venvire'
      if venv_name != default_venv:
         print(f"Error: The script is not running inside the {default_venv} virtual environment.")
         self.create_venv(default_venv)
         print(f"Now you can enter the venv '{default_venv}'")
         sys.exit(1)

      if sys.prefix == sys.base_prefix:
         print(f"Error: The script is not running inside any virtual environment.")
         self.create_venv(default_venv)
         print(f"Now you can enter the venv '{default_venv}'")
         sys.exit(1)

      print(f"Current envire : {venv_name}")

   def create_venv(self,venv_name:str):
      python_executable = sys.executable
      venv_path = os.path.join(os.getcwd(), venv_name)
   
      from modules.palette import Palette as p
   
      if os.path.exists(venv_path):
         print(f"Bruh, '{venv_name}' already exists in {venv_path}")
         return
      
      try:
         print(f"Creating '{venv_name}'...")
         subprocess.run([python_executable, "-m", "venv", venv_path], check=True)
         print(f"Venv '{venv_name}' created in {venv_path}")
      except subprocess.CalledProcessError as e:
         print(f"Error creating venv: {e}")
         sys.exit(1)
   
   def signal_exit(self,sig, frame):
      from modules.palette import Palette as p
      from modules.module import Module as m
      
      p.redBack("Signal CTRL+C detected")
      p.red("Started to clean up logs,sir")
      m.clean_up("./daemon/daemon_error.log")
      parallels_count = m.get_active_parallels()
      
      p.yellowTag("Threads",f"{parallels_count} steal active")

