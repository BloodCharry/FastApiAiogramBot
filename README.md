# CheckPointPythonBackend
    Инструкиция запуска Телеграм бота
    1. Установите все зависимости согласно -> requirements.txt
    2. В корневом каталоге находится исполняемый файл ngrok.exe, который предоставляет безопасный туннель от интернета к локальному серверу.Он служит для предоставления доступа к локальному веб-серверу и API, это на первое время для тестов.

    Для запуска ngrok нужно зарегестрироваться на dashboard.ngrok.com используя VPN, и пройти аутификацю.
    Далее переходит в каталог с исполняемым файлом спомощью командной строки и набираем команду:
        ngrok.exe http 8000

    Тем самым создав, тунель. В строке Forwarding копируем ссылку которую создал ngrok( до стрелочки ->) и вносим изменения в .env->NGROK_TUNNEL_URL. (При каждом запуске ngrok url меняется)

    основной запуск бота осуществляем из каталога CheckPointPythonBackend (uvicorn будет ругаться, если осуществим запуск из telegram_bot)
    Команда:    python -m uvicorn telegram_bot.app:app --reload


