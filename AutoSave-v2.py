import customtkinter
import multiprocessing
import time
import pyautogui
import threading
from threading import Event

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x400")
app.wm_title("Auto Saver")

intervall = 1
saveStopEvent = Event()

def button_event():
    global intervall
    global saveStopEvent
    inputNumber = IntervallInput.get()
    inputNumber = inputNumber.replace(",", ".")
    if button.cget("text") == "Start":
        try:
            intervall = float(inputNumber)
        except ValueError:
            print("Invalid input intervall")
            return
        if(intervall <= 0):
            print("You have to enter a positive intervall")
            return
        saveStopEvent = Event()
        SaveThread = threading.Thread(target=save_loop, args=(saveStopEvent,))
        SaveThread.setDaemon(True)
        SaveThread.start()
        button.configure(text="Stop")
    else:
        button.configure(text="Start")
        saveStopEvent.set()

def save_loop(saveStopEvent):
    while True:
        if(saveStopEvent.is_set()):
            break
        pyautogui.hotkey("ctrl", "s")
        time.sleep(intervall)


button = customtkinter.CTkButton(master=app, text="Start", command=button_event)
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

IntervallInput = customtkinter.CTkEntry(master=app, width=100, placeholder_text="Intervall (secs)")
IntervallInput.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

Title = customtkinter.CTkLabel(master=app, text="Welcome to Auto Saver!", width=120, height=25)
Title.configure(font=("Arial", 30)) 

Title.place(relx=0.5, rely=0.1, anchor=customtkinter.N)

app.mainloop()