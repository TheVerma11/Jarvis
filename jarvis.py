import tkinter as tk
from tkinter import END
from PIL import Image, ImageTk, ImageOps
import cv2
import os
import threading
import time
from datetime import datetime

from voice import listen, speak
from assistant import run_jarvis


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

GIF_PATH = os.path.join(ASSETS_DIR, "jarvis.gif")
VIDEO_PATH = os.path.join(ASSETS_DIR, "startup.mp4")


# ============================================================
# GLOBALS
# ============================================================

root = None
terminal = None
status_label = None
status_dot = None
gif_label = None
command_entry = None

listen_button = None
stop_button = None
video_button = None

gif_frames = []
gif_index = 0

video_capture = None
video_playing = False

voice_listening = False
voice_thread = None

processing = False


# ============================================================
# COLORS
# ============================================================

BG = "#02070b"
PANEL = "#06141b"
PANEL_2 = "#071a22"

CYAN = "#00e5ff"
CYAN_DARK = "#08343d"

GREEN = "#00ff9d"
GREEN_DARK = "#06382d"

YELLOW = "#ffc857"
YELLOW_DARK = "#30280d"

RED = "#ff416c"
RED_DARK = "#35101a"

WHITE = "#eafcff"
GRAY = "#78909c"
DARK_GRAY = "#263238"


# ============================================================
# LOGGING
# ============================================================

def get_time_string():
    return datetime.now().strftime("%H:%M:%S")


def log(message, level="INFO"):
    if terminal is None:
        print(f"[{level}] {message}")
        return

    timestamp = get_time_string()

    if level == "SUCCESS":
        tag_color = GREEN
    elif level == "ERROR":
        tag_color = RED
    elif level == "WARNING":
        tag_color = YELLOW
    else:
        tag_color = CYAN

    terminal.configure(state="normal")

    terminal.insert(
        END,
        f"[{timestamp}] "
    )

    terminal.insert(
        END,
        f"[{level}] ",
        level
    )

    terminal.insert(
        END,
        f"{message}\n"
    )

    terminal.configure(state="disabled")
    terminal.see(END)


# ============================================================
# STATUS
# ============================================================

def set_status(text, color=CYAN):
    if status_label is not None:
        status_label.config(
            text=text,
            fg=color
        )

    if status_dot is not None:
        status_dot.config(
            fg=color
        )


# ============================================================
# GIF LOADING
# ============================================================

def load_gif():
    global gif_frames

    gif_frames = []

    if not os.path.exists(GIF_PATH):
        log("jarvis.gif not found.", "ERROR")
        return

    try:
        gif = Image.open(GIF_PATH)

        frame_count = getattr(gif, "n_frames", 1)

        for i in range(frame_count):
            gif.seek(i)

            frame = gif.convert("RGB").copy()

            gif_frames.append(frame)

        log(
            f"HUD GIF loaded successfully. Frames: {len(gif_frames)}",
            "SUCCESS"
        )

    except Exception as error:
        log(f"GIF loading error: {error}", "ERROR")


# ============================================================
# GIF DISPLAY
# ============================================================

def show_gif_frame():
    global gif_index

    if video_playing:
        return

    if not gif_frames:
        return

    try:
        frame = gif_frames[gif_index]

        width = gif_label.winfo_width()
        height = gif_label.winfo_height()

        if width <= 1:
            width = 1040

        if height <= 1:
            height = 300

        # Fill the complete HUD rectangle.
        # The GIF is cropped only if necessary.
        frame = ImageOps.fit(
            frame,
            (width, height),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )

        photo = ImageTk.PhotoImage(frame)

        gif_label.configure(image=photo)
        gif_label.image = photo

        gif_index = (gif_index + 1) % len(gif_frames)

        root.after(40, show_gif_frame)

    except Exception as error:
        log(f"GIF animation error: {error}", "ERROR")


# ============================================================
# VIDEO PLAYBACK
# ============================================================

def play_video():
    global video_capture
    global video_playing

    if video_playing:
        log("Video is already playing.", "WARNING")
        return

    if not os.path.exists(VIDEO_PATH):
        log("startup.mp4 not found in assets folder.", "ERROR")
        set_status("VIDEO NOT FOUND", RED)
        return

    try:
        video_capture = cv2.VideoCapture(VIDEO_PATH)

        if not video_capture.isOpened():
            log("Could not open startup.mp4.", "ERROR")
            set_status("VIDEO ERROR", RED)
            video_capture = None
            return

        video_playing = True

        set_status("VIDEO PLAYING", CYAN)
        log("Startup video started.", "SUCCESS")

        play_video_frame()

    except Exception as error:
        video_playing = False
        video_capture = None

        log(f"Video error: {error}", "ERROR")
        set_status("VIDEO ERROR", RED)


