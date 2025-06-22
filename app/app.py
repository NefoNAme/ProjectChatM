from datetime import datetime
from itertools import zip_longest
from flask import Flask, jsonify, render_template, request, redirect, url_for, session, flash
from src.database.modelsData import UserData, ChatDatabase, MessageData, UsersChatData
import sys


app = Flask(__name__)
app.secret_key = 'your_secret_key'  

if len(sys.argv) < 6:
    print("""недостаточно параметров для работы файла \n 
          \n
          
           введите ip адрес postger (например 127.0.0.1)\n
           введите название базы данных (например Mydatabase)\n
           введите пользователя базы данных (например postgres )\n
           введите пароль пользователя (например password)\n\n
          И введите порт. К примеру 5432 стандартный порт для postgres\n\n

          Главное все вводить в том порядке которой я показал.\n\n\n\n
            Кроме того, для того чтобы быстро запустить файл не вводя много параметров 
          я сделал скрипт который Который делает подключение к серверу с параметрами по умолчанию .Он называется : \n\n\n

          \t|---------------------------------|
          \t|                                 |
          \t|         название файла          |
          \t|                                 |
          \t|---------------------------------|
          \n\n\n\n
           Если все правильно то у вас запуститься программа, а сейчас она покидает вас

          
          
          
           """)
    exit()


user_data = UserData(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

chat_data = ChatDatabase(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

message_data = MessageData(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])

users_chat_data = UsersChatData(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])


@app.route('/')
def root():
    return render_template('root.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        loginname = request.form['loginname']
        password = request.form['password']
        if user_data.addUser(loginname, password):
            flash('Регистрация прошла успешно!')
            return redirect(url_for('login'))
        flash('Ошибка: пользователь с таким именем уже существует.')
    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    wrongMess = ''
    if request.method == 'POST':
        loginname = request.form['loginname']
        password = request.form['password']
        user = user_data.getUser(loginname,password) 
        if user:
            session['user_id'] = user["user_id"]  
            flash('Вы успешно вошли в систему!')
            return redirect(url_for('mainpage'))
        wrongMess = 'Ошибка: неверное имя пользователя или пароль.'
        flash(wrongMess)
       
    return render_template('login.html',wrongMess=wrongMess)

@app.route('/logout')
def logout():
    session.pop('user_id', None)  
    flash('Вы вышли из системы.')
    return redirect(url_for('root'))

@app.route('/mainpage')
def mainpage():
    chats = chat_data.getAllChats()
     
    
    return render_template('main.html', chats=chats)


@app.route('/create_chat', methods=['POST'])
def create_chat():
    chat_name = request.form.get('chat_name')
    if chat_name:
        chat_data.addChat(chat_name, datetime.now()) 
        flash('Чат успешно создан!')
    else:
        flash('Введите имя чата!')
    return redirect(url_for('mainpage'))

@app.route('/join_chat/<int:chat_id>', methods=['POST'])
def join_chat(chat_id):
    user_id = session.get('user_id')  
    if user_id:
        users_chat_data.addUserToChat(chat_id, user_id) 
        
        flash('Вы присоединились к чату!')
    else:
        flash('Не удалось присоединиться к чату!')
    return redirect(url_for('chat', chat_id=chat_id))

@app.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    message_text = None


    if request.method == 'POST':
        
        user_id = session.get('user_id')
        print(f"ID user :{user_id}")
        message_text = request.form.get('message_text')
        print(f"message : {message_text}")
        if user_id and message_text:
            message_data.addMessage(user_id,datetime.now(), chat_id, message_text) 
            flash('Сообщение отправлено!')
        else:
            flash('Не удалось отправить сообщение!')

   
    messages = message_data.getMessages(chat_id, 'chat_id')
    
    users = users_chat_data.getUsersInChat(chat_id) 
    combined  = zip_longest(users,messages) #полная лажа
    print("users:", users)  

    return render_template('chat.html', chat_id=chat_id,
                           chatName=chat_data.getChatName(chat_id)["name"]
                           , messages=messages, users=users,combined = combined)


@app.route('/chat/<int:chat_id>/messages', methods=['GET'])
def get_messages(chat_id):
    messages = message_data.getMessages(chat_id,'chat_id')
    return jsonify(messages) 
    



if __name__ == '__main__':
    app.run(debug=True)