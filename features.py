# features.py

import datetime
import webbrowser
import requests
import pywhatkit
import wikipedia


# =========================================================
# WEATHER
# =========================================================

def get_weather(city="Delhi"):
    try:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"Sorry, I couldn't get the weather for {city}."

        data = response.json()
        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        humidity = current["humidity"]
        description = current["weatherDesc"][0]["value"]

        return (
            f"The weather in {city} is {description}. "
            f"The temperature is {temperature} degrees Celsius, "
            f"and it feels like {feels_like} degrees. "
            f"Humidity is {humidity} percent."
        )

    except Exception as error:
        print(f"[WEATHER ERROR] {error}")
        return "Sorry, I couldn't fetch the weather right now."


# =========================================================
# YOUTUBE
# =========================================================

def play_youtube(query):
    try:
        if not query:
            return "What would you like me to play on YouTube?"

        print(f"[YOUTUBE] Playing: {query}")
        pywhatkit.playonyt(query)

        return f"Playing {query} on YouTube."

    except Exception as error:
        print(f"[YOUTUBE ERROR] {error}")
        return "Sorry, I couldn't open YouTube."


# =========================================================
# WIKIPEDIA
# =========================================================

def search_wikipedia(query):
    try:
        if not query:
            return "What would you like me to search on Wikipedia?"

        wikipedia.set_lang("en")

        result = wikipedia.summary(
            query,
            sentences=2,
            auto_suggest=True
        )

        return result

    except wikipedia.exceptions.DisambiguationError as error:
        options = error.options[:5]
        return (
            "There are multiple results for that topic. "
            "Some options are: " + ", ".join(options)
        )

    except wikipedia.exceptions.PageError:
        return "I couldn't find that topic on Wikipedia."

    except Exception as error:
        print(f"[WIKIPEDIA ERROR] {error}")
        return "Sorry, I couldn't search Wikipedia."


# =========================================================
# GOOGLE SEARCH
# =========================================================

def google_search(query):
    try:
        if not query:
            return "What should I search for?"

        search_url = (
            "https://www.google.com/search?q="
            + requests.utils.quote(query)
        )

        webbrowser.open(search_url)

        return f"Searching Google for {query}."

    except Exception as error:
        print(f"[GOOGLE ERROR] {error}")
        return "Sorry, I couldn't open Google."


# =========================================================
# WEBSITES
# =========================================================

WEBSITES = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "linkedin": "https://www.linkedin.com",
    "gmail": "https://mail.google.com",
    "facebook": "https://www.facebook.com",
    "instagram": "https://www.instagram.com",
    "chatgpt": "https://chatgpt.com",
}


def open_website(name):
    try:
        name = name.lower().strip()

        if name in WEBSITES:
            webbrowser.open(WEBSITES[name])
            return f"Opening {name}."

        # If complete URL is given
        if name.startswith("http://") or name.startswith("https://"):
            webbrowser.open(name)
            return "Opening the website."

        return f"I don't have a shortcut for {name}."

    except Exception as error:
        print(f"[WEBSITE ERROR] {error}")
        return "Sorry, I couldn't open the website."


# =========================================================
# JOKES
# =========================================================

def tell_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return "Sorry, I couldn't find a joke right now."

        data = response.json()

        setup = data.get("setup", "")
        punchline = data.get("punchline", "")

        return f"{setup} ... {punchline}"

    except Exception as error:
        print(f"[JOKE ERROR] {error}")
        return "Why did the computer go to the doctor? Because it had a virus."


# =========================================================
# TIME
# =========================================================

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    return f"The current time is {current_time}."


# =========================================================
# DATE
# =========================================================

def get_date():
    current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
    return f"Today is {current_date}."


# =========================================================
# CALCULATOR
# =========================================================

def calculate(expression):
    try:
        if not expression:
            return "Please provide a calculation."

        # Allow only basic mathematical characters
        allowed_characters = "0123456789+-*/().% "

        if not all(char in allowed_characters for char in expression):
            return "I can only calculate basic mathematical expressions."

        result = eval(expression, {"__builtins__": None}, {})

        return f"The answer is {result}."

    except ZeroDivisionError:
        return "You cannot divide by zero."

    except Exception as error:
        print(f"[CALCULATOR ERROR] {error}")
        return "Sorry, I couldn't calculate that."


# =========================================================
# MODULE TEST
# =========================================================

if __name__ == "__main__":

    print("========================================")
    print("       J.A.R.V.I.S FEATURES TEST")
    print("========================================")

    print("\n1. Time:")
    print(get_time())

    print("\n2. Date:")
    print(get_date())

    print("\n3. Calculator:")
    print(calculate("25 * 4 + 10"))

    print("\n4. Website:")
    print(open_website("github"))

    print("\n5. Weather:")
    print(get_weather("Delhi"))

    print("\n6. Joke:")
    print(tell_joke())

    print("\n========================================")
    print("Features module test completed.")
    print("========================================")