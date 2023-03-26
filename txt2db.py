import pandas as pd
import os, sqlite3
from tqdm import tqdm
import json


# Create sqlite database and table
def createDB(db_save_path, table_name, header_name):
    conn = sqlite3.connect(db_save_path)
    cursor = conn.cursor()

    # Add all column names to the table
    name_list = ''
    for i in header_name:
        name_list = name_list + ', ' + i + ' INTEGER'
    try:
        cursor.execute(f'CREATE TABLE {table_name} (id INTEGER PRIMARY KEY{name_list})')
        conn.commit()
    except Exception as e:
        print("Create table error : %s" % e)
    
    cursor.close()
    conn.close()
    return None


# List all TXT files in dir
def iterTXT(txt_dir):
    def checkTXT(file_name):
        if file_name.rsplit('.')[1] == 'TXT':
            return txt_dir + '/' + file_name
        else:
            return None
    return list(filter(None, list(map(checkTXT, os.listdir(txt_dir)))))


# Extract content from TXT to csv
def extractTXT2DB(txt_file_path, header_name, db_save_path, table_name):
    df = pd.read_csv(txt_file_path, sep = '\s+', header = None, names = header_name)
    df_list = df.values.tolist()

    # Write into the sqlite database
    conn = sqlite3.connect(db_save_path)
    cursor = conn.cursor()

    for i in list(map(tuple, df_list)):
        insert_query = f'INSERT INTO {table_name} {tuple(header_name)} VALUES {i}'
        try:
            cursor.execute(insert_query)
        except Exception as e:
            print("Execution error: %s" % e)

    conn.commit() # Commit after all execution finished
    cursor.close()
    conn.close()
    
    return None

# Execute 1 feature
def executeSingleFeature(db_save_path, table_name, header_name, txt_dir):
    # Create database and table
    createDB(db_save_path, table_name , header_name)
    # Execute SQL query
    for i in tqdm(iterTXT(txt_dir)):
        try:
            extractTXT2DB(i, header_name, db_save_path, table_name)
        except Exception as e0:
            print(e0)
            print(i)
            continue
                
    return None


def main():
    with open("header.json", "r") as f:
        header_dict = json.load(f)

    for i in [
              'SSD', 'TEM', 
              'GST', 'PRS', 
              'WIN', 'RHU', 
              'PRE', 'EVP'
              ]:
        db_save_path = 'weather.db'
        header_name = header_dict[i]
        txt_dir = 'datasets/' + i
        print("Executing %s" % i)
        executeSingleFeature(db_save_path, i, header_name, txt_dir)

    return None

if __name__ == "__main__":
    main()
