from app.database.decorators.connection import connection
from app.database.enums.db import Bases
from psycopg import sql
from modules.palette import Palette as p
import os
import json
from dotenv import load_dotenv
from modules.exceptions import RatException


class Configurator:


    @connection([Bases.admin.value])
    async def fill_admin(self , pool = None):
        db, cursor = pool[Bases.admin.value]
        tables = {
            "plans": [
                "_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
                "title VARCHAR(100) NOT NULL UNIQUE",
                "description TEXT NOT NULL"
            ],
            "permission": [
                "_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
                "title VARCHAR(150) NOT NULL UNIQUE",
                "description TEXT NOT NULL"
            ],
            "role": [
                "_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
                "title VARCHAR(30) NOT NULL UNIQUE"
            ],
            "plans_permissions": [
                "plan_id INTEGER REFERENCES plans(_id) ON DELETE CASCADE",
                "permission_id INTEGER REFERENCES permission(_id) ON DELETE CASCADE",
                "PRIMARY KEY (plan_id, permission_id)"
            ],
            "role_permission": [
                "role_id INTEGER REFERENCES role(_id) ON DELETE CASCADE",
                "permission_id INTEGER REFERENCES permission(_id) ON DELETE CASCADE",
                "PRIMARY KEY (role_id, permission_id)"
            ]
        }

        for table_name, columns in tables.items():
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({fields})").format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(map(sql.SQL, columns))
            )

            await cursor.execute(query)
        
        await db.commit()
        p.cyanTag("Bases","✅ Administrative configured")

    @connection([Bases.u.value])
    async def fill_users(self,pool):
        db, cursor = pool[Bases.u.value]
        load_dotenv()

        db_connection_params_str = os.getenv("DB_CONNECTION_PARAMS_DEFAULT")
        db_connection_params = json.loads(db_connection_params_str)
        host , port ,user, password = db_connection_params['host'],db_connection_params['port'],db_connection_params['user'],db_connection_params['password']
        dbname = Bases.admin.value
        queries = [
            sql.SQL("CREATE EXTENSION IF NOT EXISTS postgres_fdw;"),
            sql.SQL("""
                DO $$ 
                BEGIN 
                    IF EXISTS (SELECT 1 FROM pg_foreign_server WHERE srvname = 'plans_server') THEN
                        DROP SERVER plans_server CASCADE;
                    END IF;
                END $$;

                CREATE SERVER plans_server
                    FOREIGN DATA WRAPPER postgres_fdw
                    OPTIONS (host {}, port {}, dbname {});
            """).format(
                sql.Literal(str(host)),
                sql.Literal(str(port)),
                sql.Literal(str(dbname))
            )
            ,
            sql.SQL("""
                CREATE USER MAPPING FOR CURRENT_USER
                SERVER plans_server
                OPTIONS (user {}, password {});

                """).format(
                    sql.Literal(user),
                    sql.Literal(password)                
                    ),
            sql.SQL("""
                IMPORT FOREIGN SCHEMA public
                FROM SERVER plans_server
                INTO public;
            """),

            sql.SQL("""
                CREATE TABLE IF NOT EXISTS themes (
                    _id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    name VARCHAR(25) UNIQUE NOT NULL
                );
            """),
            sql.SQL("""
                CREATE TABLE IF NOT EXISTS users (
                    _id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    nickname VARCHAR(100) UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    pronounce VARCHAR(20),
                    plan_id INTEGER NOT NULL,
                    role_id INTEGER NOT NULL,
                    theme_id INTEGER NOT NULL,
                    avatar VARCHAR,
                    profile_hat VARCHAR,
                    language_id INTEGER NOT NULL,
                    sex CHAR(1) CHECK (sex IN ('M', 'F')),
                    birthday DATE,
                    status VARCHAR(30),
                    status_until TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_email_verified BOOLEAN DEFAULT FALSE,
                    social_google_id TEXT UNIQUE
                );
            """),
            sql.SQL("""
                CREATE OR REPLACE FUNCTION update_timestamp()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """),
            sql.SQL("""
                DROP TRIGGER IF EXISTS trigger_update_timestamp ON users;
            """),
            sql.SQL("""
                CREATE TRIGGER trigger_update_timestamp
                BEFORE UPDATE ON users
                FOR EACH ROW
                EXECUTE FUNCTION update_timestamp();
            """)


        ]

        for query in queries:
            await cursor.execute(query)
            await db.commit()
        p.cyanTag("Bases","✅ Users base configured")

    @connection([Bases.u.value])
    async def fill_subtables(self,pool):
        db, cursor = pool[Bases.u.value]
        tables = {
            "languages": [
                "_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY",
                "title VARCHAR(100) NOT NULL UNIQUE",
                "abbreviation CHAR(2) NOT NULL UNIQUE"
            ],
        }

        for table_name, columns in tables.items():
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({fields})").format(
                table=sql.Identifier(table_name),
                fields=sql.SQL(", ").join(map(sql.SQL, columns))
            )

            await cursor.execute(query)
        
        await db.commit()
        p.cyanTag("Bases","✅ Users subtable configured")

