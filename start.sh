#!/bin/bash

if [[ "$VIRTUAL_ENV" == "" ]]; then
    source ./.venv/bin/activate
fi



if [[ -f ".env" ]]; then

    set -a
    source .env
    set +a
    if [[ -z "$USER_NAME" || -z "$PASSWORD" || -z "$IP_ADDRESS" || -z "$PORT" || -z "$NAME_DATABASE" ]]; then
        echo "Ошибка: одна или несколько переменных окружения не установлены."
        [[ -z "$USER_NAME" ]] && echo "Переменная USER_NAME не установлена."
        [[ -z "$PASSWORD" ]] && echo "Переменная PASSWORD не установлена."
        [[ -z "$IP_ADDRESS" ]] && echo "Переменная IP_ADDRESS не установлена."
        [[ -z "$PORT" ]] && echo "Переменная PORT не установлена."
        [[ -z "$NAME_DATABASE" ]] && echo "Переменная NAME_DATABASE не установлена."
        exit 1
    fi
    python3 ./app/app.py "$IP_ADDRESS" "$NAME_DATABASE" "$USER_NAME" "$PASSWORD" "$PORT"
else 
    echo "Ошибка: файл .env не найден."
fi


