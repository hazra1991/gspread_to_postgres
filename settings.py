import os

class Spreadsheet_config:
    
    credential_path = os.environ['JSON_CRED']
    spreadsheetName = os.environ['SPREADSHEET_NAME'] 

class PostgresSQL_config:

    DRIVER = "postgresql"  # Dont change this  
    host = "localhost"
    port = 5432
    username = "postgres"
    password = "password123"

    # [optional] uncommenct and specify .DB name will automatically be fetched from spreadsheetName
    
    # database:= None       
