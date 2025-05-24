import psycopg
import os
import json
from dotenv import load_dotenv
from app.database.enums.db import Bases


from modules.exceptions import RatException
from modules.palette import Palette as p

class baseModerator:
    def __init__(self,database:str=None):
        self._check_bases(database)
        self.db_connection_params = None
        try:
            load_dotenv()
            db_connection_params_str = os.getenv("DB_CONNECTION_PARAMS_DEFAULT")
            db_connection_params = json.loads(db_connection_params_str)

            db_connection_params["dbname"] = database
            self.db_connection_params = db_connection_params

        except Exception as e:
            RatException.fastRat(f"Can not connect to database : {e}")

    async def create_connection(self):
        try:
            conn = await psycopg.AsyncConnection.connect(**self.db_connection_params)
            cursor = conn.cursor()
            return conn, cursor
        except Exception as e:
            p.red(e)
        
    @staticmethod
    async def close_connections(connection,cursor):
        if 'cursor' in locals() and cursor:
            await cursor.close()
        if 'db' in locals() and connection:
            await connection.close()
            
    def _check_bases(self,base):
        if not base:
            RatException.fastRat("Wrong usage of decorator: Not database selected")
        if base not in [b.value for b in Bases]:
            RatException.fastRat("Database is not exits")


class BasePool:
    def __init__(self,input_databases: list = None):
        self._connections_checker(input_databases)
        self.input_databases = input_databases
        self.connections = dict()
    async def __call__(self):
        for base in self.input_databases:
            try:
                self.connections[base] = await baseModerator(base).create_connection()
            except Exception as e:
                RatException.catcher(e)
                
        if not self.connections or len(self.connections) < 1:
            RatException.fastRat("Can not working without any argument")
            
        return self.connections
    
    async def close_connections(self,name_pool):
        for db_name in name_pool:
            await baseModerator.close_connections(*self.connections[db_name])
    
    def _connections_checker(self,input_bases:list):
        if not input_bases or len(input_bases) < 1:
            RatException.fastRat("Can not working without any argument")
            
        