class DefaultDataCreature:

    @connection([Bases.admin.value])
    async def create_permissions(self,pool):
        db, cursor = pool[Bases.admin.value]
        admins_users_permissions = [("Update user","Permission that gave opportunity to update information in another user accout"),
                                    ("Ban","Block user account permanently"),
                                    ("Ban Until","Ban user accoount on some period"),
                                    ("Delete user","Can delete account of another user"),
                                    ("Approve email","Can approve account of another user without verification"),
                                    ("With admin","Can do the same, but with admin accounts")
                                    ]

        permissions_list = admins_users_permissions


    @connection([Bases.admin.value])
    async def create_roles(self, pool):
        db, cursor = pool[Bases.admin.value]
        roles = [("user",), ("support",), ("operator",), ("admin",), ("admin+",),("prime",)] 

        query = """
            INSERT INTO role (title)
            VALUES (%s)
            ON CONFLICT (title) DO NOTHING;
        """

        await cursor.executemany(query, roles)
        await db.commit()
        p.cyanTag("Bases","✅ Roles Added")

    @connection([Bases.admin.value])
    async def create_plans(self,pool):
        db, cursor = pool[Bases.admin.value]
        plans = [("default","Default plan that gives for all users",),
                ("echo","Temporary access for some characters , clothes for them and themes ",),
                ("eclipse","Gives an opportunity to give a custom name for a model, unlock a new cloth ,unlock a special character,gives current echo opportunities",),
                ]
                

        query = """
            INSERT INTO plans (title,description)
            VALUES (%s , %s)
            ON CONFLICT (title) DO NOTHING;
        """

        await cursor.executemany(query, plans)
        await db.commit()
        p.cyanTag("Bases","✅ Plans Added")

    @connection([Bases.u.value])
    async def create_themes(self,pool):
        db,cursor = pool[Bases.u.value]
        themes = [("default",),("nair",),("dark_punk",)]
        query = """
            INSERT INTO themes (name)
            VALUES (%s)
            ON CONFLICT (name) DO NOTHING;
        """

        await cursor.executemany(query, themes)
        await db.commit()
        p.cyanTag("Bases","✅ Themes Added")


    @connection([Bases.u.value])
    async def create_languages(self,pool):
        db,cursor = pool[Bases.u.value]

        languages = [("english",), ("ukrainian",), ("poland",), ("russian",)] 

        query = """
            INSERT INTO languages (title)
            VALUES (%s)
            ON CONFLICT (title) DO NOTHING;
        """

        await cursor.executemany(query, languages)
        await db.commit()
        p.cyanTag("Bases","✅ Roles Added")

    @connection([Bases.u.value])
    async def create_users(self,pool):
        db,cursor = pool[Bases.u.value]
        users = [("giber2017artur@gmail.com","Giber","D3F0JITu$3PII@CB0pD","Creator",3,41,3,"prime","prime","en",)]


