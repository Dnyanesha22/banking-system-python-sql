import pyodbc

def get_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=LIN-5L2GBK3\\SQLEXPRESS;"
        "DATABASE=Banking DB;"
        "Trusted_Connection=yes;"
    )