from psycopg2 import sql



def insert_dataInTable(conn,table,**kargs):
    column = ', '.join(kargs.keys())
    values = ', '.join(['%s'] * len(kargs))
    try:
        with conn.cursor() as cur:
            cur.execute(f"INSERT INTO { table} ({column}) VALUES ({values})",tuple(kargs.values()))
            conn.commit()
    except Exception as ex:
        print(f"Ощибка при добавлении в таблицу{table} ошибка\n {ex}")

def createDatabaseIfNotExists(conn,database):
    
    try:   

        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(database)))
        conn.commit()
        print(f"База данных '{database}' успешно создана.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback() 

   
    
def get_data_fromTable(conn,table:str,keyword:str,keyfield:str,*field:str):
    column = ', '.join(field)
    try:
        with conn.cursor() as cur:
            cur.execute(f"SELECT {column} FROM {table} WHERE {keyfield} = %s",keyword)
            return cur.fetchone()
        
    except Exception as ex:
        print(f"Ошибка при получении из полей {column} с таблицы {table} ошибка\n {ex}")    



def delete_data_fromTable(conn,table,record_id):

    with conn.cursor() as cur:
        cur.execute(f"DELETE FROM {table} WHERE id = %s", (record_id,))
        conn.commit()


def update_data_onTable(conn,table:str,record_id,newWord,keyField):
     with conn.cursor() as cur:
        cur.execute(f"UPDATE {table} SET {keyField} = %s WHERE id = %s", (newWord,record_id,))
        conn.commit()

