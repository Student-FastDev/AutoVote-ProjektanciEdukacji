# AutoVote-ProjektanciEdukacji

**AutoVote-ProjektanciEdukacji** is a Python-based bot designed to automate the voting process on the ProjektanciEdukacji website. Utilizing the Requests library, it generates random user details, submits votes through POST requests, and handles vote confirmations via the secmail library.

## Features

- **Automated Voting:** Automatically submit votes using generated random user details.
- **Email Confirmation:** Handle confirmation emails with the secmail library to verify votes.
- **Multithreading Support:** Run multiple threads simultaneously for efficient voting.
- **Proxy Support:** Optionally use proxies to mask voting origins and enhance anonymity.

## Prerequisites

To run the AutoVote-ProjektanciEdukacji script, ensure you have the following installed:

- **Python:** Version 3.6 or higher.
- **Git:** For cloning the repository.

## Installation

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/Student-FastDev/AutoVote-ProjektanciEdukacji
    cd AutoVote-ProjektanciEdukacji
    ```

2. **Install Required Packages:**

    Install the necessary Python packages using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Python Script:**

    Execute the main script to start the voting process:

    ```bash
    python main.py
    ```

2. **Configure Settings:**

    After running the program for the first time, a `settings.json` file will be generated. Open this file in a text editor to customize your settings:

    ```json
    {
        "iterations": 100, 
        "link": "https://projektanciedukacji.pl/api/vote-email/[PROJECT_ID]",
        "threads": 5,
        "use_proxy": false,
        "proxy_file": "proxies.txt"
    }
    ```

    - **iterations:** The number of votes to submit.
    - **link:** The API endpoint for voting. Replace `[PROJECT_ID]` with the actual project ID.
    - **threads:** Number of threads to run simultaneously.
    - **use_proxy:** Set to `true` to enable proxy usage.
    - **proxy_file:** Path to the file containing proxy addresses.

## Notes

- **API Endpoint:** Ensure the `link` in `settings.json` is correct and points to the appropriate voting API.
- **Proxy Configuration:** If using proxies, populate the `proxies.txt` file with valid proxy addresses, one per line.
- **Email Handling:** The secmail library is used to manage confirmation emails. Ensure that the email service is properly configured.

---

<div align="center">  
<img src="https://i.imgur.com/EHiOHX8.png" alt="Projektanci Logo" width="50px">
</div>
