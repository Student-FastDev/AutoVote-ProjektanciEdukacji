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

# Define settings
DEFAULT_SETTINGS = {
    "iterations": 100,
    "link": "https://projektanciedukacji.pl/api/vote-email/[PROJECT_ID]",
    "threads": 5
}

# Function to load settings from a JSON file
def load_settings():
    # Check if settings file exists
    if not isfile('settings.json'):
        # If not, create one with default settings
        with open('settings.json', 'w') as settings_file:
            json.dump(DEFAULT_SETTINGS, settings_file, indent=4)
    # Open the settings file and load the settings
    with open('settings.json', 'r') as settings_file:
        settings = json.load(settings_file)
    # Return the settings
    return settings

# Function to generate a person's details
def generate_person():
    # Randomly select a gender
    gender = 'M' if random.randint(1,2) == 1 else 'F'
    # Based on the gender, select the appropriate names list
    list_first_names = data_names.FIRST_NAMES_M if gender == 'M' else data_names.FIRST_NAMES_F
    list_second_names = data_names.LAST_NAMES_M if gender == 'M' else data_names.LAST_NAMES_F
    # Select a random name and surname from the list
    name = choice(list_first_names)
    surname = choice(list_second_names)
    # Return the selected name and surname
    return name, surname

# Function to send a post request
def send_post_request(name, surname, email, phone, select, link):
    # Define the payload
    payload = {
        'name': name,
        'surname': surname,
        'email': email,
        'phone': phone,
        'select': select
    }
    # Send the post request
    requests.post(link, json=payload)

# Function to confirm the request
def confirm_request(client, email):
    # Wait for a new message
    messageWait = client.await_new_message(email)
    # Get the message
    message = client.get_message(address=email, message_id=messageWait.id)
    # Get the confirmation link from the message
    confirmLink = requests.get(re.search("(?<=<a href=\")(.*?)(?=\")", message.html_body).group(0), allow_redirects=False)
    # Send a post request to the confirmation link
    requests.post(confirmLink.headers['Location'])

# Function to append an email to a JSON file
def append_email_to_file(email, email_domain, file_path='emails.json'):
    try:
        with open(file_path, 'r') as json_file:
            listObj = json.load(json_file)
    except json.JSONDecodeError:
        # Handle JSON decode error
        listObj = []
    except FileNotFoundError:
        # Handle file not found error
        listObj = []

    listObj.append(email + email_domain)

    with open(file_path, 'w') as json_file:
        json.dump(listObj, json_file, indent=4, separators=(',', ': '))

# Function to generate an random combination of an email
def generate_email(name, surname):
    # Generate a random amount of letters from the surname
    surname_length = random.randint(3, len(surname))
    # Randomly select a separator
    separator = random.choice(['', '.', '_', ''])
    # Randomly select the digits
    digits = random.choice(['', str(random.randint(1, 100)), str(random.randint(100, 1000)), str(random.randint(1000, 10000))])
    # Construct the email
    email = name.lower() + separator + surname[:surname_length].lower() + digits
    return email

# Main function
def main(i, settings):
    # Initialize the client
    client = secmail.Client()
    # Generate a person's details
    name, surname = generate_person()
    # Generate a random phone number
    phone = random.randint(100000000,999999999)
    # Generate an random email
    email = generate_email(name, surname)
    select = "Przyjaciel projektu"
    # List of email domains
    email_domains = [
        "@ezztt.com",
        "@icznn.com",
        "@vjuum.com",
        "@laafd.com",
        "@txcct.com"
    ]
    # Select a random email domain
    email_domain = choice(email_domains)
    # Send a post request
    send_post_request(name, surname, email + email_domain, phone, select, settings['link'])
    # Confirm the request
    confirm_request(client, email + email_domain)
    # Append the email to the JSON file
    append_email_to_file(email, email_domain, 'emails.json')

# Run the main function in a loop
if __name__ == "__main__":
    # Load settings
    settings = load_settings()
    # Loop the main function
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings['threads']) as executor:
        # Create a progress bar
        with tqdm(total=settings['iterations']) as pbar:
            # Submit tasks to executor
            futures = {executor.submit(main, i, settings) for i in range(1, settings['iterations'] + 1)}
            for future in as_completed(futures):
                # Update the progress bar
                pbar.update()
