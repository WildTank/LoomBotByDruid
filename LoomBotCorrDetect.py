import sqlite3
import time
import pyautogui
import pydirectinput
import LoomianImports
import pytesseract as tess
from PIL import ImageGrab


def get_tuple(menu_x: int, menu_y: int):
    main_x1 = menu_x - 350
    main_y1 = menu_y + 474
    main_x2 = main_x1 + 790
    main_y2 = main_y1 + 117
    tup = (main_x1, main_y1, main_x2, main_y2)
    return tup


tess.pytesseract.tesseract_cmd = "C:\\PythonStuff\\SupportingPrograms\\Tesseract-OCR\\tesseract.exe"


def main(noisy: str = "Off", err: int = 20, chat: str = "Off"):
    print("Starting encounter bot...")
    if noisy == "On":
        LoomianImports.say("Text to speech is on", noisy)
    try:
        LoomianImports.foreground("roblox")
    except IndexError:
        print(r'Did not find any window with "Roblox" in it, please open Roblox Loomian Legacy first.')
        return 1
    print("Noisy:", noisy)
    print("Chat:", chat)
    print("Max errors:", err)
    print("Make sure you have done the set up in the guide, the bot will detect the menu icon on the top.")
    keys_encountered = []
    keys_enc_num = []
    encounter_num = 0
    in_battle = False
    main_error = 0
    while True:
        if not in_battle:
            start_time = int(time.time())
            while True:
                menu_feat = pyautogui.locateOnScreen("images\\menu.png")
                if menu_feat is None:
                    total_time = int(time.time()) - start_time
                    if total_time > 15:
                        print("Did not detect menu icon within 15 seconds, stopping bot...")
                        LoomianImports.say("Did not detect menu icon after some time, stopping...", noisy)
                        return 0
                    continue
                print("\nDetected the menu icon, pressing the 'D' key to character spin...")
                print("Learn how: https://www.youtube.com/watch?v=bXvBfVpEqWQ&pp=ygUSbHVja3kgaGQgYXV0byBodW50",
                      "[select link -> ctrl+C] to copy")
                main_tuple = get_tuple(menu_feat[0], menu_feat[1])
                break
            pydirectinput.keyDown("d")
            LoomianImports.press("/")
            pydirectinput.keyUp("d")
            print("Waiting...")
            start_time = int(time.time())
            # encounter detector and database handler
            while True:
                total_time = int(time.time()) - start_time
                if total_time > 15:
                    print("No encounters in 15 seconds, stopping roam and bot...")
                    LoomianImports.say("No encounters after some time, stopping...", noisy)
                    return 0
                try:
                    ss = ImageGrab.grab()
                    cropped = ss.crop(main_tuple)
                    processed = LoomianImports.BattleSTC.key_preprocess(cropped, 90)
                    text = tess.image_to_string(processed)
                    main_text = LoomianImports.BattleSTC.key_cleaner(text)
                    if main_text.find("appear") >= 0:
                        print("Got an encounter! {}".format(main_text))
                        encounter_num += 1
                        if main_text.find("wild") < 0:
                            print(r'Did not find the word "wild". Might be a corrupt, stopping bot...')
                            LoomianImports.BattleSTC.alarm("Potentially corrupt", noisy)
                            return 0
                        loom_key = main_text.split("appear")[0].split(" ")[2]
                        print("Loom Key: {}".format(loom_key))
                        connection = sqlite3.Connection("loomianlegacy.db")
                        cursor = connection.cursor()
                        cursor.execute("SELECT * FROM loomians")
                        entries_array = cursor.fetchall()
                        in_database = False
                        for entry in entries_array:
                            if loom_key == entry[1]:
                                LoomianImports.press("enter")
                                in_database = True
                                in_battle = True
                                action = entry[2]
                                print("Database: {} {}".format(entry[1], entry[2]))
                                break
                        if not in_database:
                            print("Loom was not found in database.")
                            return 0
                        connection.commit()
                        connection.close()
                        break
                except UnboundLocalError:
                    print("Something went wrong, horribly wrong... [Unbound Local Error]")
                    main_error += 1
                    print("Error Count:", main_error)
                    if main_error == err:
                        print("Maximum number of errors reached, stopping bot...")
                        LoomianImports.say("Max number of errors reached, stopping...")
                        return 1
        if in_battle:
            try:
                fight_feat = pyautogui.locateOnScreen("images\\fight.png")
                if fight_feat is not None:
                    if action == "Esc":
                        print("Escaping...")
                        LoomianImports.BattleSTC.escape()
                    elif action == "Alert":
                        print("Stalling...")
                        if chat == "On":
                            LoomianImports.press("/")
                            pydirectinput.write(loom_key)
                            LoomianImports.press("enter")
                        if LoomianImports.BattleSTC.alarm("Stalling...", noisy):
                            return 0
                    else:
                        LoomianImports.BattleSTC.fight()
                        if action == "Atk1":
                            print("Using move 1...")
                            LoomianImports.BattleSTC.move1()
                        elif action == "Atk2":
                            print("Using move 2...")
                            LoomianImports.BattleSTC.move2()
                        elif action == "Atk3":
                            print("Using move 3...")
                            LoomianImports.BattleSTC.move3()
                        elif action == "Atk4":
                            print("Using move 4...")
                            LoomianImports.BattleSTC.move4()
                        else:
                            print("Something is wrong with the Loomian database.")
                            print("Please reset in settings, and if still not fixed, just download again.")
                            return 1
            except UnboundLocalError:
                print("Something went wrong, horribly wrong... [Unbound Local Error]")
                main_error += 1
                print("Error Count:", main_error)
                if main_error == err:
                    print("Maximum number of errors reached, stopping bot...")
                    LoomianImports.say("Max number of errors reached, stopping...")
                    return 1
            # after encounter handler
            menu_feat = pyautogui.locateOnScreen("images\\menu.png")
            if menu_feat is not None:
                final_key = loom_key
                alr_enc = False
                index = 0
                for key in keys_encountered:
                    if key == final_key:
                        keys_enc_num[index] += 1
                        alr_enc = True
                    index += 1
                if not alr_enc:
                    keys_encountered.append(final_key)
                    keys_enc_num.append(1)
                print("Encounter finished: {} ... {}".format(encounter_num, final_key))
                print(keys_encountered)
                print(keys_enc_num)
                in_battle = False
            # these if statements detect certain prompts/events during an encounter
            progress_feat = pyautogui.locateOnScreen("images\\progress.png")
            if progress_feat is not None:
                print("A trainer mastery mission milestone, please check manually, stopping bot...")
                LoomianImports.BattleSTC.alarm("Mission milestone...", noisy)
                return 0
            evolve_feat = pyautogui.locateOnScreen("images\\evolving.png")
            if evolve_feat is not None:
                print("An evolution is occurring, stopping bot for user to decide... ")
                LoomianImports.BattleSTC.alarm("Evolution ready...", noisy)
                return 0
            no_feat = pyautogui.locateOnScreen("images\\blue_no.png")
            if no_feat is not None:
                print("There is a yes or no prompt!!!")
                LoomianImports.BattleSTC.alarm("Waiting...", noisy)
                return 0
            faint_feat = pyautogui.locateOnScreen("images\\loomian_faint.png")
            if faint_feat is not None:
                print("Detected Loomian party window. Current Loomian probably has fainted.")
                LoomianImports.BattleSTC.alarm("Waiting...", noisy)
                return 0
# 191 - 7/11/2023, 11:51 AM [ 3 warnings ] : My brain is rotting
