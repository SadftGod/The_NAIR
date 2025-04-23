import psycopg
from psycopg import sql
from psycopg.sql import Composable
from psycopg.rows import dict_row
import re
from modules.palette import Palette as p
from modules.server_exceptions import RubberException

class Harp:
    def __init__(self, pool:dict,base:str,params):
        self.db, self.cursor = pool
        self.base, self.base_alias = self._base_worker(base)
        self.params = self._beautify_params(params)
        self.whats = sql.SQL("*")
        self.wheres = sql.SQL("")
        self.query = sql.SQL("")
        self.joins = sql.SQL("")


    def _beautify_params(self,params):
        if not isinstance(params,tuple):
            params = tuple(params)
        else:
            params = params

        return params
    
    def _base_worker(self,base):
        base ,base_alias = base.split(" ",1)
        return base.strip() , base_alias.strip()

    def what(self, *fields:str):
        sql_fields: list[Composable] = []

        for f in fields:
            if isinstance(f, Composable):
                sql_fields.append(f)
                continue
            if " " in f or "(" in f or ")" in f:
                sql_fields.append(sql.SQL(f))
                continue

            if "." in f:
                alias, col = f.split(".", 1)
                sql_fields.append(
                    sql.SQL("{}.{}").format(
                        sql.Identifier(alias),
                        sql.Identifier(col)
                    )
                )
            else:
                sql_fields.append(sql.Identifier(f))

        
        self.whats = sql.SQL(", ").join(sql_fields)
        return self


    def where(self,where_condition):
        tokens = re.split(r'\s+(AND|OR)\s+', where_condition, flags=re.IGNORECASE)
        sql_tokens = []
        for idx, tok in enumerate(tokens):
            if idx % 2 == 0:
                sql_tokens.append(sql.SQL(tok.strip()))
            else:
                sql_tokens.append(sql.SQL(tok.upper()))

        where_sql = sql.SQL(" ").join(sql_tokens)
        self.wheres = sql.SQL(" WHERE {}").format(where_sql)
        return self
    
    def build_select(self):
        self.query = sql.SQL("SELECT {fields} FROM {table} {alias} {joins}{where}").format(
            fields = self.whats,
            table = sql.Identifier(self.base),
            alias = sql.Identifier(self.base_alias),
            joins=self.joins,
            where = self.wheres
        )

    def build_delete(self):
        self.query = sql.SQL(
            "DELETE FROM {table} {alias} {where}"
        ).format(
            table = sql.Identifier(self.base),
            alias = sql.Identifier(self.base_alias),
            where=self.wheres
        )

    def join(self,base:str,on:str):
        base, alias = self._base_worker(base)
        join_sql = sql.SQL(" INNER JOIN {table} {alias} ON {cond}").format(
            table=sql.Identifier(base),
            alias = sql.Identifier(alias),
            cond=sql.SQL(on)
        )
        self.joins = sql.SQL("").join([self.joins, join_sql])
        return self


    async def call(self, req_type:str="select",return_type:str="tuple"):
        possible_req = ["select","insert","update","delete"]
        possible_return = ["tuple","dict"]

        req_type = req_type.strip().lower()
        return_type = return_type.strip().lower()
        if not req_type in possible_req:
            RubberException.fastRubber(f"Wrong request type choose one of {possible_req}",13)
        if not return_type in possible_return:
            RubberException.fastRubber(f"Wrong return type choose one of {possible_return}",13)


        match req_type:
            case "select":
                self.build_select()

            case "delete":
                self.build_delete


        p.blueTag("Harp log",self.query.as_string(self.cursor))
        p.blueTag("Harp log",self.params)

        match req_type:
            case "select":
                await self.cursor.execute(self.query,self.params)
                rows = await self.cursor.fetchall()

        match return_type:
            case "dict":
                cols = [col.name for col in self.cursor.description]
                return [dict(zip(cols, row)) for row in rows]
            case "tuple":
                return rows
            
        
