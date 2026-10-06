# system.py

import os
import subprocess
import time
from pathlib import Path

import psutil
import pyautogui


# =========================================================
# OPEN APPLICATIONS
# =========================================================

def open_notepad():
    try:
        subprocess.Popen(["notepad.exe"])
        return "Opening Notepad."
    except Exception as error:
        print(f"[SYSTEM ERROR] Notepad: {error}")
        return "Sorry, I couldn't open Notepad."


def open_calculator():
    try:
        subprocess.Popen(["calc.exe"])
        return "Opening Calculator."
    except Exception as error:
        print(f"[SYSTEM ERROR] Calculator: {error}")
        return "Sorry, I couldn't open Calculator."


def open_paint():
    try:
        subprocess.Popen(["mspaint.exe"])
        return "Opening Paint."
    except Exception as error:
        print(f"[SYSTEM ERROR] Paint: {error}")
        return "Sorry, I couldn't open Paint."


def open_cmd():
    try:
        subprocess.Popen(["cmd.exe"])
        return "Opening Command Prompt."
    except Exception as error:
        print(f"[SYSTEM ERROR] CMD: {error}")
        return "Sorry, I couldn't open Command Prompt."


def open_powershell():
    try:
        subprocess.Popen(["powershell.exe"])
        return "Opening PowerShell."
    except Exception as error:
        print(f"[SYSTEM ERROR] PowerShell: {error}")
        return "Sorry, I couldn't open PowerShell."


def open_file_explorer():
    try:
        subprocess.Popen(["explorer.exe"])
        return "Opening File Explorer."
    except Exception as error:
        print(f"[SYSTEM ERROR] Explorer: {error}")
        return "Sorry, I couldn't open File Explorer."


# =========================================================
# OPEN FOLDERS
# =========================================================

def open_downloads():
    try:
        path = Path.home() / "Downloads"
        os.startfile(path)
        return "Opening Downloads folder."
    except Exception as error:
        print(f"[SYSTEM ERROR] Downloads: {error}")
        return "Sorry, I couldn't open Downloads."


def open_documents():
    try:
        path = Path.home() / "Documents"
        os.startfile(path)
        return "Opening Documents folder."
    except Exception as error:
        print(f"[SYSTEM ERROR] Documents: {error}")
        return "Sorry, I couldn't open Documents."


def open_desktop():
    try:
        path = Path.home() / "Desktop"
        os.startfile(path)
        return "Opening Desktop."
    except Exception as error:
        print(f"[SYSTEM ERROR] Desktop: {error}")
        return "Sorry, I couldn't open Desktop."


# =========================================================
# BATTERY
# =========================================================

def get_battery_status():
    try:
        battery = psutil.sensors_battery()

        if battery is None:
            return "Battery information is not available."

        percentage = battery.percent

        if battery.power_plugged:
            status = "charging"
        else:
            status = "not charging"

        return (
            f"The battery is at {percentage} percent "
            f"and is currently {status}."
        )

    except Exception as error:
        print(f"[BATTERY ERROR] {error}")
        return "Sorry, I couldn't check the battery status."


# =========================================================
# SCREENSHOT
# =========================================================

def take_screenshot():
    try:
        screenshot_dir = Path.home() / "Pictures" / "Jarvis Screenshots"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = (
            screenshot_dir / f"jarvis_screenshot_{timestamp}.png"
        )

        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        return f"Screenshot saved successfully at {screenshot_path}."

    except Exception as error:
        print(f"[SCREENSHOT ERROR] {error}")
        return "Sorry, I couldn't take a screenshot."


# =========================================================
# SYSTEM INFORMATION
# =========================================================

def get_system_info():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()

        ram_usage = memory.percent

        return (
            f"CPU usage is {cpu_usage} percent. "
            f"RAM usage is {ram_usage} percent."
        )

    except Exception as error:
        print(f"[SYSTEM INFO ERROR] {error}")
        return "Sorry, I couldn't get system information."


# =========================================================
# LOCK COMPUTER
# =========================================================

def lock_computer():
    try:
        subprocess.run(
            ["rundll32.exe", "user32.dll,LockWorkStation"],
            check=False
        )
        return "Locking the computer."

    except Exception as error:
        print(f"[LOCK ERROR] {error}")
        return "Sorry, I couldn't lock the computer."


# =========================================================
# OPEN TASK MANAGER
# =========================================================

def open_task_manager():
    try:
        subprocess.Popen(["taskmgr.exe"])
        return "Opening Task Manager."

    except Exception as error:
        print(f"[SYSTEM ERROR] Task Manager: {error}")
        return "Sorry, I couldn't open Task Manager."


# =========================================================
# MODULE TEST
# =========================================================

if __name__ == "__main__":

    print("========================================")
    print("        J.A.R.V.I.S SYSTEM TEST")
    print("========================================")

    print("\n1. Battery:")
    print(get_battery_status())

    print("\n2. System Information:")
    print(get_system_info())

    print("\n3. Testing application functions:")
    print(open_notepad())

    print("\n4. Testing folder function:")
    print(open_downloads())

    print("\n5. Screenshot:")
    print(take_screenshot())

    print("\n========================================")
    print("System module test completed.")
    print("========================================")