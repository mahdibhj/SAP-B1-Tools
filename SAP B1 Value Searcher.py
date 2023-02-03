import pyodbc
import pandas as pd

searched_values = ['VALUE TO SEARCH']

columns_to_not_consider = ["LogEntry","SysNumber","MdAbsEntry","DocNum","Series","Time","CountType"]

con = pyodbc.connect(driver="{SQL Server}",server='DB_SERVER',database='DB_NAME',Trusted_Connection='yes')
cur = con.cursor()

def check_if_table_is_empty(table_name):
    try:
        query = """SELECT TOP 1 * from {0}""".format(table_name)
        #print(query)
        results = cur.execute(query).fetchall()
        #print(len(results))
        if not results:
            return True
        else:
            return False
    except:
        pass


def get_table_names_from_db():
    #print('fetching tables names...')
    query = """
    SELECT TABLE_NAME
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_TYPE='BASE TABLE'
    """
    sql_res = cur.execute(query)
    #print('Query executed...')
    data = sql_res.fetchall()
    #print ('Raw data fetched from db...')
    table_names = []
    for table_name in data:
        clean_table_name = str(table_name).split("'")[1]
        if not(clean_table_name.startswith("@")):
            if not(check_if_table_is_empty(clean_table_name)) :
                table_names.append(clean_table_name)
            else:
                pass
        #print (clean_table_name)
    #print('Table names cleaned...')
    return table_names


def get_columns_names_from_db(table_name):
    #print('Fetching columns names from the table '+table_name)
    query = """
    SELECT
        COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE
    FROM
        INFORMATION_SCHEMA.COLUMNS
    WHERE
        TABLE_NAME = '{0}'
    ORDER BY 2
    """.format(table_name)
    #print(query)
    sql_res = cur.execute(query)
    #print('Query executed...')
    data = sql_res.fetchall()
    #print ('Raw data fetched from db...')
    columns_names = []
    for col_names in data:
        clean_col_names = str(col_names).split("'")[1]
        columns_names.append(clean_col_names)
        #print (clean_table_name)
    #print('Columns names cleaned...')
    return columns_names



tables = get_table_names_from_db()
print(str(len(tables))+" non empty tables"  )

db_dictionary = {}
for table in tables:
    #print(table)
    cols = get_columns_names_from_db(table)
    db_dictionary[table] = cols
    #print(len(cols))


def get_column_data_from_db(table,column):
    query = """SELECT [{0}] FROM {1}""".format(column,table)
    #print(query)
    try:
        sql_res = cur.execute(query)
        #print('Query executed...')
        raw_data = sql_res.fetchall()
        data = []
        for value in raw_data:
            clean_value = str(value).split(",")[0][1:].replace('"','').replace("'","")
            if clean_value not in data:
                data.append(clean_value)
                #print (clean_table_name)
        return data
    except:
        print(query + " Doesn't work!")
        return []



def check_for_searched_values(searched_values):
    for searched_value in searched_values:
        counter = 0
        for table in tables:
            counter += 1
            print(str(counter) +"/" +str(len(tables)) )
            for column in db_dictionary[table]:
                if ((column not in columns_to_not_consider) & ('Date' not in str(column))):
                    column_data = get_column_data_from_db(table,column)
                    if searched_value in column_data:
                        print(searched_value + ' IS IN COLUMN ' +column+ ' IN THE TABLE ' + table +' ************************************')
                    #print(column_data)

check_for_searched_values(searched_values)
print("Finished...")
