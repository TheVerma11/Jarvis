import io
import wave

import sounddevice as sd
import speech_recognition as sr
import pyttsx3


# ============================================================
# SETTINGS
# ============================================================

SAMPLE_RATE = 16000
RECORD_SECONDS = 5
SPEECH_RATE = 165


# ============================================================
# MALE VOICE
# ============================================================

def get_male_voice(engine):
    """
    Try to find a male Windows voice.
    """

    voices = engine.getProperty("voices")

    if not voices:
        return None

    male_keywords = [
        "david",
        "ravi",
        "mark",
        "guy",
        "george",
        "james",
        "male"
    ]

    female_keywords = [
        "zira",
        "female",
        "hazel",
        "susan"
    ]

    # First: look for known male voices.
    for voice in voices:

        name = voice.name.lower()

        if any(keyword in name for keyword in male_keywords):
            return voice

    # Second: choose a voice that does not look female.
    for voice in voices:

        name = voice.name.lower()

        if not any(keyword in name for keyword in female_keywords):
            return voice

    # Last fallback.
    return voices[0]


# ============================================================
# TEXT TO SPEECH
# ============================================================

def speak(text):
    """
    Convert text into speech.
    """

    if not text:
        return

    try:

        engine = pyttsx3.init()

        engine.setProperty(
            "rate",
            SPEECH_RATE
        )

        engine.setProperty(
            "volume",
            1.0
        )

        male_voice = get_male_voice(engine)

        if male_voice:

            engine.setProperty(
                "voice",
                male_voice.id
            )

            print(
                f"[VOICE] Using: {male_voice.name}"
            )

        engine.say(text)

        engine.runAndWait()

        engine.stop()

    except Exception as error:

        print(
            f"[VOICE ERROR] {error}"
        )


# ============================================================
# MICROPHONE LISTENING
# ============================================================

def listen():
    """
    Record microphone audio and convert it to text.
    """

    recognizer = sr.Recognizer()

    print()
    print("[VOICE] Listening...")

    try:

        # ----------------------------------------------------
        # RECORD AUDIO
        # ----------------------------------------------------

        recording = sd.rec(
            int(
                RECORD_SECONDS *
                SAMPLE_RATE
            ),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        # ----------------------------------------------------
        # CONVERT RECORDING TO WAV BUFFER
        # ----------------------------------------------------

        audio_buffer = io.BytesIO()

        with wave.open(
            audio_buffer,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)

            wav_file.setsampwidth(2)

            wav_file.setframerate(
                SAMPLE_RATE
            )

            wav_file.writeframes(
                recording.tobytes()
            )

        audio_buffer.seek(0)

        # ----------------------------------------------------
        # SPEECH RECOGNITION
        # ----------------------------------------------------

        with sr.AudioFile(
            audio_buffer
        ) as source:

            audio = recognizer.record(
                source
            )

        print(
            "[VOICE] Processing..."
        )

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = command.lower().strip()

        print(
            f"[YOU] {command}"
        )

        return command

    # --------------------------------------------------------
    # COULD NOT UNDERSTAND
    # --------------------------------------------------------

    except sr.UnknownValueError:

        print(
            "[VOICE] Could not understand."
        )

        return ""

    # --------------------------------------------------------
    # GOOGLE SPEECH SERVICE ERROR
    # --------------------------------------------------------

    except sr.RequestError as error:

        print(
            f"[VOICE ERROR] Speech service: {error}"
        )

        return ""

    # --------------------------------------------------------
    # MICROPHONE / SYSTEM ERROR
    # --------------------------------------------------------

    except Exception as error:

        print(
            f"[VOICE ERROR] {error}"
        )

        return ""


# ============================================================
# VOICE MODULE TEST
# ============================================================

if __name__ == "__main__":

    print(
        "========================================"
    )

    print(
        "       J.A.R.V.I.S VOICE TEST"
    )

    print(
        "========================================"
    )

    print()

    # Test male TTS.
    speak(
        "Hello. I am Jarvis. "
        "My voice system is online."
    )

    print()

    # Test microphone.
    command = listen()

    print()

    if command:

        print(
            f"Recognized command: {command}"
        )

        speak(
            f"You said {command}"
        )

    else:

        speak(
            "I could not understand you."
        )