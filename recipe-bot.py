import random
import os
import google.generativeai as genai
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def get_random_country():
    """Returns a random country name."""
    countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua & Deps", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina", "Burundi", "Cambodia", "Cameroon", "Canada", "Cape Verde", "Central African Rep", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo", "Congo {Democratic Rep}", "Costa Rica", "Croatia", "Cuba", "Cyprus",
    "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Ethiopia", "Fiji", "Finland", "France", "Gabon",
    "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana",
    "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy",
    "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea North", "Korea South",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea", "Paraguay",
    "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russian Federation", "Rwanda", "St Kitts & Nevis",
    "St Lucia", "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands",
    "Somalia", "South Africa", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Swaziland", "Sweden",
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania", "Thailand", "Togo", "Tonga", "Trinidad & Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia",
    "Zimbabwe"]

    return random.choice(countries)

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

def send_email(recipe_text, sender_email, sender_password, receiver_email):
    """Sends the recipe as an email."""
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com" # Example for Gmail, adjust for your provider

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Daily Recipe from {get_random_country()}" # Subject will reflect the country *at sending time*, not generation time necessarily
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

    if not all([gemini_api_key, sender_email, sender_password, receiver_email]):
        print("Error: Missing API keys or email credentials. Make sure to set environment variables.")
        exit(1)

    country = get_random_country()
    print(f"Generating recipe from: {country}")
    recipe = generate_recipe(country, gemini_api_key)

    if recipe:
        print("Recipe generated successfully!")
        print("--- Recipe ---")
        print(recipe) # Optional: Print recipe to console for debugging
        send_email(recipe, sender_email, sender_password, receiver_email)
    else:
        print("Failed to generate or send recipe.")