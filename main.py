import telebot


app = telebot.TeleBot("1847942519:AAHomWiXhsQlh8Wkq2kkSgs5G54I5pgVWKs")

from message_handlers import *
from callback_query import *

if __name__ == "__main__":
    app.polling()