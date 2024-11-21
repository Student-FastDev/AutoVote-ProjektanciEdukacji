# AutoVote-ProjektanciEdukacji

AutoVote bot for ProjektanciEdukacji made with Python and Requests.

## Table of Contents
- [Questions](#questions)
  - [How this works?](#how-this-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Python File](#running-the-python-file)

## Questions

### How this works?

The bot automates the voting process on the ProjektanciEdukacji website using Python and the Requests library. It generates random person details, submits votes through a POST request, and confirms votes by handling confirmation emails using the secmail library.

## Getting Started

This section will guide you through setting up and running the project locally.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python
- Git

### Installation

1. Clone this repository to your local machine using Git:

```plain
git clone https://github.com/Student-FastDev/AutoVote-ProjektanciEdukacji
```

2. Change to the project directory:

```plain
cd (path to AutoVote-ProjektanciEdukacji)
```

3. Install the required Python packages using pip and the requirements.txt file:

```plain
pip install -r requirements.txt
```

## Usage

### Running the Python File

To run the Python file, use the following command while being in the repository folder:

```bash
python main.py
```

Edit the settings by opening the settings.json (will appear after running the program for the first time) in some text editor.

```plain
{
    "iterations": 100, <- The number of iterations to run the program.
    "link": "https://projektanciedukacji.pl/api/vote-email/[PROJECT_ID]" <- Link to the website api.
    "threads": 5, <- The number of threads working simultaneously.
    "use_proxy": False, <- Use of proxy.
    "proxy_file": "proxies.txt" <- The file where are proxies.
}
```