def play_video_frame():
    global video_capture
    global video_playing

    if not video_playing or video_capture is None:
        return

    try:
        success, frame = video_capture.read()

        if not success:
            finish_video()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        image = Image.fromarray(frame)

        width = gif_label.winfo_width()
        height = gif_label.winfo_height()

        if width <= 1:
            width = 1040

        if height <= 1:
            height = 300

        # Make video fill the same HUD rectangle.
        image = ImageOps.fit(
            image,
            (width, height),
            method=Image.Resampling.LANCZOS,
            centering=(0.5, 0.5)
        )

        photo = ImageTk.PhotoImage(image)

        gif_label.configure(image=photo)
        gif_label.image = photo

        fps = video_capture.get(cv2.CAP_PROP_FPS)

        if fps <= 0:
            fps = 30

        delay = max(10, int(1000 / fps))

        root.after(delay, play_video_frame)

    except Exception as error:
        log(f"Video frame error: {error}", "ERROR")
        finish_video()


def finish_video():
    global video_capture
    global video_playing

    video_playing = False

    if video_capture is not None:
        try:
            video_capture.release()
        except Exception:
            pass

    video_capture = None

    set_status("READY", CYAN)
    log("Video finished. Returning to HUD.", "SUCCESS")

    # GIF will automatically continue.
    show_gif_frame()


# ============================================================
# VOICE PROCESSING
# ============================================================

def process_voice_command(command):
    global processing

    if not command:
        return False

    command = command.strip().lower()

    if not command:
        return False

    log(f"You said: {command}", "SUCCESS")

    processing = True
    set_status("PROCESSING", YELLOW)

    try:
        response, should_exit = run_jarvis(command)

        if response:
            log(response, "SUCCESS")

        if should_exit:
            # Goodbye/exit command.
            stop_listening()

            set_status("OFFLINE", RED)

            root.after(
                1200,
                close_application
            )

            return True

    except Exception as error:
        log(f"Command error: {error}", "ERROR")
        set_status("ERROR", RED)

    finally:
        processing = False

    if voice_listening:
        set_status("LISTENING", GREEN)
    else:
        set_status("READY", CYAN)

    return False


# ============================================================
# CONTINUOUS VOICE LOOP
# ============================================================

def voice_loop():
    global voice_listening

    log("Voice command system started.", "SUCCESS")

    while voice_listening:

        if processing:
            time.sleep(0.1)
            continue

        set_status("LISTENING", GREEN)

        log("Listening for command...", "INFO")

        command = listen()

        if not voice_listening:
            break

        if not command:
            log("No command detected. Listening again...", "WARNING")
            continue

        log(f"Command: {command}", "SUCCESS")

        should_close = process_voice_command(command)

        if should_close:
            break

        # Automatically listen for next command.
        if voice_listening:
            time.sleep(0.3)

    if voice_listening is False:
        set_status("READY", CYAN)
        log("Voice command system stopped.", "WARNING")


def start_listening():
    global voice_listening
    global voice_thread

    if voice_listening:
        log("Voice listening is already active.", "WARNING")
        return

    voice_listening = True

    set_status("LISTENING", GREEN)

    log("Continuous voice listening enabled.", "SUCCESS")

    voice_thread = threading.Thread(
        target=voice_loop,
        daemon=True
    )

    voice_thread.start()


def stop_listening():
    global voice_listening

    if not voice_listening:
        set_status("READY", CYAN)
        return

    voice_listening = False

    set_status("READY", CYAN)

    log("Voice listening stopped.", "WARNING")


# ============================================================
# TEXT COMMAND
# ============================================================

def submit_text_command(event=None):
    global command_entry

    if command_entry is None:
        return

    command = command_entry.get().strip()

    if not command:
        return

    command_entry.delete(0, END)

    log(f"Text command: {command}", "INFO")

    threading.Thread(
        target=process_text_command,
        args=(command,),
        daemon=True
    ).start()


def process_text_command(command):
    process_voice_command(command)


# ============================================================
# CLEAR TERMINAL
# ============================================================

def clear_terminal():
    if terminal is None:
        return

    terminal.configure(state="normal")
    terminal.delete("1.0", END)
    terminal.configure(state="disabled")

    log("Terminal cleared.", "SUCCESS")


