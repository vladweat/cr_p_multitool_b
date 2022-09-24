import os
from time import sleep
from turtle import position
import telebot
import secrets
from telebot.types import *
from eth_account import Account
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("API_TOKEN"))

## TODO добавить проверку переменных, установить ограничения на число кошельков, удаление файла


def start_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    hello = KeyboardButton(text="Hello")
    generator = KeyboardButton(text="Generator")
    keyboard.add(hello, generator)
    return keyboard


@bot.message_handler(commands=["start"])
def message_handler(message):
    bot.send_message(
        message.chat.id, "Hello, this is start page", reply_markup=start_keyboard()
    )


@bot.message_handler(content_types=["text"])
def start(message):
    if message.text == "Generator":
        bot.send_message(
            message.from_user.id,
            "Введите необходимое число кошельков (до 1000) \nP.S. Это может занять некоторое время",
        )

        bot.register_next_step_handler(message, get_wallets)

    if message.text == "Hello":
        bot.send_message(message.chat.id, "Дарова")


def get_wallets(message):

    global num_of_wallets
    num_of_wallets = message.text
    wallet_file_name = create_wallets(message, int(num_of_wallets))

    doc = open(f"{wallet_file_name}", "rb")

    bot.send_message(message.from_user.id, "Спасибо за ожидание")
    bot.send_document(message.from_user.id, doc)
    

def create_wallets(message, num_of_wallets): 

    now = datetime.now().strftime("%d-%m-%Y %H-%M")
    wallet_file_name = f"multitool_b/wallets/wallets {message.from_user.id} {now}.txt"

    for _ in range(int(num_of_wallets)):

        private_key = "0x" + secrets.token_hex(32)
        account = Account.from_key(private_key)

        with open(f"{wallet_file_name}", "a+") as file:
            file.write(f"{account.address} {private_key} \n")

    sleep(5)
    return wallet_file_name


if __name__ == "__main__":
    bot.infinity_polling()
