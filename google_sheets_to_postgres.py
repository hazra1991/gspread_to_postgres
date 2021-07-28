import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import sqlalchemy as sa
from sqlalchemy.engine import make_url
from sqlalchemy.sql.expression import true
# from sqlalchemy.types import Integer, Text, String, DateTime
import datetime

from sqlalchemy.util.deprecations import SQLALCHEMY_WARN_20


class GoogleSheetHelper:
    """Helper class to pull data from googlesheets"""
    def __init__(self, cred_json, spreadsheetName):
        self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.cred_json = cred_json
        self.spreadsheetName = spreadsheetName
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(self.cred_json, self.scope)
        self.client = gspread.authorize(self.creds)

    def getDataframe(self,worksheet):
        """Returns all rows data from sheet as dataframe"""
        spreadsheet = self.client.open(self.spreadsheetName)
        sheet = spreadsheet.worksheet(worksheet)
        rows = sheet.get_all_records()
        return pd.DataFrame(rows)

    def getAllWorksheet(self):
        spreadsheet = self.client.open(self.spreadsheetName)
        return [s.title for s in spreadsheet.worksheets()] 

    def getAllSpreadsheets(self):
        """Returns sheets this gspread (self.client) authorized to view/edit"""
        available_sheets = self.client.openall()
        print(available_sheets)
        return [sheet.title for sheet in available_sheets]


def _set_url_database(url , databasename):
    """creates url with provided DB for the engine """

    url = make_url(url)
    if hasattr(sa.engine, 'URL'):
        res = sa.engine.URL.create(
            drivername=url.drivername,
            username=url.username,
            password=url.password,
            host=url.host,
            port=url.port,
            database=databasename,
            query=url.query
        )
    else:  # SQLAlchemy <1.4
        url.database = databasename
        res = url

    return res


def database_exists(url:str,dbname:str)->bool:
    """Checkes if the database exists and returns bool"""

    query  =  f"SELECT 1 FROM pg_database WHERE datname='{dbname}'"
    en = sa.create_engine(url)
    with en.connect() as con:
        r = con.scalar(query)
    if r :
        return True
    return False


def create_database(url,dbname):
    sql = f'CREATE DATABASE "{dbname}"'
    en = sa.create_engine(url,isolation_level="AUTOCOMMIT", echo=True)
    with en.connect() as con:
        con.execute(sql)

 
    
def excecute():

    from settings import Spreadsheet_config as sp_config
    from settings import PostgresSQL_config as psql_config

    if psql_config.__dict__.get('database'):
        database =  psql_config.database
    else:
        database =  sp_config.spreadsheet_name
    
    DBDRIVER = psql_config.__dict__.get("DRIVER","postgresql")
    
    uri = f"{DBDRIVER}://{psql_config.username}:{psql_config.password}@{psql_config.host}:{psql_config.port}"

    if not database_exists(uri,database):
        create_database(uri,database)
    
    url_with_db = _set_url_database(uri,database)
    
    engine = sa.create_engine(url_with_db, echo=True)

    main_sheet = GoogleSheetHelper(sp_config.credential_path, sp_config.spreadsheet_name)

    if sp_config.backup_all_worksheets:
        wrksheet_list = main_sheet.getAllWorksheet()
    else:
        wrksheet_list =  sp_config.worksheet_to_consider

    for wrksht in wrksheet_list:
        df = main_sheet.getDataframe(wrksht)
        table_name = wrksht
        current_utc = datetime.datetime.utcnow()
        df["CreatedUTC"] = current_utc
        df.to_sql(
            table_name,
            engine,
            if_exists='replace',
            index=False,
            chunksize=500,
        )


if __name__ == "__main__":
    pass

    excecute()