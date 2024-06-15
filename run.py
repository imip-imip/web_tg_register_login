from models import create_table
import threading
from telegram_bot import telegram_bot
from routes import *

if __name__ == '__main__':
    create_table()
    threading.Thread(target=telegram_bot).start()
    app.run(port=8000, debug=True)
