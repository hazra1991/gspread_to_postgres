import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, Text, String, DateTime
import datetime

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




def excecute():
    from settings import Spreadsheet_config as sp_config, 
    from settings import PostgresSQL_config as psql_config
    if psql_config.__dict__.get('database'):
        database =  psql_config.database
    else:
        database =  sp_config.spreadsheetName
    # host = "localhost"
    # port = 5432
    # username = "postgres"
    # password = "password123"
    # database = "goanddo" 
    # database = "postgres" 
    db_uri = f"postgresql://{psql_config.username}:{psql_config.password}@{psql_config.host}:{psql_config.port}"
    /{psql_config.database}
    if not database_exists(db_uri,)
    engine = create_engine(db_uri, echo=True)

if __name__ == "__main__":
    pass

