# 🃏 Блэкджек — Discord бот

Бот для игры в 21 (Blackjack) с дилером. Только ты видишь свои карты.

## Команды
- `/bj` — начать игру
- `/hit` — взять карту
- `/stand` — остановиться

## Установка
1. Установи Python 3.12+
2. Установи библиотеки: `pip install -r requirements.txt`
3. Создай файл `.env` и добавь `DISCORD_TOKEN=твой_токен`
4. Запусти: `python main.py`

## Технологии
- Python 3.13
- discord.py 2.7.1
- python-dotenv

## Структура
- `main.py` — команды и запуск
- `blackjack.py` — логика игры
- `config.py` — настройки
- `.env` — токен (не заливать)
- `requirements.txt` — библиотеки