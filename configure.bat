@echo off
setlocal

REM Проверка наличия Python 3
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python 3 не установлен. Устанавливаю...
    REM Установка Python 3 (предполагается, что Chocolatey установлен)
    choco install python --version=3.9.0 -y
    echo Python 3 успешно установлен.
) else (
    echo Python 3 уже установлен.
)

REM Создание виртуального окружения
python -m venv .venv

REM Активация виртуального окружения
call .venv\Scripts\activate.bat

echo Виртуальное окружение активно: %VIRTUAL_ENV%

REM Проверка наличия файла requirements.txt
if exist "requirements.txt" (
    echo Устанавливаю библиотеки из requirements.txt...
    pip install -r requirements.txt
    echo Библиотеки успешно установлены.

    REM Проверка наличия файла .env
    if not exist ".env" (
        echo Создание файла .env...
        echo введите имя пользователя postgres
        set /p name=
        echo введите пароль пользователя:
        set /p password=
        echo введите ip-адрес сервера postgres:
        set /p ipserver=
        echo введите порт подключения postgres:
        set /p portserver=
        echo введите название базы данных postgres:
        set /p namedatabase=

        echo USER_NAME=%name% > .env
        echo PASSWORD=%password% >> .env
        echo IP_ADDRESS=%ipserver% >> .env
        echo PORT=%portserver% >> .env
        echo NAME_DATABASE=%namedatabase% >> .env
    ) else (
        echo Файл .env уже существует. Все прошло успешно, можно запускать файл.
    )
) else (
    echo Файл requirements.txt не найден.
)

endlocal