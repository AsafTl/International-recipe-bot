import random
import os
import google.generativeai as genai
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_random_country():
    """Returns a random country name."""
    import random
import os
import google.generativeai as genai
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def get_random_country():
    """Returns a random country name and its flag emoji from country_list.txt."""
    countries_data = [] # List to store tuples of (country_name, flag_emoji)
    try:
        with open("country_list.txt", "r", encoding='utf-8') as file: # Specify encoding for emojis
            for line in file:
                line = line.strip()
                if line: # Skip empty lines
                    parts = line.split(";")
                    if len(parts) == 2: # Check if line has country and flag separated by ';'
                        country = parts[0].strip()
                        flag_emoji = parts[1].strip()
                        countries_data.append((country, flag_emoji))
                    else:
                        print(f"Warning: Invalid line format in country_list.txt: '{line}'. Skipping.")
    except FileNotFoundError:
        print("Error: country_list.txt not found. Using default country list and emojis.")
        countries_data = [ # Default list of tuples (country, flag)
            ("Italy", "🇮🇹"), ("France", "🇫🇷"), ("Japan", "🇯🇵"), ("India", "🇮🇳"), ("Mexico", "🇲🇽"),
            ("China", "🇨🇳"), ("Spain", "🇪🇸"), ("Greece", "🇬🇷"), ("Thailand", "🇹🇭"), ("Vietnam", "🇻🇳"),
            ("Morocco", "🇲🇦"), ("Brazil", "🇧🇷"), ("Argentina", "🇦🇷"), ("Peru", "🇵🇪"), ("Turkey", "🇹🇷"),
            ("Egypt", "🇪🇬"), ("Nigeria", "🇳🇬"), ("Kenya", "🇰🇪"), ("South Korea", "🇰🇷"), ("Germany", "🇩🇪")
        ]
    except Exception as e:
        print(f"Error reading country_list.txt: {e}. Using default country list and emojis. Error: {e}")
        countries_data = [ # Default list of tuples (country, flag) - same as above
            ("Italy", "🇮🇹"), ("France", "🇫🇷"), ("Japan", "🇯🇵"), ("India", "🇮🇳"), ("Mexico", "🇲🇽"),
            ("China", "🇨🇳"), ("Spain", "🇪🇸"), ("Greece", "🇬🇷"), ("Thailand", "🇹🇭"), ("Vietnam", "🇻🇳"),
            ("Morocco", "🇲🇦"), ("Brazil", "🇧🇷"), ("Argentina", "🇦🇷"), ("Peru", "🇵🇪"), ("Turkey", "🇹🇷"),
            ("Egypt", "🇪🇬"), ("Nigeria", "🇳🇬"), ("Kenya", "🇰🇪"), ("South Korea", "🇰🇷"), ("Germany", "🇩🇪")
        ]

    if not countries_data:
        print("Error: No countries found in country_list.txt or default list. Please check the file.")
        return None, None

    chosen_country_data = random.choice(countries_data)
    chosen_country, flag_emoji = chosen_country_data # Unpack the tuple
    return chosen_country, flag_emoji


def generate_recipe(country, gemini_api_key):
    """Generates a recipe using Gemini API for the given country."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    

    prompt = f"post a recipe which is originating in {country}, choose either an appetizer or a main course recipe, list the ingredients and instructions in a clear manner. If the particular recipe has a cultural importance such as a special holiday or history, tell it as well."

    try:
        response = model.generate_content(prompt)
        recipe_text = response.text
        return recipe_text
    except Exception as e:
        print(f"Error generating recipe from Gemini API: {e}")
        return None

def send_email(recipe_text, sender_email, sender_password, receiver_email, country, flag_emoji):
    """Sends the recipe as an email with country flag in subject, using env vars for SMTP."""
    port = os.environ.get("SMTP_PORT")  # Get port from env var, default to 465
    smtp_server = os.environ.get("SMTP_SERVER") # Get server from env var, default to Gmail

    subject = f"Daily Recipe: {flag_emoji} {country}" # Subject with flag and country
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Create the plain-text and HTML versions of your message
    text = f"Here is your daily recipe:\n\n{recipe_text}"
    html = f"""
    <html>
      <body>
        <p>Here is your daily recipe:<br><br>
           <pre>{recipe_text}</pre>
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)


    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Recipe sent to email successfully!")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False



if __name__ == "__main__":
    # --- IMPORTANT: Set your API keys and email credentials as environment variables ---
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD") # Consider using an App Password for better security
    receiver_email = os.environ.get("RECEIVER_EMAIL") # Your email to receive recipes

    country, flag_emoji = get_random_country() # Get both country and emoji

    if not country: # Check if country is None (error in get_random_country)
        print("Failed to get a country. Aborting recipe generation and email.")
        exit(1)

    print(f"Generating recipe from: {country} {flag_emoji}") # Print with emoji
    recipe = generate_recipe(country, gemini_api_key)

    if recipe:
        print("Recipe generated successfully!")
        print("--- Recipe ---")
        print(recipe)
        send_email(recipe, sender_email, sender_password, receiver_email, country, flag_emoji) # Pass country and emoji
    else:
        print("Failed to generate or send recipe.")