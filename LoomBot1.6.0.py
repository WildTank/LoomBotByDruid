import time
import customtkinter
import sqlite3
import pydirectinput
import ctypes
import LoomBotCorrDetect
from scrapy.crawler import CrawlerProcess
import scraper
import json
# reset entries must be adjusted/fixed


def set_window():
    user32 = ctypes.windll.user32
    res = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
    handle = user32.FindWindowW(None, u"Roblox")
    user32.ShowWindow(handle, 6)
    user32.ShowWindow(handle, 9)
    user32.MoveWindow(handle, res[0] - 800, 0, 800, 630, True)
    # for GUI
    handle = user32.FindWindowW(None, u"LoomBot1.5.0 - Loomian Legacy Keyboard "
                                      u"Input Emulator Bot by Druid")
    user32.MoveWindow(handle, 0, 0, 616, 519, True)
    # for console
    handle = user32.FindWindowW(None, u"C:\\LoomBot-Druid\\LoomBot1.5.0\\LoomBot1.5.0.exe")
    user32.MoveWindow(handle, 0, 400, 1000, 300, True)
    user32.ShowWindow(handle, 6)
    user32.ShowWindow(handle, 9)
    print("\n[Roblox -> upper right corner]",
          "\n[LoomBot -> upper left corner]",
          "\n[Roblox -> 800x630 pixels]",
          "\n[LoomBot -> 600x480 pixels]")
    print("Make sure that the Loomian Legacy is already open by yourself.")


def encounter_start():
    try:
        LoomBotCorrDetect.main(mode.get_noise(), int(mode.get_error()), mode.get_chat())
    except pydirectinput.FailSafeException:
        print("The mouse cursor was on corner of screen while emulating keyboard input.")
        print("The fail safe function has been triggered, the bot is stopped forcibly.")


class Database:     # class for database related tasks/requests
    def __init__(self):
        db_frame = customtkinter.CTkScrollableFrame(frameTab.tab("    DATA BASE    "))
        db_frame.pack(padx=10, pady=10, fill="both", expand="True")
        self.master = db_frame
        self.entry_out = False
        Database.scrape_looms()
        self.message = "Generating database entries..."
        Database.generate_entry(self)

    @staticmethod
    def loom_entry(master: customtkinter.CTkScrollableFrame, loom_id: str, loom_name: str,  # 97 columns
                   loom_action: str):
        frame = customtkinter.CTkFrame(master)
        frame.pack(padx=10, pady=10, fill="x")
        loom_id = customtkinter.CTkLabel(frame, font=("Arial", 16), text=loom_id)
        loom_id.pack(padx=10, pady=0)
        name = customtkinter.CTkLabel(frame, font=("Arial", 24), text=loom_name)
        name.pack(padx=10, pady=0, side="left")
        action = customtkinter.CTkLabel(frame, font=("Arial", 24), text=loom_action)
        action.pack(padx=10, pady=0, side="right")

    @staticmethod
    def scrape_looms():
        if __name__ == "__main__":
            connection = sqlite3.connect("loomianlegacy.db")
            cursor = connection.cursor()
            # emptying database
            cursor.execute("""DELETE FROM loomians""")
            # start scraping and store to loomians.json file
            print("Scraping loomians from fandom wiki....")
            time.sleep(2)
            process = CrawlerProcess(
                settings = {
                    "FEEDS": {
                        "loomians.json": {"format": "json"}
                    }
                } 
            )
            process.crawl(scraper.LoomianSpider)
            process.start()
            print("Scraping finished!")
            # getting and adding data from loomians.json file to database
            print("Adding scraped loomians to database...")
            file = open("loomians.json")
            data = json.load(file)
            looms_tupArr = []
            for i in data:
                looms_tupArr.append((i['id'], i['name'], "Esc"))
            cursor.executemany("""INSERT INTO loomians VALUES (?, ?, ?)""", looms_tupArr)
            file.close()
            print("Database filled!")
            open("loomians.json", "w").close()  # clears loomian JSON file
            connection.commit()
            connection.close()

    def generate_entry(self):
        connection = sqlite3.connect("loomianlegacy.db")
        cursor = connection.cursor()
        if not self.entry_out:
            print(self.message)
            cursor.execute("""SELECT * FROM loomians""")
            database = cursor.fetchall()
            for entry in database:
                Database.loom_entry(self.master, entry[0], entry[1], entry[2])
            self.entry_out = True
        elif self.entry_out:
            for entry_frame in self.master.winfo_children():
                entry_frame.destroy()
            self.entry_out = False
            self.message = "Refreshing database entries..."
            Database.generate_entry(self)
        connection.commit()
        connection.close()

    @staticmethod
    def reset():
        print("Resetting database to default...")
        Database.scrape_looms()
        Database.generate_entry()

    @staticmethod
    def get_db_entry():
        name = entry_box.get()
        connection = sqlite3.connect("loomianlegacy.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM loomians")
        entries = cursor.fetchall()
        for entry in entries:
            if entry[1] == name:
                return entry[0], entry[1]
        connection.commit()
        connection.close()
        print("Input a Loomian that is in the database, make sure there are no spaces.")
        print("\t^^^If the Loomian you are looking for is new, download newer bot version.")
        return None, None

    @staticmethod
    def db_update(loom_id: str, name: str, action: str):
        connection = sqlite3.connect("loomianlegacy.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE loomians SET action = '{}' WHERE name = '{}'".format(action, name))  # 99 columns
        connection.commit()
        connection.close()
        entry_box.delete(0, customtkinter.END)
        print("Set action of [Loomian: {}] {} as {}. Please refresh to see changes."
              .format(loom_id, name, action))

    @staticmethod
    def update_atk1():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Atk1")

    @staticmethod
    def update_atk2():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Atk2")

    @staticmethod
    def update_atk3():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Atk3")

    @staticmethod
    def update_atk4():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Atk4")

    @staticmethod
    def update_alert():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Alert")

    @staticmethod
    def update_escape():
        loom_id, name = Database.get_db_entry()
        if loom_id is None:
            return None
        Database.db_update(loom_id, name, "Esc")


