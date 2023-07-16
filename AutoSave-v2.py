import customtkinter
import multiprocessing
import time
import pyautogui
import threading
import win32gui
from threading import Event

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x400")
app.wm_title("Auto Saver")

saveWindowHandler = ""
currentWindowHandler = win32gui.GetForegroundWindow()
OpenWindowHandlers = list()

intervall = 1
saveStopEvent = Event()

def removeErrorMessage():
    time.sleep(3.5)
    ErrorDisplay.configure(text="")


def button_event():
    global intervall
    global saveStopEvent
    inputNumber = IntervallInput.get()
    inputNumber = inputNumber.replace(",", ".")
    if button.cget("text") == "Start":
        try:
            intervall = float(inputNumber)
        except ValueError:
            ErrorDisplay.configure(text="Error: You have to enter a valid intervall number")
            RemoveErrorThread = threading.Thread(target=removeErrorMessage)
            RemoveErrorThread.daemon = True
            RemoveErrorThread.start()
            return
        if(intervall < 1):
            ErrorDisplay.configure(text="Error: You should pick an intervall length above 1")
            RemoveErrorThread = threading.Thread(target=removeErrorMessage)
            RemoveErrorThread.daemon = True
            RemoveErrorThread.start()
            return
        saveStopEvent = Event()
        SaveThread = threading.Thread(target=save_loop, args=(saveStopEvent,))
        SaveThread.daemon = True
        SaveThread.start()
        button.configure(text="Stop")
    else:
        button.configure(text="Start")
        saveStopEvent.set()

def save_loop(saveStopEvent):
    global saveWindowHandler
    global currentWindowHandler
    global OpenWindowHandlers
    while True:
        if(saveStopEvent.is_set()):
            break
        if(saveWindowHandler == ""):
            saveWindowHandler = OpenWindowHandlers.index(0)
        currentWindowHandler = win32gui.GetForegroundWindow()
        FocusWindow(saveWindowHandler)
        pyautogui.hotkey("ctrl", "s")
        FocusWindow(currentWindowHandler)
        time.sleep(intervall)


button = customtkinter.CTkButton(master=app, text="Start", command=button_event)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

IntervallInput = customtkinter.CTkEntry(master=app, width=100, placeholder_text="Intervall (secs)")
IntervallInput.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

Title = customtkinter.CTkLabel(master=app, text="Welcome to Auto Saver!", width=120, height=25)
Title.configure(font=("Arial", 30)) 
Title.place(relx=0.5, rely=0.1, anchor=customtkinter.N)

SaveApplicationCaption = customtkinter.CTkLabel(master=app, text="Save Application:", width=120, height=25)
SaveApplicationCaption.configure(font=("Arial", 15))
SaveApplicationCaption.place(relx=0.35, rely=0.7, anchor=customtkinter.CENTER)

ErrorDisplay = customtkinter.CTkLabel(master=app, text="", width=120, height=25)
ErrorDisplay.configure(font=("Arial", 12), text_color = '#F20505')	
ErrorDisplay.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

# Code for choosing to focus for saving
combobox = customtkinter.CTkComboBox(master=app, values=["Empty"], width=120, height=25)
combobox.place(relx=0.65, rely=0.7, anchor=customtkinter.CENTER)
OpenWindows = list()
def processWindow(currentWindowHandler, _):
    global OpenWindowHandlers
    global OpenWindows
    if win32gui.IsWindowVisible(currentWindowHandler) and win32gui.GetWindowText(currentWindowHandler) != "":
        OpenWindows.append(win32gui.GetWindowText(currentWindowHandler))
        OpenWindowHandlers.append(currentWindowHandler)

oldwindowlength = 0
def UpdateDropDown(choice):
    global OpenWindows
    global oldwindowlength
    global OpenWindowHandlers
    OpenWindows.clear()
    OpenWindowHandlers.clear()
    win32gui.EnumWindows(processWindow, None)
    windowsChanged = False
    if(oldwindowlength != len(OpenWindows)):
        windowsChanged = True
    if(windowsChanged):
        oldwindowlength = len(OpenWindows)
        combobox.configure(values=OpenWindows)
        combobox.set(OpenWindows[0])


def WindowUpdateLoop():
    while True:
        UpdateDropDown("none")
        time.sleep(3)

def FocusWindow(WindowToFucus):
    win32gui.BringWindowToTop(WindowToFucus)
    win32gui.SetForegroundWindow(WindowToFucus)

def WindowChoiceHandler(choice):
    global saveWindowHandler
    global OpenWindowHandlers
    saveWindowHandler = OpenWindowHandlers[OpenWindows.index(choice)]

combobox.configure(command=WindowChoiceHandler)
WindowUpdateThread = threading.Thread(target=WindowUpdateLoop)
WindowUpdateThread.daemon = True
WindowUpdateThread.start()

app.mainloop()