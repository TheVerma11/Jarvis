from voice import speak

from features import (
    get_weather,
    play_youtube,
    search_wikipedia,
    google_search,
    open_website,
    tell_joke,
    get_time,
    get_date,
    calculate,
)

from system import (
    open_notepad,
    open_calculator,
    open_paint,
    open_cmd,
    open_powershell,
    open_file_explorer,
    open_downloads,
    open_documents,
    open_desktop,
    get_battery_status,
    take_screenshot,
    get_system_info,
    lock_computer,
    open_task_manager,
)


# ============================================================
# J.A.R.V.I.S COMMAND PROCESSOR
# ============================================================

def run_jarvis(command):

    if not command:
        return "", False

    command = command.lower().strip()

    print()
    print(f"[JARVIS] Processing: {command}")

    # ========================================================
    # EXIT / GOODBYE
    # ========================================================

    if command in [
        "exit",
        "quit",
        "goodbye",
        "good bye",
        "shutdown jarvis",
        "close jarvis",
        "go offline",
    ]:

        response = (
            "Goodbye. JARVIS is going offline."
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, True

    # ========================================================
    # GREETINGS
    # ========================================================

    if command in [
        "hello",
        "hi",
        "hey",
        "hello jarvis",
        "hi jarvis",
        "hey jarvis",
    ]:

        response = (
            "Hello. I am Jarvis. "
            "How can I help you?"
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # IDENTITY
    # ========================================================

    if (
        "who are you" in command
        or "what are you" in command
        or "your name" in command
    ):

        response = (
            "I am JARVIS, your personal "
            "virtual assistant."
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # HOW ARE YOU
    # ========================================================

    if (
        "how are you" in command
        or "how are you doing" in command
    ):

        response = (
            "I am doing great. "
            "All systems are working normally."
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # THANKS
    # ========================================================

    if (
        "thank you" in command
        or "thanks" in command
        or "thank you jarvis" in command
    ):

        response = (
            "You're welcome."
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # TIME
    # ========================================================

    if (
        "what time is it" in command
        or "current time" in command
        or command == "time"
        or "tell me the time" in command
    ):

        response = get_time()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # DATE
    # ========================================================

    if (
        "what is today's date" in command
        or "what is the date" in command
        or "today's date" in command
        or command == "date"
        or "tell me the date" in command
    ):

        response = get_date()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # WEATHER
    # ========================================================

    if (
        "weather" in command
        or "temperature" in command
        or "forecast" in command
    ):

        city = "Delhi"

        weather_words = [
            "weather in",
            "temperature in",
            "forecast in",
        ]

        for word in weather_words:

            if word in command:

                city = command.split(
                    word,
                    1
                )[1].strip()

                break

        if not city:
            city = "Delhi"

        response = get_weather(city)

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # YOUTUBE
    # ========================================================

    if (
        "play on youtube" in command
        or "play youtube" in command
        or "youtube" in command
    ):

        query = command

        for phrase in [
            "play on youtube",
            "play youtube",
            "youtube",
        ]:

            query = query.replace(
                phrase,
                ""
            )

        query = query.strip()

        if not query:
            query = "music"

        response = play_youtube(query)

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # WIKIPEDIA
    # ========================================================

    if (
        "wikipedia" in command
        or "search wikipedia" in command
        or "according to wikipedia" in command
    ):

        query = command

        for phrase in [
            "search wikipedia for",
            "search wikipedia",
            "wikipedia",
            "according to wikipedia",
        ]:

            query = query.replace(
                phrase,
                ""
            )

        query = query.strip()

        if not query:

            response = (
                "Please tell me what "
                "you want me to search on Wikipedia."
            )

        else:

            response = search_wikipedia(
                query
            )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # GOOGLE SEARCH
    # ========================================================

    if (
        "search google for" in command
        or "google search" in command
        or "search google" in command
        or command.startswith("search ")
    ):

        query = command

        for phrase in [
            "search google for",
            "search google",
            "google search",
            "search",
        ]:

            query = query.replace(
                phrase,
                ""
            )

        query = query.strip()

        if not query:

            response = (
                "Please tell me what "
                "you want me to search."
            )

        else:

            response = google_search(
                query
            )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # WEBSITES
    # ========================================================

    website_names = [
        "google",
        "youtube",
        "github",
        "linkedin",
        "gmail",
        "facebook",
        "instagram",
        "chatgpt",
    ]

    for website in website_names:

        if (
            command == website
            or f"open {website}" in command
            or f"open {website} website" in command
        ):

            response = open_website(
                website
            )

            print(
                f"JARVIS > {response}"
            )

            speak(response)

            return response, False

    # ========================================================
    # JOKE
    # ========================================================

    if (
        "tell me a joke" in command
        or "tell a joke" in command
        or command == "joke"
        or "make me laugh" in command
    ):

        response = tell_joke()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # NOTEPAD
    # ========================================================

    if (
        "open notepad" in command
        or "start notepad" in command
        or command == "notepad"
    ):

        response = open_notepad()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # CALCULATOR APP
    # ========================================================

    if (
        "open calculator" in command
        or "start calculator" in command
        or command == "calculator"
    ):

        response = open_calculator()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # PAINT
    # ========================================================

    if (
        "open paint" in command
        or "start paint" in command
        or command == "paint"
    ):

        response = open_paint()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # COMMAND PROMPT
    # ========================================================

    if (
        "open command prompt" in command
        or "open cmd" in command
        or command == "cmd"
    ):

        response = open_cmd()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # POWERSHELL
    # ========================================================

    if (
        "open powershell" in command
        or "start powershell" in command
        or command == "powershell"
    ):

        response = open_powershell()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # FILE EXPLORER
    # ========================================================

    if (
        "open file explorer" in command
        or "open explorer" in command
        or "file explorer" in command
    ):

        response = open_file_explorer()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # DOWNLOADS
    # ========================================================

    if (
        "open downloads" in command
        or command == "downloads"
    ):

        response = open_downloads()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # DOCUMENTS
    # ========================================================

    if (
        "open documents" in command
        or command == "documents"
    ):

        response = open_documents()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # DESKTOP
    # ========================================================

    if (
        "open desktop" in command
        or command == "desktop"
    ):

        response = open_desktop()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # BATTERY
    # ========================================================

    if (
        "battery" in command
        or "battery status" in command
        or "how much battery" in command
    ):

        response = get_battery_status()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    if (
        "system information" in command
        or "system info" in command
        or "system status" in command
        or "cpu usage" in command
        or "ram usage" in command
    ):

        response = get_system_info()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # SCREENSHOT
    # ========================================================

    if (
        "take screenshot" in command
        or "take a screenshot" in command
        or command == "screenshot"
    ):

        response = take_screenshot()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # TASK MANAGER
    # ========================================================

    if (
        "open task manager" in command
        or command == "task manager"
    ):

        response = open_task_manager()

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        return response, False

    # ========================================================
    # LOCK COMPUTER
    # ========================================================

    if (
        "lock computer" in command
        or "lock the computer" in command
        or command == "lock"
    ):

        response = (
            "Locking the computer."
        )

        print(
            f"JARVIS > {response}"
        )

        speak(response)

        lock_computer()

        return response, False

    # ========================================================
    # CALCULATION
    # ========================================================

    calculation_triggers = [
        "calculate",
        "what is",
        "how much is",
    ]

    for trigger in calculation_triggers:

        if command.startswith(trigger):

            expression = command[
                len(trigger):
            ].strip()

            if expression:

                response = calculate(
                    expression
                )

                print(
                    f"JARVIS > {response}"
                )

                speak(response)

                return response, False

    # ========================================================
    # UNKNOWN COMMAND
    # ========================================================

    response = (
        "I am sorry, I did not understand "
        "that command."
    )

    print(
        f"JARVIS > {response}"
    )

    speak(response)

    return response, False


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "========================================"
    )

    print(
        "       J.A.R.V.I.S ASSISTANT TEST"
    )

    print(
        "========================================"
    )

    print()

    print(
        "Type commands to test Jarvis."
    )

    print(
        "Type 'exit' to stop."
    )

    print()

    while True:

        command = input(
            "YOU > "
        ).strip()

        if not command:
            continue

        response, should_exit = run_jarvis(
            command
        )

        if should_exit:
            break