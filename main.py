import requests
import data_names
import random
from random import choice
import secmail
import asyncio
import re
import json
from os import path
from clear_screen import clear
import time
from os.path import isfile
import concurrent.futures
from concurrent.futures import as_completed
from tqdm import tqdm
import os

DEFAULT_SETTINGS = {
    "iterations": 100,
    "link": "https://projektanciedukacji.pl/api/vote-email/[PROJECT_ID]",
    "threads": 5,
    "use_proxy": False,
    "proxy_file": "proxies.txt"
}

def load_settings():
    if not isfile('settings.json'):
        with open('settings.json', 'w') as settings_file:
            json.dump(DEFAULT_SETTINGS, settings_file, indent=4)
        clear()
        print("Settings file created. Please update the settings and run the program again.")
        os._exit(1)
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
    if settings["use_proxy"] and not isfile(settings["proxy_file"]):
        with open(settings["proxy_file"], 'w') as proxy_file:
            proxy_file.write("DEFAULT_PROXY")
        clear()
        print("Proxy file created. Please update the proxies and run the program again.")
        os._exit(1)
    return settings
    
def load_proxies(file_path):
    with open(file_path, 'r') as proxy_file:
        proxies = proxy_file.readlines()
    return proxies
    
def generate_person():
    gender = 'M' if random.randint(1,2) == 1 else 'F'
    list_first_names = data_names.FIRST_NAMES_M if gender == 'M' else data_names.FIRST_NAMES_F
    list_second_names = data_names.LAST_NAMES_M if gender == 'M' else data_names.LAST_NAMES_F
    name = choice(list_first_names)
    surname = choice(list_second_names)
    return name, surname
    
def send_post_request(name, surname, email, phone, select, link, proxy=None):
    payload = {
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'select': select
    }
    try:
        response = requests.post(link, json=payload, proxies={"http": proxy, "https": proxy}) if proxy else requests.post(link, json=payload)
        if response.status_code != 200:
            clear()
            print(f"Error! Received status code {response.status_code} from the server. Check the link!")
            os._exit(1)
    except requests.exceptions.RequestException as e:
        clear()
        print(f"Error! An error occurred while sending the post request. Check proxies!")
        os._exit(1)
    return response
    
def confirm_request(client, email, proxy=None):
    messageWait = client.await_new_message(email)
    message = client.get_message(address=email, message_id=messageWait.id)
    confirmLink = requests.get(re.search("(?<=<a href=\")(.*?)(?=\")", message.html_body).group(0), allow_redirects=False, proxies={"http": proxy, "https": proxy} if proxy else None)
    response = requests.post(confirmLink.headers['Location'], proxies={"http": proxy, "https": proxy} if proxy else None)
    while response.status_code != 200:
        time.sleep(1)
        response = requests.post(confirmLink.headers['Location'], proxies={"http": proxy, "https": proxy} if proxy else None)
        
def append_email_to_file(email, email_domain, file_path='emails.json'):
    try:
        with open(file_path, 'r') as json_file:
            listObj = json.load(json_file)
    except json.JSONDecodeError:
        listObj = []
    except FileNotFoundError:
        listObj = []

    listObj.append(email + email_domain)

    with open(file_path, 'w') as json_file:
        json.dump(listObj, json_file, indent=4, separators=(',', ': '))
        
def generate_email(name, surname):
    surname_length = random.randint(3, len(surname))
    separator = random.choice(['', '.', '_', ''])
    digits = random.choice(['', str(random.randint(1, 100)), str(random.randint(100, 1000)), str(random.randint(1000, 10000))])
    email = name.lower() + separator + surname[:surname_length].lower() + digits
    return email
    
def main(i, settings):
    client = secmail.Client()
    name, surname = generate_person()
    phone = random.randint(100000000,999999999)
    email = generate_email(name, surname)
    select = "Przyjaciel projektu"
    email_domains = [
        "@ezztt.com",
        "@icznn.com",
        "@vjuum.com",
        "@laafd.com",
        "@txcct.com"
    ]
    email_domain = choice(email_domains)
    proxy = None
    if settings["use_proxy"]:
        proxies = load_proxies(settings["proxy_file"])
        proxy = random.choice(proxies).strip()
    send_post_request(name, surname, email + email_domain, phone, select, settings['link'], proxy)
    confirm_request(client, email + email_domain, proxy)
    append_email_to_file(email, email_domain, 'emails.json')
    
if __name__ == "__main__":
    settings = load_settings()
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings['threads']) as executor:
        with tqdm(total=settings['iterations']) as pbar:
            futures = {executor.submit(main, i, settings) for i in range(1, settings['iterations'] + 1)}
            for future in as_completed(futures):
                pbar.update()
    clear()
    print("Finished!")
