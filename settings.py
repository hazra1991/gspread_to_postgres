import os

class Spreadsheet_config:
    credential_path = os.environ['JSON_CRED']
    spreadsheetName = os.environ['SPREADSHEET_NAME'] 

class PostgresSQL_config:
    host = "localhost"
    port = 5432
    username = "postgres"
    password = "password123"
    # database:= None      '''[optional] uncommenct and specify .Note the DB name will automatically be fetched from spreadsheetName'''  
    # database = "postgres" 
