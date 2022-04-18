from asyncio import AbstractEventLoop
from functools import update_wrapper
import json
from optparse import Values
from venv import create
import pyodbc

"""
Function: class for database initialization
Status: Under construction.
Remark(s): 

"""
class DB_Init:
    def __init__(self) -> None:
        "Log Databse connection Initializaiton step"
        # 

        "Retrieve Json Data relating to Database Connection Initialization"
        self.json_data = json.load(open('./static/json/static.json'))["db"]

        "Initialize Class variables"
        self.db_conn=None
        self.db_conn_str=""

        "Perform Database Connectivity healthy check"
        self.db_connection_healthy=self.db_check()

        "Log Database Connectivity is healthy"
        print("Database Connectivity Healthy status: {}".format(self.db_connection_healthy))

        "Provide Functionality to Initialize database if db_conn_healthy = False"
        if not (self.db_connection_healthy and self.checkAllTableExists(self.db_conn, list(self.json_data["used_tables"].keys()))):

            "Create UX for recreating missing tables"
            print("It appears that not all tables are present in the Database {} ...".format(self.json_data["db_conn"]["db_db"]))
            bool_create_all_tables = input("Would you like to recreate all tables?[y/n]").upper()=="y".upper()
            bool_create_miss_tables = False

            "Check if user only wants to create missing tables"
            if not bool_create_all_tables:
                bool_create_miss_tables = input("Would you like to recreate the missing tables?[y/n]").upper()=="y".upper()
            

            "If creation of tables is approved, proceed accordingly"
            if bool_create_miss_tables:
                self.create_tables(self.db_conn, self.json_data["used_tables"])
            elif bool_create_all_tables:
                self.create_tables(self.db_conn, self.json_data["used_tables"],all_tables=True)

    """
    Function: Check Databse Health
    Status: Not Finished
    Remark(s): 
                - Still to incorporate Logging of errors
                - To be tested with Database Connection over the Network
    """
    def db_check(self):
        try:
            """
            Try and establish Open DataBase Connection
            Retrieve Database Connection data from Json Data: db_driver, db_server, db_db ~ db_database, db_port
            """
            db_driver = self.json_data["db_conn"]["db_driver"]
            db_server = self.json_data["db_conn"]["db_server"]
            db_db = self.json_data["db_conn"]["db_db"]
            db_port = self.json_data["db_conn"]["db_port"]

            "Construct Database Connection String"
            self.db_conn_str="Driver={};Server={};Database={};Trusted_Connection=yes;".format(db_driver, db_server, db_db)
            # self.db_conn = pyodbc.connect(self.json_data["connection_string"])

            "Test Database connection"
            self.db_conn = pyodbc.connect(self.db_conn_str)

            "Log a succesfull database connection at Initialization"
            # 
        except:
            "Log error occured during establishing Database Connectivity: No Open DataBase Connection could be established"
            print("gaat niet")

            "Return bad db connection"
            return False

        """
        Try and detect existing tables and retrieve data from it, if not, create tables except the user table..
        First Loop through all tables which will be needed for the application:
        """
        return self.checkAllTableExists(self.db_conn, list(self.json_data["used_tables"].keys()))


        pass

    def checkAllTableExists(self, dbcon, list_of_tables):
        for table in list_of_tables:
            
            "If it doesn't exist, return False"
            if not self.checkTableExists(dbcon,table):
                return False

        "Looped through all tables succesfully, return True"
        return True

    """
    Function: Check if table already exists in Database
    Status: Finished
    Remark(s): 
    
    """
    def checkTableExists(self, dbcon, tablename):
        """
        This function checks if the tablename exists in this database connection (dbcon).
        First a database connection Cursos has to be created
        """
        dbcur = dbcon.cursor()

        "Perform following query:"
        dbcur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))

        "Does the queried tablename exist?"
        if dbcur.fetchone()[0] == 1:
            dbcur.close()
            return True

        "Close Database cursor"
        dbcur.close()
        return False

    """
    Funciton: Create a table in the Database.
    Status: Finished.
    Remark:
    """
    def create_table(self, dbcon, table_name, cols):
        "Prepare elements for the column IDs and Datatyope - string"
        col_ids = []

        "Loop through all table columns"
        for key, value in cols.items():

            "Store the column and datatype"
            col_ids.append(" ".join([key, value]))
            pass

        "Once looped through all columns, create string for query"
        col_ids=", ".join(col_ids)

        "Prepare SQL Query, create connection Cursor()"
        dbcur = dbcon.cursor()

        "Prepare SQL Query Strinh"
        dbcur_string = """
        CREATE TABLE {}({})
        """.format(table_name, col_ids)

        try:
            "Execute SQL Query"
            dbcur.execute(dbcur_string)
            
            "After altering, creating via query always commit via the db connection"
            dbcon.commit()
        except pyodbc.ProgrammingError as e:
            "Log creation of table failed: Table already exists in Database"
            print("Creation of table '{}' failed, table already exists probably".format(table_name))
            print("Following error got thrown..\n{}".format(e.__str__))

    """
    Function: Create All or only missing tables
    Status: Finished
    Remark(s): 
    
    """
    def create_tables(self, dbcon, tables, all_tables=False):
        "Loop though all existing tables"
        for table in tables:
            
            "If instructed to create all tables in the list then create all, otherwise only create the missing tables"
            if all_tables:
                self.create_table(dbcon, table, tables[table])
            elif not (all_tables and self.checkTableExists(dbcon, table)):
                self.create_table(dbcon, table, tables[table])
        
    """
    Function: Insert Record into a given table
    Status: Under Construction
    Remark(s): 
    
    """
    def insert_record(self,table,values):
        
        cols=self.json_data['used_tables'][table]
        
        dbcur=self.db_conn.cursor()

        maxid = dbcur.execute("select max({}) from {};".format("TransactionID", table)).fetchval()
        if maxid:
            maxid += 1
        else:
            maxid = 1
        
        dbcur_string="""
            insert into {}({}) values ({});
        """.format(table, ", ".join(list(cols.keys())), ", ".join([str(maxid), *values]))

        dbcur.execute(dbcur_string)

        dbcur.commit()
    """
    Function: Remove Record from a given table
    Status: Under Construction
    Remark(s): 
    
    """
    def remove_record(self,table, pk):
        pass

    """
    Function: Update Record in a given table
    Status: Under Construction
    Remark(s): 
    
    """
    def update_record(self, table,pk, new_record):
        pass