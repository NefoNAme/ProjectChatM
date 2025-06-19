#!/bin/bash


if command -v python3 &>/dev/null; then
    echo "Python 3 уже установлен."
else
    echo "Python 3 не установлен. Устанавливаю..."
    sudo apt update
    sudo apt install -y python3 python3-pip
    echo "Python 3 успешно установлен."
fi
python3 -m venv ./.venv
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Виртуальное окружение активно: $VIRTUAL_ENV"
    if [[ -f "requirements.txt" ]]; then
        echo "Устанавливаю библиотеки из requirements.txt..."
        pip install -r requirements.txt
        echo "Библиотеки успешно установлены."
        if [[! -f ".env"]]; then
            touch .env
            read -p "введите имя пользователя postgres" name
            read -p "введите пароль пользователя:  " password
            read -p "введите ip-фдрес сервера postgres" ipserver
            read -p "введите порт подключения postgres" portserver
            read -p "введите название базы данных postgres" namedatabase

            echo "USER_NAME=$name"> .env
            echo "PASSWORD=$password">> .env
            echo "IP_ADDRESS=$ipserver">> .env
            echo "PORT=$portserver">> .env
            echo "NAME_DATABASE=$name">> .env
        else
        echo "все прошло успешно можно запускать файл"
        fi

    else
        echo "Файл requirements.txt не найден."
    fi

else
    echo "Виртуальное окружение не активно."
fi