# ============================================================
# STOP BUTTON
# ============================================================

def stop_button_action():
    stop_listening()

    log("STOP pressed. Voice command loop stopped.", "WARNING")

    set_status("READY", CYAN)


# ============================================================
# VIDEO BUTTON
# ============================================================

def video_button_action():
    # Video button does NOT affect voice listening.
    threading.Thread(
        target=play_video,
        daemon=True
    ).start()


# ============================================================
# BUTTON STYLE
# ============================================================

def create_button(
    parent,
    text,
    command,
    bg_color,
    fg_color,
    width=14
):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg_color,
        fg=fg_color,
        activebackground=bg_color,
        activeforeground=fg_color,
        relief="flat",
        bd=0,
        highlightthickness=0,
        font=("Consolas", 11, "bold"),
        width=width,
        height=2,
        cursor="hand2"
    )

    return button


# ============================================================
# WINDOW CLOSE
# ============================================================

def close_application():
    global video_capture
    global video_playing
    global voice_listening

    voice_listening = False
    video_playing = False

    if video_capture is not None:
        try:
            video_capture.release()
        except Exception:
            pass

        video_capture = None

    try:
        root.destroy()
    except Exception:
        pass


# ============================================================
# WINDOW RESIZE
# ============================================================

def on_window_resize(event=None):
    # GIF/video automatically use the current HUD dimensions.
    pass


# ============================================================
# CREATE GUI
# ============================================================

