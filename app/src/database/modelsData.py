import psycopg2
from psycopg2 import sql
from src.database.method_database import createDatabaseIfNotExists,  get_data_fromTable, insert_dataInTable, delete_data_fromTable




class UserData:
    def __init__(self, host, database, user, password,port):
        try:
            self.connect = psycopg2.connect(host=host, database=database, user=user, password=password,port=port)
        except psycopg2.errors.InvalidCatalogName:
            self.connect = psycopg2.connect(host=host,  user=user, password=password,port=port)
            createDatabaseIfNotExists(self.connect, database )
            self.connect = psycopg2.connect(host=host, database=database, user=user, password=password,port=port)

        self._createEnsureTable()
        self.table = "UserData"

    def addUser(self, loginname, password):
        try:
            insert_dataInTable(self.connect, self.table, Loginname=loginname, Password=password)
            self.connect.commit()
            return True
        except psycopg2.errors.UniqueViolation:
            self.connect.rollback()
            return False

    def getUser(self, loginname,password):
        try:
            with self.connect.cursor() as cur:
                cur.execute("SELECT user_id, Loginname, Password FROM UserData WHERE Loginname = %s AND Password = %s", (loginname,password))
                result = cur.fetchone()
                if result:
                    return {"user_id": result[0],"Loginname": result[1], "Password": result[2]}
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def getUserNameById(self,user_id):
        try:
            with self.connect.cursor() as cur:
                cur.execute("SELECT Loginname FROM UserData WHERE Loginname = %s", (user_id))
                result = cur.fetchone()
                if result:
                    return {"Loginname": result[0]}
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def getUsersByUsername(self, loginname):
        try:
            with self.connect.cursor() as cur:
                cur.execute("SELECT Loginname FROM UserData WHERE Loginname = %s", (loginname))
                result = cur.fetchall()
                if result:
                    return {"Loginname": result[0]}
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback()         

    def deleteUserBy(self, loginname):
        try:
            userId = get_data_fromTable(self.connect, self.table, loginname, "Loginname", "user_id")
            delete_data_fromTable(self.connect, self.table, userId)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    
    def _createEnsureTable(self):
        try:
                
            with self.connect.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS UserData  (
                        user_id SERIAL PRIMARY KEY,
                        Loginname VARCHAR(255) UNIQUE NOT NULL,
                        Password VARCHAR(255) NOT NULL,
                        registedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 



class ChatDatabase:
    def __init__(self, host, database, user, password,port):
        self.connect = psycopg2.connect(host=host, database=database, user=user, password=password,port=port)

        self.table = "ChatData"
        self._createEnsureTable()

    def _createEnsureTable(self):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS ChatData (
                        chat_id SERIAL PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        created_at TIMESTAMP NOT NULL
                    )
                    """
                )
                self.connect.commit()

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def addChat(self, nameChat, create_at):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    f"INSERT INTO {self.table} (name, created_at) VALUES (%s, %s) ON CONFLICT (name) DO NOTHING",
                    (nameChat, create_at)
                )
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 

    def getChatName(self, id_chat ):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("SELECT name, created_at FROM ChatData WHERE chat_id = %s", (id_chat,))
                result = cur.fetchone()
                if result:
                    return {"name": result[0], "created_at": result[1]}
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def getAllChats(self):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("SELECT chat_id, name, created_at FROM ChatData;")
                return cur.fetchall() 
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def deleteChat(self, loginname):
        try:
                
            with self.connect.cursor() as cursor:
                cursor.execute("DELETE FROM ChatData WHERE name = %s", (loginname,))
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 



class MessageData:
    def __init__(self, host, database, user, password,port):
        self.connect = psycopg2.connect(host=host, database=database, user=user, password=password,port=port)
        self._createEnsureTable()
       

    def addMessage(self, user_id,date_message, chat_id,messageText):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO MessageData (user_id, createMessage, chat_id, textMessage ) VALUES (%s,%s, %s, %s)",
                    (user_id,date_message, chat_id,messageText)
                )
                self.connect.commit()
                print(f"Сообщение '{messageText}', от пользователя {user_id}, в чат {chat_id} добавлено в БД.")
            return True
        except psycopg2.errors.UniqueViolation:
            self.connect.rollback()
            return False


    
    def getMessages(self, chat_id,field):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute(f"SELECT * FROM MessageData WHERE {field} = %s", (chat_id,))
                result = cur.fetchall()
                if result:
                    return result
                return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 


    def deleteMessage(self, message_id):
        try:
                
            with self.connect.cursor() as cursor:
                cursor.execute("DELETE FROM MessageData WHERE MessageId = %s", (message_id,))
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 

    def getMessageWithUsernameById(self,message_id):
        try:
            with self.connect.cursor() as cursor:
                cursor.execute("""
                         SELECT u.user_id, u.Loginname
                    FROM UserData u
                    JOIN MessageData m ON u.id = m.chat_id
                    WHERE m.user_id = %s;

                    """,message_id)
                
                result = cursor.fetchall()
                if result:
                    return result
                return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 


    def _createEnsureTable(self):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS MessageData (
                    MessageId SERIAL PRIMARY KEY,
                    createMessage TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER REFERENCES UserData(user_id) ON DELETE CASCADE,
                    chat_id INTEGER REFERENCES ChatData(chat_id) ON DELETE CASCADE,
                    textMessage TEXT,
                    fileData BYTEA,
                    CHECK (textMessage IS NOT NULL OR fileData IS NOT NULL) 
                            )
                """)
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 

