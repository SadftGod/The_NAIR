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
        self.returning_clause = sql.SQL("")

        self.conflict_strategy = None
        self.conflict_columns = []
        self.update_fields = []
        self.ctes = []


    def _beautify_params(self,params):
        if not isinstance(params,tuple):
            params = tuple(params)
        else:
            params = params

        return params
    
    def _base_worker(self,base):
        parts = base.split(" ", 1)
        base_name = parts[0].strip()
        base_alias = parts[1].strip() if len(parts) > 1 else ''

        return base_name, base_alias

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

    def on_conflict(self,strategy:str,*columns: str):
        strategies = ['nothing','update']

        if not strategy.lower().strip() in strategies:
            RubberException.fastRubber("Strategy is not allowed",13)
        
        self.conflict_strategy = strategy.lower().strip()
        match strategy:
            case "nothing":
                pass
            case "update":
                if len(columns) < 2:
                    RubberException.fastRubber("Update strategy requires conflict columns AND update fields", 13)
                self.conflict_columns = [columns[0]]
                self.update_fields = list(columns[1:])

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
            alias = sql.Identifier(self.base_alias) if self.base_alias else sql.SQL(""),
            joins=self.joins,
            where = self.wheres
        )
   
    def build_insert(self):
        base_insert = sql.SQL("INSERT INTO {table} ({fields}) VALUES ({values})").format(
            table=sql.Identifier(self.base),
            fields=self.whats,
            values=sql.SQL(', ').join(sql.Placeholder() * len(self.params)),
        )
        if self.conflict_strategy and self.conflict_columns:
            conflict_clause = sql.SQL(" ON CONFLICT ({})").format(
                sql.SQL(", ").join(sql.Identifier(col) for col in self.conflict_columns)
            )

            match self.conflict_strategy:
                case "nothing":
                    conflict_clause += sql.SQL(" DO NOTHING")
                case "update":
                    if not self.update_fields:
                        RubberException.fastRubber("Update fields must be provided for update strategy", 13)
                    update_pairs = [
                        sql.SQL("{} = EXCLUDED.{}").format(
                            sql.Identifier(f), sql.Identifier(f)
                        ) for f in self.update_fields
                    ]
                    update_pairs.append(
                        sql.SQL("created_at = NOW() + interval '2 minutes'")
                    )

                    update_clause = sql.SQL(', ').join(update_pairs)

                    conflict_clause += sql.SQL(" DO UPDATE SET ") + update_clause

            base_insert += conflict_clause
        base_insert += self.returning_clause

        self.query = base_insert

    def build_update(self):
        if not self.whats or self.whats.as_string(self.cursor) == "*":
            RubberException.fastRubber("Update requires specific fields to set", 13)

        fields = []

        if isinstance(self.whats, sql.Composed):
            for part in self.whats:
                if isinstance(part, sql.Identifier):
                    fields.append(part)
                elif isinstance(part, sql.Composed):
                    fields.extend(p for p in part if isinstance(p, sql.Identifier))
                else:
                    continue
        elif isinstance(self.whats, sql.Identifier):
            fields.append(self.whats)
        else:
            RubberException.fastRubber("Unknown whats parameter", 2)

        if not fields:
            RubberException.fastRubber("No fields to update", 10)

        set_clause = sql.SQL(", ").join(
            sql.SQL("{} = {}").format(
                f,
                sql.Placeholder()
            ) for f in fields
        )

        base_update = sql.SQL("UPDATE {table} SET {set_clause} {where_clause}").format(
            table=sql.Identifier(self.base),
            set_clause=set_clause,
            where_clause=self.wheres
        )

        base_update += self.returning_clause
        self.query = base_update

    def build_delete(self):
        self.query = sql.SQL(
            "DELETE FROM {table} {alias} {where}"
        ).format(
            table = sql.Identifier(self.base),
            alias = sql.Identifier(self.base_alias),
            where=self.wheres
        )


    def add_cte(self, ctes: tuple[sql.Composed], names: tuple[str]):
        if len(ctes) != len(names):
            RubberException.fastRubber("Length of ctes and names must be the same", 13)

        for cte, name in zip(ctes, names):
            if not isinstance(cte, sql.Composed):
                RubberException.fastRubber("Each CTE must be a sql.Composed object", 13)
            composed_cte = sql.SQL("{} AS ({})").format(
                sql.Identifier(name),
                cte
            )
            self.ctes.append(composed_cte)

        return self




    def join(self,base:str,on:str):
        base, alias = self._base_worker(base)
        join_sql = sql.SQL(" INNER JOIN {table} {alias} ON {cond}").format(
            table=sql.Identifier(base),
            alias = sql.Identifier(alias),
            cond=sql.SQL(on)
        )
        self.joins = sql.SQL("").join([self.joins, join_sql])
        return self


    def returning(self, *returning):
        self.returning_clause = sql.SQL(" RETURNING ") + sql.SQL(', ').join(
                sql.SQL(item) for item in returning
            )
        return self



    def _apply_ctes(self, query: sql.Composable) -> sql.Composable:
        if not self.ctes:
            return query

        cte_section = sql.SQL("WITH ") + sql.SQL(", ").join(self.ctes)
        return cte_section + sql.SQL(" ") + query



    async def call(self, req_type:str="select",return_type:str="tuple",need_commit:bool=False,get:bool = False,printed:bool = True, ):
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

            case "insert":
                self.build_insert()

            case "update":
                self.build_update()

            case "delete":
                self.build_delete()

        self.query = self._apply_ctes(self.query)
        if printed:
            p.blueTag("Harp log",self.query.as_string(self.cursor))
            p.blueTag("Harp log",self.params)
        if get:
            return self.query , self.params
        



        match req_type:
            case "select":
                await self.cursor.execute(self.query,self.params)
                rows = await self.cursor.fetchall()
                if need_commit:
                    await self.db.commit()

            case "insert":
                await self.cursor.execute(self.query, self.params )
                rows = await self.cursor.fetchall()
                if need_commit:
                    await self.db.commit()

            case "update":
                await self.cursor.execute(self.query, self.params )
                rows = await self.cursor.fetchall()
                if need_commit:
                    await self.db.commit()

        match return_type:
            case "dict":
                cols = [col.name for col in self.cursor.description]
                return [dict(zip(cols, row)) for row in rows]
            case "tuple":
                return rows