class ModeAttr:     # class for storing and passing mode attributes

    def __init__(self):
        self.noise = customtkinter.StringVar(value="Off")
        self.error = customtkinter.StringVar(value="20")
        self.chat = customtkinter.StringVar(value="Off")
        self.buzz = customtkinter.StringVar(value="1")
        self.ven = customtkinter.StringVar(value="1")
        self.kir = customtkinter.StringVar(value="1")

    def get_noise(self):        # get functions are for passing string arguments to actual bot
        return self.noise.get()

    def get_error(self):
        return self.error.get()

    def get_chat(self):
        return self.chat.get()

    def get_buzz(self):
        return self.buzz.get()

    def get_ven(self):
        return self.ven.get()

    def get_kir(self):
        return self.kir.get()


# ================================================================================================= <100> MAIN
print("\n\nLoading GUI...")
root = customtkinter.CTk()
root.geometry("600x480")
root.title("LoomBot1.5.0 - Loomian Legacy Keyboard Input Emulator Bot by Druid")
root.iconbitmap("images\\Icon.ico")
frameTab = customtkinter.CTkTabview(root, corner_radius=0)
frameTab.pack(padx=10, pady=(0, 10), fill="both", expand="True")
frameTab.add("   ENCOUNTER   ")     # 3 / 3
frameTab.add("   NPC BATTLE   ")    # 3 / 1 / 3
frameTab.add("    AUTO  FISH    ")  # 4 / 2 / 4
frameTab.add("    DATA BASE    ")   # 4 / 1 / 4
frameTab.add("         GUIDE         ")     # 9 / 9
frameTab.add("     SETTINGS     ")  # 5 / 5
mode = ModeAttr()


# ================================================================================================= <100> ENCOUNTER
chat_frame = customtkinter.CTkFrame(frameTab.tab("   ENCOUNTER   "), corner_radius=0)
chat_frame.pack(padx=10, pady=(20, 0), fill="both")
chat_label = customtkinter.CTkLabel(chat_frame, font=("Arial", 24),
                                    text="Input Loomian In Roblox Chat")
chat_label.pack(padx=10, pady=0, side="left")
chat_segBut = customtkinter.CTkSegmentedButton(chat_frame, variable=mode.chat,
                                               values=["On", "Off"], width=50, height=50,
                                               corner_radius=0, border_width=0)
chat_segBut.pack(padx=0, pady=0, side="right")
chat_hint = customtkinter.CTkLabel(frameTab.tab("   ENCOUNTER   "), font=("Arial", 16),
                                   text="""
Turning on this input Loomian in chat option will make it so that the bot will
automatically input the encountered Loomian's name in the in-game Roblox chat
if they are set as alert (when bot triggers alarm). It is recommended to turn
this option off, because it may seem odd for others."""
                                   )
chat_hint.pack(padx=0, pady=0)
start_encounter = customtkinter.CTkButton(frameTab.tab("   ENCOUNTER   "), font=("Arial", 24),
                                          hover_color="#3B3B3B", text="Start(800x630px only)",
                                          corner_radius=0, width=500, height=50,
                                          command=encounter_start)
start_encounter.pack(padx=10, pady=(0, 20), side="bottom")
start_hint = customtkinter.CTkLabel(frameTab.tab("   ENCOUNTER   "), font=("Arial", 16),
                                    text="Bot will detect the 'menu' icon. Please read guide.")
start_hint.pack(padx=0, pady=0, side="bottom")
set_win_button = customtkinter.CTkButton(frameTab.tab("   ENCOUNTER   "), fg_color="#2B2B2B",
                                         hover_color="#3B3B3B", command=set_window,
                                         font=("Arial Bold", 16), text=
                                         ">CLICK TO AUTOMATICALLY SET UP WINDOWS<")
set_win_button.pack(padx=10, pady=10, side="bottom")


# ================================================================================================= <100> NPC BATTLE


# ================================================================================================= <100> DATABASE
db = Database()
entry_box = customtkinter.CTkEntry(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                   corner_radius=0, width=175, height=50,
                                   placeholder_text="Loomian Name")
