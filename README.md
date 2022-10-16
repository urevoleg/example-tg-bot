# example-tg-bot

0. Клонировать репо
1. Перейти в него `cd example-tg-bot`
2. Создать venv `python3 -m venv venv` и активировать `source venv/bin/activate` (linux)
3. Установить пакеты `python -m pip -r -requirements.txt`
4. Создать файл `.env` и записать в него telegram token `TG_TOKEN=token`
5. Запускаем `pythno bot.py`

Бот скачивает записанное аудио в папку `src`, вычисляет громкость и выдает простое сообщение:

```text
        if loudness < -28:
            update.message.reply_text(f"Loudness is : {loudness:.1f}. Your voice is quite!")
        else:
            update.message.reply_text(f"Loudness is : {loudness:.1f}. Your voice is good!")
```

Громкость вашего аудио такая-то и говорили ли вы тихо или громко.