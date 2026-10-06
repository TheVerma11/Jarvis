# 🤖 J.A.R.V.I.S – Personal Virtual Assistant

A Python-based personal virtual assistant that supports voice and text commands for web tasks, Windows system operations, and everyday utilities.

The project uses a modular architecture to keep voice processing, command handling, web features, system operations, and GUI functionality organized.

---

## ✨ Features

- 🎙️ Voice command recognition
- 🔊 Text-to-Speech using pyttsx3
- ⌨️ Text command support
- 🖥️ Futuristic Tkinter GUI with animated HUD
- 🌐 Google Search
- ▶️ YouTube search and playback
- 📖 Wikipedia search
- 🌤️ Weather information
- 🌍 Open frequently used websites
- 💻 Open Windows applications
- 📁 Open common folders
- 🔋 Battery, CPU and RAM monitoring
- 📸 Screenshot capture
- 🧮 Calculator
- 😂 Joke generation
- 🔒 Computer lock
- ▶️ Video playback inside the HUD
- 📝 Real-time command terminal

---

## 🛠️ Technologies Used

- Python
- Tkinter
- SpeechRecognition
- SoundDevice
- pyttsx3
- Requests
- PyWhatKit
- Wikipedia
- psutil
- PyAutoGUI
- Pillow
- OpenCV

---

## 📂 Project Structure

    Jarvis/
    │
    ├── jarvis.py
    ├── assistant.py
    ├── voice.py
    ├── features.py
    ├── system.py
    ├── requirements.txt
    ├── README.md
    │
    └── assets/
        ├── jarvis.gif
        └── startup.mp4

---

## 🧩 Modules

| File | Purpose |
|------|---------|
| `jarvis.py` | Main GUI and application controller |
| `assistant.py` | Command processing and routing |
| `voice.py` | Speech recognition and Text-to-Speech |
| `features.py` | Web and utility features |
| `system.py` | Windows system operations |
| `assets/` | GIF and video assets |

---

## ⚙️ How It Works

1. Start the J.A.R.V.I.S application.
2. Use voice commands through the microphone or enter commands through the text box.
3. `assistant.py` processes the command.
4. The command is routed to the appropriate feature or system function.
5. J.A.R.V.I.S performs the requested task.
6. The response is displayed in the terminal and can also be spoken using Text-to-Speech.

---

## ▶️ How to Run

### 1. Clone the repository

    git clone https://github.com/TheVerma11/Jarvis.git
    cd Jarvis

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Run the application

    py jarvis.py

or:

    python jarvis.py

---

## 🎙️ Example Commands

    Hello Jarvis
    What is the time?
    What is the weather in Delhi?
    Search Google for Python
    Search Wikipedia for Artificial Intelligence
    Play YouTube music
    Open GitHub
    Open Notepad
    Open Calculator
    Open Downloads
    Battery status
    System information
    Take a screenshot
    Tell me a joke
    Calculate 25 * 4
    Goodbye

Commands can also be entered through the GUI text box.

---

## 📦 Requirements

The project requires Python and the following packages:

    SpeechRecognition
    pyttsx3
    requests
    sounddevice
    pywhatkit
    wikipedia
    psutil
    pyautogui
    Pillow
    opencv-python

The project is primarily designed for **Windows**.

An internet connection is required for features such as web search, YouTube, Wikipedia, weather, and online speech recognition.

---

## 🚀 Future Improvements

Possible future enhancements include:

- Wake-word activation
- AI-powered conversations
- More natural language understanding
- Additional Windows automation
- Volume, Wi-Fi and Bluetooth controls
- File search and management
- Improved GUI and voice interaction

---

## 👨‍💻 Author

**Rohit Verma**


GitHub: [TheVerma11](https://github.com/TheVerma11)

---

## 📄 License

This project is created for educational, learning, and portfolio purposes.