def create_gui():
    global root
    global terminal
    global status_label
    global status_dot
    global gif_label
    global command_entry

    global listen_button
    global stop_button
    global video_button

    root = tk.Tk()

    root.title("J.A.R.V.I.S - Personal Virtual Assistant")

    root.geometry("1100x850")
    root.minsize(900, 700)

    root.configure(bg=BG)

    root.protocol(
        "WM_DELETE_WINDOW",
        close_application
    )

    root.bind(
        "<Configure>",
        on_window_resize
    )

    # ========================================================
    # MAIN CONTAINER
    # ========================================================

    main = tk.Frame(
        root,
        bg=BG
    )

    main.pack(
        fill="both",
        expand=True,
        padx=24,
        pady=16
    )

    # ========================================================
    # HEADER
    # ========================================================

    title = tk.Label(
        main,
        text="J.A.R.V.I.S",
        font=("Consolas", 42, "bold"),
        fg=CYAN,
        bg=BG
    )

    title.pack(
        pady=(5, 0)
    )

    subtitle = tk.Label(
        main,
        text="JUST A RATHER VERY INTELLIGENT SYSTEM",
        font=("Consolas", 11),
        fg="#4e7580",
        bg=BG
    )

    subtitle.pack(
        pady=(5, 12)
    )

    # ========================================================
    # STATUS
    # ========================================================

    status_frame = tk.Frame(
        main,
        bg=BG
    )

    status_frame.pack(
        pady=(2, 22)
    )

    status_dot = tk.Label(
        status_frame,
        text="●",
        font=("Arial", 12),
        fg=CYAN,
        bg=BG
    )

    status_dot.pack(
        side="left",
        padx=(0, 8)
    )

    status_label = tk.Label(
        status_frame,
        text="READY",
        font=("Consolas", 11, "bold"),
        fg=CYAN,
        bg=BG
    )

    status_label.pack(
        side="left"
    )

    # ========================================================
    # HUD FRAME
    # ========================================================

    hud_frame = tk.Frame(
        main,
        bg=PANEL,
        highlightbackground="#10414b",
        highlightcolor="#10414b",
        highlightthickness=1
    )

    hud_frame.pack(
        fill="x",
        pady=(0, 20)
    )

    # Give HUD a fixed minimum visual height.
    hud_frame.configure(
        height=305
    )

    hud_frame.pack_propagate(False)

    gif_label = tk.Label(
        hud_frame,
        bg=PANEL,
        bd=0,
        highlightthickness=0,
        anchor="center"
    )

    gif_label.pack(
        fill="both",
        expand=True,
        padx=0,
        pady=0
    )

    # ========================================================
    # BUTTONS
    # ========================================================

    button_frame = tk.Frame(
        main,
        bg=BG
    )

    button_frame.pack(
        pady=(0, 13)
    )

    listen_button = create_button(
        button_frame,
        "🎙  LISTEN",
        start_listening,
        PANEL,
        CYAN,
        14
    )

    listen_button.pack(
        side="left",
        padx=6
    )

    clear_button = create_button(
        button_frame,
        "⌫  CLEAR",
        clear_terminal,
        PANEL,
        YELLOW,
        14
    )

    clear_button.pack(
        side="left",
        padx=6
    )

    video_button = create_button(
        button_frame,
        "▶  VIDEO",
        video_button_action,
        PANEL,
        GREEN,
        14
    )

    video_button.pack(
        side="left",
        padx=6
    )

    stop_button = create_button(
        button_frame,
        "■  STOP",
        stop_button_action,
        PANEL,
        RED,
        14
    )

    stop_button.pack(
        side="left",
        padx=6
    )

    # ========================================================
    # TEXT COMMAND AREA
    # ========================================================

    command_frame = tk.Frame(
        main,
        bg=BG
    )

    command_frame.pack(
        fill="x",
        pady=(0, 14)
    )

    command_entry = tk.Entry(
        command_frame,
        bg=PANEL,
        fg=WHITE,
        insertbackground=CYAN,
        relief="flat",
        bd=0,
        font=("Consolas", 13),
        highlightthickness=1,
        highlightbackground=BG,
        highlightcolor=CYAN
    )

    command_entry.pack(
        side="left",
        fill="x",
        expand=True,
        ipady=12,
        padx=(0, 5)
    )

    command_entry.insert(
        0,
        "Type a command..."
    )

    def clear_placeholder(event):
        if command_entry.get() == "Type a command...":
            command_entry.delete(0, END)

    command_entry.bind(
        "<FocusIn>",
        clear_placeholder
    )

    command_entry.bind(
        "<Return>",
        submit_text_command
    )

    send_button = tk.Button(
        command_frame,
        text="➤  SEND",
        command=submit_text_command,
        bg=PANEL,
        fg=GREEN,
        activebackground=PANEL,
        activeforeground=GREEN,
        relief="flat",
        bd=0,
        font=("Consolas", 11, "bold"),
        cursor="hand2",
        width=12,
        height=2
    )

    send_button.pack(
        side="right",
        fill="y"
    )

    # ========================================================
    # TERMINAL HEADER
    # ========================================================

    terminal_header = tk.Frame(
        main,
        bg=PANEL_2,
        height=40
    )

    terminal_header.pack(
        fill="x"
    )

    terminal_header.pack_propagate(False)

    terminal_title = tk.Label(
        terminal_header,
        text="SYSTEM TERMINAL",
        font=("Consolas", 10, "bold"),
        fg=CYAN,
        bg=PANEL_2
    )

    terminal_title.pack(
        side="left",
        padx=20
    )

    online_label = tk.Label(
        terminal_header,
        text="ONLINE ●",
        font=("Consolas", 9),
        fg=GREEN,
        bg=PANEL_2
    )

    online_label.pack(
        side="right",
        padx=20
    )

    # ========================================================
    # TERMINAL
    # ========================================================

    terminal_frame = tk.Frame(
        main,
        bg="#020a0f"
    )

    terminal_frame.pack(
        fill="both",
        expand=True
    )

    terminal = tk.Text(
        terminal_frame,
        bg="#020a0f",
        fg="#b8e8ee",
        insertbackground=CYAN,
        relief="flat",
        bd=0,
        font=("Consolas", 10),
        wrap="word",
        padx=12,
        pady=8
    )

    terminal.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar = tk.Scrollbar(
        terminal_frame,
        command=terminal.yview
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    terminal.configure(
        yscrollcommand=scrollbar.set
    )

    # Terminal tags.
    terminal.tag_config(
        "INFO",
        foreground=CYAN
    )

    terminal.tag_config(
        "SUCCESS",
        foreground=GREEN
    )

    terminal.tag_config(
        "WARNING",
        foreground=YELLOW
    )

    terminal.tag_config(
        "ERROR",
        foreground=RED
    )

    terminal.configure(
        state="disabled"
    )

    # ========================================================
    # STARTUP
    # ========================================================

    load_gif()

    log(
        "J.A.R.V.I.S HUD activated.",
        "SUCCESS"
    )

    log(
        "System ready. Press LISTEN for voice commands.",
        "INFO"
    )

    set_status(
        "READY",
        CYAN
    )

    # Start GIF.
    root.after(
        300,
        show_gif_frame
    )

    return root


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    try:
        create_gui()

        root.mainloop()

    except KeyboardInterrupt:
        pass

    except Exception as error:
        print(f"JARVIS ERROR: {error}")