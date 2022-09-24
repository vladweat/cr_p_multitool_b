from datetime import datetime

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