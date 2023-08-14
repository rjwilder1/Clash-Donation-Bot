import datetime
import os
import subprocess
import time
import pyautogui
import pytesseract
import pygetwindow
import numpy as np
import random
import cv2
import threading
from PIL import Image, ImageFilter
import easyocr
import io
from PIL import ImageEnhance, Image

class Funcs:
    def __init__(self):
        self.FoundWindow = False
        self.Resetting = False
        #self.HardResetting = False
        self.Disabled = False
        self.ResetIntervalMinutes = 60
        self.IdleIntervalMinutes = 4
        self.MaxTimeoutSeconds = 15
        self.Donations = 0
        self.buffer = io.BytesIO()
        self.ocr = easyocr.Reader(["en"])
        self.Uptime = 0
        #self.StartTime = self.gettime()

        self.Icon = "Images\ICON.png"
        self.ClashIcon = "Images\ClashIcon.png"
        self.ClearAll = "Images\ClearAll.png"
        self.Trophy = "Images\Trophy.png"
        self.OpenChat = "Images\OpenChat.png"
        self.CloseChat = "Images\CloseChat.png"
        self.BottomChat = "Images\BottomChat.png"#Possibly delete?
        self.EnterTroops = "Images\EnterTroops.png"
        self.TrainTroopsIMG = "Images\TrainTroops.png"
        self.Dragon = "Images\Dragon.png"
        self.BrewSpells = "Images\BrewSpells.png"
        self.RageSpell = "Images\RageSpell.png"
        self.X = "Images\X.png"
        self.DonateButton = "Images\Donate_Button.png"
        self.QuickDonate = "Images\Quick_Donate.png"
        self.DragonDonate = "Images\DragonDonate.png"
        self.RageSpellDonate = "Images\RageSpellDonate.png"
        self.DonateSuperTroop = "Images\DonateSuperTroop.png"
        self.DonateNormalTroop = "Images\DonateNormalTroop.png"
        self.BuildSiegeMachine = "Images\BuildSiegeMachine.png"
        self.Blimp = "Images\Blimp.png"
        self.Chat = "Images\Chat.png"
        self.SendChatIMG = "Images\SendChat.png"#Could remove idk BackCW.png
        self.Reload = "Images\Reload.png"
        #CW
        self.CWBack = "Images\BackCW.png"
        self.CWGoBack = "Images\CWGoBack.png"
        self.CWForward = "Images\ForwardCW.png"
        self.CWReturnHome = "Images\ReturnHome.png"
        self.CWButton = "Images\ClanWarButton.png"
        self.CWDonate = "Images\CWDonate.png"
        self.CWQuickDonate = "Images\CWQuickDonate.png"
        self.CWMe = "Images\LegacyWRLDCW.png"
        self.CWSuperMinion = "Images\CWSuperMinion.png"
        self.CWMinion = "Images\CWMinion.png"
        self.CWArcher = "Images\CWArcher.png"
        self.CWIceGolem = "Images\CWIceGolem.png"
        self.CWNight = "Images\CWNight.png"
        #SwitchAccount
        self.SK = "Images\SK.png"
        self.LegacyWRLD = "Images\LegacyWRLD.png"
        self.SwitchAccountButton = "Images\SwitchButton.png"
        self.SwitchSettings = "Images\Settings.png"
        #Lists
        self.banned = ["Velixity"]
        self.AuthUsers = ["Legacy", "LegacyWRLD", "king", "iNeverTriple", "Strikers6699", "-$Cam$-", "DallasCowboys"]
        
        self.ResetThread()
        self.ResetThread2()
        self.UpTimeFunc()

    def SwitchAccount(self, who="SK"):
        if self.Resetting: return
        img = self.CheckImage(self.SwitchSettings)
        if img: 
            self.Click(img)
            self.Click(self.WaitUntilImage(self.SwitchAccountButton))
            if who == "SK":
                self.Click(self.WaitUntilImage(self.SK)) 
            else:
                self.Click(self.WaitUntilImage(self.LegacyWRLD))
                self.DonateWarCC()

    def DonateWarCC(self, event=None):
        while not self.CheckImage(self.Trophy): time.sleep(0.5)
        self.Click(self.WaitUntilImage(self.CWButton))
        self.Click(self.WaitUntilImage(self.CWMe))

        while not self.CheckImage(self.CWBack): time.sleep(0.5)

        while not self.CheckRGB(pyautogui.pixel(511, 886), (166, 166, 166)):
            pyautogui.click(511, 886)
            time.sleep(0.1)

        AlreadyIn = False
        while True:
            if not self.CheckRGB(pyautogui.pixel(639, 849), (148, 148, 148)): 
                if not AlreadyIn:
                    AlreadyIn = True
                    pyautogui.click(639, 849)
                    self.Click(self.WaitUntilImage(self.CWQuickDonate))
                    self.WaitUntilImage(self.CWGoBack)
                self.Click(self.CheckImage(self.CWSuperMinion), amt=3)
                #DRAG
                time.sleep(1)
                pyautogui.mouseDown(1100, 363)
                pyautogui.moveTo(425, 363)
                pyautogui.mouseUp()
                time.sleep(2)
                self.Click(self.CheckImage(self.CWIceGolem), amt=2)
                    #time.sleep(0.5)

                self.Click(self.CheckImage(self.CWNight), amt=1)
                time.sleep(1)

                pyautogui.mouseDown(425, 363)
                pyautogui.moveTo(1100, 363)
                pyautogui.mouseUp()

                time.sleep(2)
                self.Click(self.CheckImage(self.CWMinion), amt=2)
                pyautogui.click(739, 244, 2)
            time.sleep(0.5)
            if not self.CheckRGB(pyautogui.pixel(1406, 887), (166, 166, 166)):
                #self.Click(self.CheckImage(self.CWForward))
                pyautogui.click(1406, 887)
                time.sleep(1)
            else:
                self.Click(self.CheckImage(self.CWReturnHome))
                time.sleep(1)
                self.EnterChat()
                time.sleep(1)
                self.SendChat(msg = "Finished Donating to War Clan Castles")
                #self.Click(self.CloseChat)
                self.SwitchAccount(who="SK")
                break

    def gettime(self):
        current_time = datetime.datetime.now()
        time_string = "[" + current_time.strftime("%H:%M:%S") + "] "
        return time_string

    def ResetThread(self):
        thread = threading.Thread(target=self.CallBluestacksReset)
        thread.daemon = True
        thread.start()

    def UpTimeFunc(self):
        thread = threading.Thread(target=self.UpTimeCount)
        thread.daemon = True
        thread.start()
    
    def UpTimeCount(self):
        while True:
            self.Uptime += 1
            time.sleep(1)

    def convert_seconds(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        return days, hours, minutes, seconds
    
    def CallBluestacksReset(self):
        while True:
            time.sleep(self.ResetIntervalMinutes * 60)
            self.ResetBlueStacks()

    def ResetThread2(self):
        thread = threading.Thread(target=self.PreventIdle)
        thread.daemon = True
        thread.start()
    
    def PreventIdle(self):
        while True:
            time.sleep(self.IdleIntervalMinutes * 60)
            self.PreventIdleFunction()

    def PreventIdleFunction(self):
        if self.Resetting: return
        img = self.CheckImage(self.CloseChat)
        if img:
            self.Click(img)

    def CheckTeamviewerBS(self):
        AllTitles = pygetwindow.getAllTitles()
        if "Sponsored session" in AllTitles:
            pygetwindow.getWindowsWithTitle("Sponsored session")[0].close()
            print("Closed TeamViewer and reset")
            self.ResetBlueStacks()

    def WaitUntilImage(self, path, conf=0.7, gray=False):
        Timeout = 0
        while (pyautogui.locateCenterOnScreen(path, grayscale=gray, confidence=conf) is None):
            if Timeout >= self.MaxTimeoutSeconds:
                print("Max timeout reached. Resetting...")
                self.ResetBlueStacks()
                break
            time.sleep(1)
            Timeout +=1
        return pyautogui.locateCenterOnScreen(path, grayscale=gray, confidence=conf)
    
    def CheckImage(self, path, conf=0.7, gray=False):
        img = pyautogui.locateCenterOnScreen(path, grayscale=gray, confidence=conf)
        if img is None:
            return False
        return img
    
    def is_grayscale(self, image):
        for pixel in image.getdata():
            if pixel[0] != pixel[1] or pixel[1] != pixel[2]:
                return False
        return True

    def CheckImageGray(self, path, conf=0.7, gray=False):
        bbox = pyautogui.locateOnScreen(path, grayscale=gray, confidence=conf)
        if bbox is None:
            return False
        screenshot = pyautogui.screenshot(region=bbox)
        if self.is_grayscale(screenshot):
            return True
        else:
            return False

    def CheckWindow(self):
        if (pygetwindow.getWindowsWithTitle("BlueStacks App Player")):
            self.FoundWindow = True
            return True
        else:
            self.FoundWindow = False
            return False
    
    def InHomePage(self):
        if self.Resetting == False and self.CheckImage(self.ClashIcon):
            self.WaitUntilImage(self.ClashIcon)
            pyautogui.hotkey('ctrlleft', 'shiftleft', '5')
            img = self.WaitUntilImage(self.ClearAll)
            self.Click(img)
            img = self.WaitUntilImage(self.ClashIcon)
            self.Click(img)
            return True
        return False

    def ResetBlueStacks(self):
        self.Resetting = True
        if self.CheckWindow():
            subprocess.call(["taskkill", "/F", "/IM", "HD-Player.exe"])
            time.sleep(1)
            subprocess.Popen("C:\Program Files\BlueStacks_nxt\HD-Player.exe")
        else:
            subprocess.Popen("C:\Program Files\BlueStacks_nxt\HD-Player.exe")#Just in case
        while (not self.CheckWindow()):
           time.sleep(1)
        window = pygetwindow.getWindowsWithTitle("BlueStacks App Player")[0]
        window.activate()
        newwindow = pygetwindow.getActiveWindow()
        newwindow.maximize()
        self.WaitUntilImage(self.ClashIcon)
        pyautogui.hotkey('ctrlleft', 'shiftleft', '5')
        img = self.WaitUntilImage(self.ClearAll)
        self.Click(img)
        img = self.WaitUntilImage(self.ClashIcon)
        self.Click(img)
        time.sleep(1)
        self.Resetting = False

    def CheckInGame(self):
        if self.Resetting: return
        if self.CheckImage(self.Trophy, conf=0.4): return True
        return False
    
    def CheckInChat(self):
        if self.Resetting: return
        if self.CheckImage(self.BottomChat): return True
        return False

    def EnterChat(self):
        if self.Resetting: return
        if self.CheckInGame():
            img = self.CheckImage(self.OpenChat)
            if img:
                self.Click(img)
                return True
        return False

    def Click(self, image, amt=1):
        if not image: return
        for i in range(0,amt):
            time.sleep(0.5)
            pyautogui.click(image.x, image.y)

    def TrainTroops(self):
        if not self.CheckInChat(): self.EnterChat()
        time.sleep(1)
        img = self.CheckImage(self.CloseChat)
        if img:
            self.Click(img)
            img = self.WaitUntilImage(self.EnterTroops)
            self.Click(img)
            self.WaitUntilImage(self.TrainTroopsIMG, conf=0.85)
            pyautogui.click(500, 100)
            time.sleep(.6)
            pyautogui.click(960, 650, 5)
            time.sleep(.6)
            pyautogui.click(900, 100)
            time.sleep(.6)
            pyautogui.click(400, 700, 5)
            time.sleep(.6)
            pyautogui.click(1200, 100)
            time.sleep(.6)
            pyautogui.click(600, 800, 5)
            time.sleep(.6)
            pyautogui.click(1750, 100)

    def Donate(self):
        if self.Resetting: return
        img = self.CheckImage(self.DonateButton)
        if img:
            if self.CheckBanned(self): return
            self.Click(img)
            self.WaitUntilImage(self.QuickDonate)
            #Regular Donate No Gems
            pyautogui.click(840, 260, 2)
            time.sleep(0.5)
            pyautogui.click(840, 440)
            time.sleep(0.5)
            pyautogui.click(840, 670)
            #Quick Donate
            img = self.CheckImage(self.QuickDonate)
            if img:
                self.Click(img)
                time.sleep(0.5)
                pyautogui.click(840, 260, 5)
                time.sleep(1)
                pyautogui.click(840, 440, 5)
                time.sleep(1)
                pyautogui.click(840, 670, 3)
                time.sleep(1)

                pyautogui.click(970, 260, 5)
                time.sleep(0.5)
                pyautogui.click(970, 440, 5)
                time.sleep(0.5)
                pyautogui.click(970, 670, 2)
                time.sleep(0.5)
            self.Donations += 1
            img = self.CheckImage(self.X)
            if img:
                self.Click(img)
            self.TrainTroops()
            return True
        return False

    def sharpen_image_from_array(self, image_array):
        pil_image = Image.fromarray(image_array)
        pil_image = pil_image.convert("L")
        sharpened_image = pil_image.filter(ImageFilter.SHARPEN)
        sharpened_array = np.array(sharpened_image)
        return sharpened_array

    def GetFilteredTextWhite(self, target_image, lang='eng', conf=None):#WHITE TEXT
        image_np = np.array(target_image)
        image_gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        _, binary_image = cv2.threshold(image_gray, 200, 255, cv2.THRESH_BINARY)
        white_image = Image.fromarray(binary_image)
        sharpened_array = self.sharpen_image_from_array(binary_image)
        sharpened_image = Image.fromarray(sharpened_array)
        extracted_text = ""
        if conf == None:
            extracted_text = pytesseract.image_to_string(sharpened_image, lang=lang)
        else:
            extracted_text = pytesseract.image_to_string(sharpened_image, lang=lang, config=conf)
        return extracted_text
    
    def CheckBanned(self, event=None):#Check da name of requester plus a little more
        left = 50
        top = 525
        width = 700 - left
        height = 800 - top
        screen_image = pyautogui.screenshot()
        target_image = screen_image.crop((left, top, left + width, top + height))
        text = self.ClearSimilar(pytesseract.image_to_string(target_image))

        for i in self.banned:
            if self.ClearSimilar(i) in text:
                return True
            
    def Gems(self, event=None):
        left = 1680
        top = 363
        width = 1815 - left
        height = 400 - top
        screen_image = pyautogui.screenshot()
        target_image = screen_image.crop((left, top, left + width, top + height))
        NoNumbers = r'--oem 3 --psm 6 -c tessedit_char_whitelist="1234567890"'
        text = self.GetFilteredTextWhite(target_image, conf=NoNumbers)
        return text

    def ClearSimilar(self, txt):
        return txt.replace('i', '').replace('I', '').replace('l', '').replace('L', '').replace('1', '').lower()

    def ReadChatWhite(self, event=None):
        left = 50
        top = 810
        width = 700 - left
        height = 940 - top
        #pyautogui.screenshot().crop((left, top, left + width, top + height)).convert('L').save("TEST.png")
        ImageEnhance.Contrast(pyautogui.screenshot().crop((left, top, left + width, top + height)).convert('L')).enhance(2).save(self.buffer, format="PNG")
        txt = self.ClearSimilar(' '.join([detection[1] for detection in self.ocr.readtext(self.buffer.getvalue())]))
        self.buffer.seek(0)
        self.buffer.truncate()
        return txt

    def CheckRGB(self, pixel, target, tolerance=25):
        return all(abs(p - t) <= tolerance for p, t in zip(pixel, target))
    
    def SendChat(self, event=None, msg="No chat entered..."):
        count = 0
        ChatImg = self.CheckImage(self.Chat)
        if ChatImg:
            self.Click(ChatImg)
            while True:
                count +=1
                if count >=60:
                    print("Error with getting chat...")
                    self.ResetBlueStacks()
                if self.CheckRGB(pyautogui.pixel(1000, 1050), (254, 254, 254)):
                    break
                time.sleep(0.5)
            time.sleep(0.7)
            pyautogui.typewrite(msg)
            time.sleep(random.uniform(0.7, 1.3))
            pyautogui.press('enter')

    def CheckCommand(self, event=None):
        cmd = self.ReadChatWhite()
        Authed = False
        for i in self.AuthUsers:
            if self.ClearSimilar(i) in cmd:
                Authed = True
                break

        if not Authed: return False

        if self.ClearSimilar("Disable") in cmd:
            self.Disabled = True
            self.SendChat(msg="Donating is disabled")

        elif self.ClearSimilar("Donate War CC") in cmd:
            self.SendChat(msg="Donating to war Clan Castles, this may take a while")
            self.SwitchAccount(who="LegacyWRLD")

        elif self.ClearSimilar("Enable") in cmd:
            self.Disabled = False
            self.SendChat(msg="Donating is enabled")

        elif self.ClearSimilar("Donations") in cmd or self.ClearSimilar("Donabions") in cmd:
            self.SendChat(msg="Donated a total of " + str(self.Donations) + " times")

        elif self.ClearSimilar("Status") in cmd or self.ClearSimilar("Sbabus") in cmd or self.ClearSimilar("Stabus") in cmd or self.ClearSimilar("Sbatus") in cmd:
            if self.Disabled: 
                self.SendChat(msg="Donating is currently disabled")
            else:
                self.SendChat(msg="Donating is currently enabled")

        elif self.ClearSimilar("Banned") in cmd:
            self.SendChat(msg="User banned: " + (", ".join(self.banned)))
        
        elif self.ClearSimilar("Uptime") in cmd or self.ClearSimilar("Upbime") in cmd:
            days, hours, minutes, seconds = self.convert_seconds(self.Uptime)
            self.SendChat(msg="Total time up: " + f"{str(days)} days, {str(hours)} hours, {str(minutes)} minutes, and {str(seconds)} seconds.")

        elif self.ClearSimilar("Auth") in cmd or self.ClearSimilar("Aubh") in cmd: self.SendChat(msg="Users allowed to use commands: " + (", ".join(self.AuthUsers)))
        elif self.ClearSimilar("Gems") in cmd: self.SendChat(msg="Total gems left: " + self.Gems())

        elif self.ClearSimilar("Pause") in cmd:
            self.SendChat(msg="Pausing for 120 seconds")
            time.sleep(120)

        elif self.ClearSimilar("Hard Reset") in cmd or self.ClearSimilar("Hard Reseb") in cmd:
            self.SendChat(msg="Hard resetting...")
            self.ResetBlueStacks()

        return False

    def CheckMaximized(self):
        if self.CheckImage(self.Icon, conf=0.6):
            print("Reset due to maximize error.")
            self.ResetBlueStacks()
            return True
        return False
    
    def CheckReload(self, event=None):
        img = self.CheckImage(self.Reload)
        if img:
            self.Click(img)
            time.sleep(1)
            self.SendChat(msg = "Back from being reloaded")
            return True
        return False

    def Start(self):
        self.CheckTeamviewerBS()
        if self.Resetting: return
        pyautogui.hotkey("ctrl", "shift", "t")
        if not self.InHomePage(): pass
        if not self.CheckMaximized(): pass
        if not self.CheckInGame(): pass
        if not self.CheckInChat(): pass
        if not self.EnterChat(): pass
        if not self.CheckCommand(): pass
        if not self.CheckReload(): pass
        if self.Disabled: return
        if not self.Donate(): pass

if __name__ == "__main__":
    self = Funcs()
    print("Users banned: " + (", ".join(self.banned)))
    print("Users authorized: " + (", ".join(self.AuthUsers)))
    self.ResetBlueStacks()
    #import keyboard
    #keyboard.on_press_key('/', self.DonateWarCC)
    #keyboard.wait()
    while True:
        time.sleep(2)
        self.Start()