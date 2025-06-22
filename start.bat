@echo off
setlocal

REM Проверка активации виртуального окружения
if not defined VIRTUAL_ENV (
    call .venv\Scripts\activate.bat
)

REM Проверка наличия файла .env
if exist ".env" (
    REM Установка переменных окружения из .env
    for /f "usebackq tokens=1,2 delims==" %%a in (.env) do (
        set %%a=%%b
    )

    REM Проверка наличия необходимых переменных окружения
    if not defined USER_NAME (
        echo Ошибка: переменная USER_NAME не установлена.
        exit /b 1
    )
    if not defined PASSWORD (
        echo Ошибка: переменная PASSWORD не установлена.
        exit /b 1
    )
    if not defined IP_ADDRESS (
        echo Ошибка: переменная IP_ADDRESS не установлена.
        exit /b 1
    )
    if not defined PORT (
        echo Ошибка: переменная PORT не установлена.
        exit /b 1
    )
    if not defined NAME_DATABASE (
        echo Ошибка: переменная NAME_DATABASE не установлена.
        exit /b 1
    )

    REM Запуск приложения с параметрами
    python ./app/app.py "%IP_ADDRESS%" "%NAME_DATABASE%" "%USER_NAME%" "%PASSWORD%" "%PORT%"
) else (
    echo Ошибка: файл .env не найден.
)

endlocal