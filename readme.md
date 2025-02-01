# Daily Recipe Bot

This repository contains a Python script and GitHub Actions workflow to automatically generate a daily recipe from a randomly chosen country and send it to your email inbox.

## Description

The Daily Recipe Bot uses the Gemini AI API to discover new recipes from around the world.  Every day, a GitHub Actions workflow runs this bot, which does the following:

1.  **Randomly selects a country** from a predefined list.
2.  **Uses the Gemini AI API** to generate a recipe for a dish from that country.
3.  **Sends the generated recipe via email** to a specified recipient.


## Features

*   **Daily Recipe Generation:**  Receives a new recipe in your email inbox every day.
*   **Random Country Selection:**  Explores recipes from a diverse list of countries.
*   **Email Delivery:**  Recipes are conveniently delivered directly to your email.
*   **Automated with GitHub Actions:**  Runs automatically on a daily schedule without manual intervention.

## Prerequisites

Before you can set up and run this recipe bot, you will need the following:

1.  **Accounts and API Keys:**
    *   **Google AI Studio API Key (Gemini API Key):**  You need a Gemini API key from Google AI Studio to access the Gemini AI model. You can obtain one at [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey).
    *   **Email Account Credentials:** You'll need an email account (like Gmail, Outlook, etc.) to send emails. You will need the email address and password.

2.  **Software:**
       **Python 3.8 or higher:**  Python is required to run the script.

3.  **GitHub Account:** You'll need a GitHub account to host the repository and set up GitHub Actions.

## Setup Instructions

Follow these steps to set up the Daily Recipe Bot:

1.  **Clone the Repository:**
        Clone this repository to your local machine:
    

2.  **Install Python Libraries:**
        pip install -r requirements.txt

    

3.  **Configure GitHub Secrets:**
    You need to securely store your API keys and email credentials as GitHub Secrets in your repository:
    *   **`GEMINI_API_KEY`**:  Your Gemini API key from Google AI Studio.
    *   **`SENDER_EMAIL`**:  Your email address that will send the recipes.
    *   **`SENDER_PASSWORD`**:  Your email password or App Password.
    *   **`RECEIVER_EMAIL`**:  The email address where you want to receive the daily recipes.
    *   **`SMTP_SERVER`** (Optional): The SMTP server address for your email provider. Defaults to `smtp.gmail.com` if not set. You can set this as a secret if you want to use a different server than Gmail or keep it configurable.
    *   **`SMTP_PORT`** (Optional): The SMTP port number. Defaults to `465` (for SSL) if not set. You can set this as a secret if your SMTP server uses a different port.


## Usage

Once set up, the Daily Recipe Bot will run automatically every day at 9:00 AM UTC (by default).

*   **Scheduled Runs:** The GitHub Actions workflow is scheduled to run daily using a cron expression in `.github/workflows/recipe_bot.yml`. You can adjust the `cron` schedule to change the time of day the bot runs.
*   **Manual Runs:** You can also manually trigger the workflow at any time from the "Actions" tab in your GitHub repository.
    

## Customization

*   **Country_List.txt:** Modify the `countries` list in the text file to include your preferred countries or regions.
*   **Recipe Prompt:**  Adjust the `prompt` in the `generate_recipe()` function to refine the type of recipes generated (e.g., specify vegetarian, vegan, quick, specific cuisine, etc.).
*   **Email Content:** Customize the email subject and body text in the `send_email()` function in `recipe_bot.py`.
*   **Scheduling:** Change the `cron` schedule in `.github/workflows/recipe_bot.yml` to adjust the daily run time.