class UsersChatData:
    def __init__(self, host, database, user, password,port):
        self.connect = psycopg2.connect(host=host, database=database, user=user, password=password,port=port)
 
       
        self._createEnsureTable()

    # Добавить пользователя в чат
    def addUserToChat(self, chat_id, user_id):
        try:
            with self.connect.cursor() as cur:
                cur.execute(
                    f"INSERT INTO user_chat (chat_id, user_id) VALUES (%s, %s) ON CONFLICT (chat_id, user_id) DO NOTHING;",
                    (chat_id, user_id)
                )
                print("добавили пользователя в чат!!")
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback()
    # Убрать пользователя из чата
    def removeUserFromChat(self, user_id, chat_id):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("DELETE FROM user_chat WHERE user_id = %s AND chat_id = %s;", (user_id, chat_id))
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def getAllChat(self):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute(f"SELECT  ")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 

    def getChatsForUser(self, user_id):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute(
                    """
                    SELECT c.chat_id, c.chat_name
                    FROM ChatData c
                    JOIN user_chat uc ON c.id = uc.chat_id
                    WHERE uc.user_id = %s;
                    """, (user_id,)
                )
                return cur.fetchall()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 
    def getUsersInChat(self, chat_id):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("""
                    SELECT u.user_id, u.Loginname
                    FROM UserData u
                    JOIN user_chat uc ON u.user_id = uc.user_id
                    WHERE uc.chat_id = %s;
                """, (chat_id,))
                result = cur.fetchall()
                if result:
                    return result
                return []
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback()
            return []     

    def isUserInChat(self, user_id,chat_id) -> bool:
        try:
                
            with self.connect.cursor() as cur:
                cur.execute(f"SELECT user_id FROM {self.titleTable} WHERE user_id = %s AND chat_id = %s",(user_id,chat_id))
                result = cur.fetchone()
                if result :
                    return True
                return False
                
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 


    def getAllUserChatRelationships(self):
        try:
                
            with self.connect.cursor() as cur:
                cur.execute("""
                    SELECT uc.user_id, uc.chat_id
                    FROM user_chat uc;
                """)
                return cur.fetchall()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback() 

    def _createEnsureTable(self):
        try: 
                
            with self.connect.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS user_chat (
                        user_id INTEGER REFERENCES UserData(user_id) ON DELETE CASCADE,
                        chat_id INTEGER REFERENCES ChatData(chat_id) ON DELETE CASCADE,
                        PRIMARY KEY (user_id, chat_id)
                    );
                """)
                self.connect.commit()
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            self.connect.rollback()     