entry_box.pack(padx=(10, 0), pady=10, side="left")
db_atk1 = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                  corner_radius=0, width=50, height=50, text="⚔️1",
                                  fg_color="orange", hover_color="#3B3B3B",
                                  command=db.update_atk1)
db_atk1.pack(padx=0, pady=10, side="left")
db_atk2 = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                  corner_radius=0, width=50, height=50, text="⚔️2",
                                  fg_color="orange", hover_color="#3B3B3B",
                                  command=db.update_atk2)
db_atk2.pack(padx=0, pady=10, side="left")
db_atk3 = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                  corner_radius=0, width=50, height=50, text="⚔️3",
                                  fg_color="orange", hover_color="#3B3B3B",
                                  command=db.update_atk3)
db_atk3.pack(padx=0, pady=10, side="left")
db_atk4 = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                  corner_radius=0, width=50, height=50, text="⚔️4",
                                  fg_color="orange", hover_color="#3B3B3B",
                                  command=db.update_atk4)
db_atk4.pack(padx=0, pady=10, side="left")
db_alert = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                   corner_radius=0, width=50, height=50, text="⏰",
                                   fg_color="red", hover_color="#3B3B3B",
                                   command=db.update_alert)
db_alert.pack(padx=0, pady=10, side="left")
db_escape = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                    corner_radius=0, width=50, height=50, text="🏃",
                                    fg_color="green", hover_color="#3B3B3B",
                                    command=db.update_escape)
db_escape.pack(padx=0, pady=10, side="left")
gen_button = customtkinter.CTkButton(frameTab.tab("    DATA BASE    "), font=("Arial", 24),
                                     corner_radius=0, width=50, height=50, text="🔄",
                                     hover_color="#3B3B3B", command=db.generate_entry)
gen_button.pack(padx=10, pady=10, side="right")


# ================================================================================================= <100> SETTINGS
noise_frame = customtkinter.CTkFrame(frameTab.tab("     SETTINGS     "), corner_radius=0)
noise_frame.pack(padx=10, pady=(20, 0), fill="both")
noise_label = customtkinter.CTkLabel(noise_frame, font=("Arial", 24),
                                     text="Noise (Text 2 Speech Feature)")
noise_label.pack(padx=10, pady=0, side="left")
noise_segBut = customtkinter.CTkSegmentedButton(noise_frame, variable=mode.noise,
                                                values=["On", "Off"], width=50, height=50,
                                                corner_radius=0, border_width=0)
noise_segBut.pack(padx=0, pady=0, side="right")
noise_hint = customtkinter.CTkLabel(frameTab.tab("     SETTINGS     "), font=("Arial", 16),
                                    text="""
The noise option is basically the text to speech feature of the bot. It is used
as alarms for important moments during the runtime of a bot in the game. When
this is turned off, the alarm feature of the bot will be silent."""
                                    )
noise_hint.pack(padx=0, pady=0)
error_frame = customtkinter.CTkFrame(frameTab.tab("     SETTINGS     "), corner_radius=0)
error_frame.pack(padx=10, pady=(20, 0), fill="both")
error_label = customtkinter.CTkLabel(error_frame, font=("Arial", 24),
                                     text="Max Number Of Errors")
error_label.pack(padx=10, pady=0, side="left")
error_segBut = customtkinter.CTkSegmentedButton(error_frame, variable=mode.error, width=50,
                                                height=50, values=["10", "20", "30", "40"],
                                                corner_radius=0, border_width=0)
error_segBut.pack(padx=0, pady=0, side="right")
error_hint = customtkinter.CTkLabel(frameTab.tab("     SETTINGS     "), font=("Arial", 16),
                                    text="""
The max number of errors variable makes the bot able to stop whenever the
bot keeps getting specific errors repeatedly. I recommend to set
this to 40 if you are closely supervising, and 10 if no. You can also pick 20
or 30 depending on your hunch. Note that 20 is good by default."""
                                    )
error_hint.pack(padx=0, pady=0)
reset_frame = customtkinter.CTkFrame(frameTab.tab("     SETTINGS     "), corner_radius=0)
reset_frame.pack(padx=10, pady=(20, 0), fill="both")
reset_label = customtkinter.CTkLabel(reset_frame, font=("Arial", 24),
                                     text="Reset Database To Default")
reset_label.pack(padx=10, pady=0, side="left")
reset_button = customtkinter.CTkButton(reset_frame, font=("Arial", 24), width=50, height=50,
                                       corner_radius=0, text="🔄", hover_color="#3B3B3B",
                                       fg_color="red", command=db.reset)
reset_button.pack(padx=0, pady=0, side="right")


# ================================================================================================= <100> CLOSE
print("Ready!\n")
print("This is the console of the bot, which outputs important information.")
print("I prefer you read the guide before starting with any mode of the bot. Good luck!")
print("You might want to reopen the program if it suddenly stops working when it used to.\n")
root.mainloop()
# 330 - 7/11/2023, 8:49 AM [ none ] : Encounter Tab, Settings Tab, Database Tab
# For version updates: Always renew version number in this file (i.e. LoomBotx.x.x)
# Notes: Lines must be BELOW 100 columns
