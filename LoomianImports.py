import sys
import time
import cv2
import numpy as np
import pydirectinput
import win32gui
import datetime
import pyautogui    # probably needs keyboard module
import pyttsx3
import pytesseract as tess
tess.pytesseract.tesseract_cmd = "C:\\PythonStuff\\SupportingPrograms\\Tesseract-OCR\\tesseract.exe"
toplist, winlist = [], []


def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))


def foreground(window: str, prnt: bool = False):
    win32gui.EnumWindows(enum_cb, toplist)
    target = [(hwnd, title) for hwnd, title in winlist if window in title.lower()]
    target = target[0]
    hwnd = target[0]
    try:
        win32gui.SetForegroundWindow(hwnd)
    except:
        print("Please open Roblox Loomian Legacy first and reopen program, exiting in 3 seconds...")
        time.sleep(3)
        sys.exit()
    if prnt:
        print("Brought", window, "window to foreground")
    time.sleep(1)


def press(key: str, frequency: int = 1, seconds: int = 0):
    repeats = 0
    while repeats < frequency:
        pydirectinput.keyDown(key)
        time.sleep(seconds)
        pydirectinput.keyUp(key)
        repeats += 1


def say(text, noisy: str = "Off"):
    if noisy == "On":
        text2speech = pyttsx3.init()
        text2speech.say(text)
        text2speech.runAndWait()
    else:
        time.sleep(1)
        return 0


def chat(message):
    press("/", 1, 1)
    pyautogui.write(message)
    press("enter")
    time.sleep(1)


class TimeStamps:
    @staticmethod
    def current():
        return str(datetime.datetime.now()).split(".")[0]

    @staticmethod
    def day(time_full):
        return str(time_full).split()[0]

    @staticmethod
    def hour(time_full):
        return str(str(time_full).split()[1]).split(".")[0]


class BattleSTC:
    @staticmethod
    def fight():
        press("s", 2)
        press("a")
        press("w")
        press("enter")
        time.sleep(1)

    @staticmethod
    def items():
        press("d", 2)
        press("s")
        press("a")
        press("enter")
        time.sleep(1)

    @staticmethod
    def escape():
        press("d", 2)
        press("s")
        press("enter")
        time.sleep(4)

    @staticmethod
    def move1():
        press("d", 2)
        press("s", 2)
        press("a", 2)
        press("w")
        press("enter")
        time.sleep(4)

    @staticmethod
    def move2():
        press("a", 2)
        press("s", 2)
        press("d", 2)
        press("w")
        press("enter")
        time.sleep(4)

    @staticmethod
    def move3():
        press("d", 2)
        press("w", 2)
        press("a", 2)
        press("s")
        press("enter")
        time.sleep(4)

    @staticmethod
    def move4():
        press("a", 2)
        press("w", 2)
        press("d", 2)
        press("s")
        press("enter")
        time.sleep(4)

    @staticmethod
    def cancel():
        press("a", 2)
        press("w", 2)
        press("s", 3)
        press("enter")
        time.sleep(1)

    @staticmethod
    def no():
        press("w", 2)
        press("a")
        press("s", 2)
        press("enter")
        time.sleep(1)

    @staticmethod
    def yes():
        press("s", 2)
        press("d")
        press("w", 2)
        press("enter")
        time.sleep(1)

    @staticmethod
    def disc():
        press("d", 2)
        press("w", 2)
        press("a", 2)
        press("enter", 1)
        time.sleep(2)
        press("enter", 2)
        time.sleep(4)

    @staticmethod
    def key_preprocess(key_img, intensity):
        low_black = np.array([0, 0, 0])
        high_black = np.array([255, 255, intensity])
        image = cv2.cvtColor(np.array(key_img), cv2.COLOR_RGB2BGR)
        image_inv = (255 - image)
        hsv = cv2.cvtColor(image_inv, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, low_black, high_black)
        mask_inv = (255 - mask)
        return mask_inv

    @staticmethod
    def key_cleaner(key_str: str):
        key_str = key_str.strip()
        cleaned = ""
        for letter in key_str:
            if letter.lower() in "abcdefghijklmnopqrstuvwxyz! ":
                cleaned += letter
        return cleaned

    @staticmethod
    def alarm(words: str, noisy: str = "Off"):
        alarm_count = 0
        time_full = TimeStamps.current()
        hour = TimeStamps.hour(time_full)
        base_position = pyautogui.position()
        print("Alarm @", hour)
        print("Mouse at top left of the screen [x:0, y:0] to stop the alarm")
        while alarm_count < 40:
            say(words, noisy)
            alarm_count += 1
            time.sleep(1)
            position = pyautogui.position()
            if position != base_position:
                print("Current mouse x, y coordinates:", position)
                base_position = position
            if position[0] == 0 and position[1] == 0:
                print("Alarm stopped")
                say("Alarm stopped", noisy)
                time.sleep(2)
                return False
        print("Alarm stopped automatically, stopping bot...")
        say("Alarm stopped automatically, stopping bot...", noisy)
        return True
# 213 - 7/10/2023, 2:48 PM [ 2/3 weak warnings ] : Seems good. No more touches, I think.
