import openai
import pyodbc

# Set your OpenAI API key here
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

# Example: MS SQL Server 2019 connection details
SQL_SERVER = 'localhost'
SQL_DATABASE = 'YourDatabase'
SQL_USERNAME = 'YourUsername'
SQL_PASSWORD = 'YourPassword'

# Function to get all table schemas from SQL Server
def get_all_table_schemas():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}')
    cursor = conn.cursor()
    cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    tables = [row[0] for row in cursor.fetchall()]
    schemas = {}
    for table in tables:
        cursor.execute(f"SELECT COLUMN_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}'")
        schemas[table] = cursor.fetchall()
    conn.close()
    return schemas

# Function to get stored procedures and their parameters
def get_stored_procedures():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.procedures")
    procs = [row[0] for row in cursor.fetchall()]
    proc_params = {}
    for proc in procs:
        cursor.execute(f"SELECT PARAMETER_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.PARAMETERS WHERE SPECIFIC_NAME = '{proc}'")
        proc_params[proc] = cursor.fetchall()
    conn.close()
    return procs, proc_params

# Function to get user-defined functions and their parameters
def get_user_defined_functions():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USERNAME};PWD={SQL_PASSWORD}')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.objects WHERE type IN ('FN', 'IF', 'TF')")
    funcs = [row[0] for row in cursor.fetchall()]
    func_params = {}
    for func in funcs:
        cursor.execute(f"SELECT PARAMETER_NAME, DATA_TYPE FROM INFORMATION_SCHEMA.PARAMETERS WHERE SPECIFIC_NAME = '{func}'")
        func_params[func] = cursor.fetchall()
    conn.close()
    return funcs, func_params

# Function to generate SQL query, stored proc, or function call from English using OpenAI
def generate_sql_query(nl_query, schemas, procs, proc_params, funcs, func_params):
    schema_str = '\n'.join([f"Table {table}: " + ', '.join([f"{col[0]} ({col[1]})" for col in cols]) for table, cols in schemas.items()])
    procs_str = '\n'.join([f"{proc}({', '.join([f'{p[0]} {p[1]}' for p in proc_params[proc]])})" for proc in procs])
    funcs_str = '\n'.join([f"{func}({', '.join([f'{p[0]} {p[1]}' for p in func_params[func]])})" for func in funcs])
    prompt = f"Given the following database schema:\n{schema_str}\nStored procedures:\n{procs_str}\nUser-defined functions:\n{funcs_str}\nWrite a SQL Server 2019 query, stored procedure call, or function call for: {nl_query}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=250
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    openai.api_key = OPENAI_API_KEY
    nl_query = input("Enter your question in English: ")
    schemas = get_all_table_schemas()
    procs, proc_params = get_stored_procedures()
    funcs, func_params = get_user_defined_functions()
    print("\nDatabase tables and columns:")
    for table, cols in schemas.items():
        print(f"- {table}: {[col[0] for col in cols]}")
    print("\nStored procedures and parameters:")
    for proc in procs:
        print(f"- {proc}: {[f'{p[0]} {p[1]}' for p in proc_params[proc]]}")
    print("\nUser-defined functions and parameters:")
    for func in funcs:
        print(f"- {func}: {[f'{p[0]} {p[1]}' for p in func_params[func]]}")
    sql_query = generate_sql_query(nl_query, schemas, procs, proc_params, funcs, func_params)
    print("\nGenerated SQL Query / Stored Procedure / Function Call:")
    print(sql_query)
