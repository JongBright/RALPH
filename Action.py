import os
import threading
import wmi
import time
from datetime import datetime, timedelta
import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# import phonenumbers
# from phonenumbers import geocoder
# from phonenumbers import carrier
# from opencage.geocoder import OpenCageGeocode
# import folium
import subprocess
import winshell
import webbrowser
from urllib.request import urlopen
import requests
import json
import random
import shutil
import psutil
import cv2
import mediapipe as mp
#import autopy
import numpy as np
import math
from math import floor, log
from pynput.keyboard import Key, Controller
#import nltk
import neattext as nt
import spacy
import GPUtil
import win32api
import win32gui
from win10toast import ToastNotifier















#function for controlling microphone
def toggle_microphone():
    try:
        WM_APPCOMMAND = 0x319
        APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None, APPCOMMAND_MICROPHONE_VOLUME_MUTE)
        return True
    except:
        return False




#update paths                 update paths
def update_paths():
    pictures = {}
    audios = {}
    videos = {}
    apps = {}
    filesz = {}
    roots = set()
    def filesLoader():
        drives = win32api.GetLogicalDriveStrings()
        available_pc_drives = drives.split('\000')[:-1]
        intitial_dir = os.getcwd()
        for pc_drive in available_pc_drives:
            try:
                os.chdir(pc_drive)
                for root, dirs, files in os.walk(pc_drive):
                    roots.add(root)
                    for file in files:
                        if (file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.gif')):
                            pictures.update({file: os.path.join(root, file)})
                            #filesz.update({file: os.path.join(root, file)})
                        if file.endswith('.mp3'):
                            audios.update({file: os.path.join(root, file)})
                            #filesz.update({file: os.path.join(root, file)})
                        if file.endswith('.mp4'):
                            videos.update({file: os.path.join(root, file)})
                            #filesz.update({file: os.path.join(root, file)})
                        if file.endswith('exe'):
                            apps.update({file: os.path.join(root, file)})
                        if (file.endswith('.txt') or file.endswith('.rar') or file.endswith('.iso') or file.endswith('.zip') or file.endswith('.csv') or file.endswith('.docx') or file.endswith('.xlsx') or file.endswith('.pdf')):
                            filesz.update({file: os.path.join(root, file)})
            except:
                pass
            finally:
                os.chdir(str(intitial_dir))
                try:
                    with open('_ralph_memory.txt', 'w', encoding="utf-8") as rm:
                        rm.write(str(pictures) + '\n')
                        rm.write(str(audios) + '\n')
                        rm.write(str(videos) + '\n')
                        rm.write(str(apps) + '\n')
                        rm.write(str(filesz) + '\n')
                        rm.write(str(roots) + '\n')
                        rm.close()
                except:
                    print('error')
        #print(pictures, audios, videos, filesz, roots)
    try:
        filesLoader()
        return pictures, audios, videos, apps, filesz, roots
    except:
        return False



#function for getting time:                 time
def get_time():
    try:
        now = datetime.today()
        c_time = now.strftime("%H:%M %p")

        return c_time
    except:
        return False



#function for getting date:                  date
def get_date():
    try:
        now = time.asctime(time.localtime())
        p_now = ([now])[0].split()
        temp = []
        for i in p_now:
            if ':' not in i:
                temp.append(i)
        d = ''
        for i in temp:
            d += i + ' '
        c_date = d[:-1]

        return c_date
    except:
        return False



#function for setting reminders                        set reminder
def set_Reminder(reminder_message, alarm_time):
    def time_in_seconds(t):
        global secsleft
        time = t
        if time[-1] == '.':
            period = time[time.index(' '):-1]
        else:
            period = time[time.index(' '):]
        if period == ' a.m' or period == ' am':
            timestrip = time.rstrip(period)
            timesplit = timestrip.split(':')
            hr = int(timesplit[0])
            min = int(timesplit[1])
            now = datetime.now()
            secsleft = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))
        elif period == ' p.m' or period == ' pm':
            timestrip = time.rstrip(period)
            timesplit = timestrip.split(':')
            hr = int(timesplit[0]) + 12
            min = int(timesplit[1])
            now = datetime.now()
            secsleft = int((timedelta(hours=24) - (now - now.replace(hour=hr, minute=min, second=0, microsecond=0))).total_seconds() % (24 * 3600))
        else:
            secsleft = 'None'

        return secsleft

    alarm_time_secsleft = time_in_seconds(alarm_time)
    reminder_message = str(reminder_message)
    duration = int(alarm_time_secsleft)
    notificator = ToastNotifier()
    notificator.show_toast('', 'Your reminder has been set.', duration=duration)
    try:
        notificator.show_toast('Reminder', reminder_message, duration=1)
        for i in range(25):
            win32api.Beep(1000, 1000)
    except:
        return False




#function for getting current location:                    location
def get_CurrentLocation():
    location_info = {}
    try:
        url = 'http://ipinfo.io/json'
        res = urlopen(url)
        data = (json.load(res))
        for i, j in data.items():
            if i!= 'readme':
                location_info.update({i: j})

        if len(location_info)>0:
            return location_info
        else:
            return False
    except:
        return False



#function for getting wheather:                 weather
def get_Weather(city):
    #current_city = (location())['city']
    weather_info = {}
    weather_token = 'c0b1dfb21e8e3ab7bc3f33b494f187c1'
    try:
        weather_api = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + weather_token
        data = requests.get(weather_api).json()
        weather_info.update({'wheather description': data['weather'][0]['description']})
        weather_info.update({'temperature': str(round((data['main']['temp']-273.15), 2)) + ' degrees celcius'})
        weather_info.update({'humidity': round((data['main']['humidity']), 2)})
        weather_info.update({'wind speed': round((data['wind']['speed']), 2)})

        if len(weather_info)>0:
            return weather_info
        else:
            return False
    except:
        return False



#function for getting telephone number location:                      track tel-number
# def get_PhoneNumberLocation(number):
#     if '+' not in number:
#         phone_number = '+' + str(number)
#     else:
#         phone_number = str(number)
#
#     try:
#         parsed_phone_number = phonenumbers.parse(phone_number)
#         num_country = geocoder.description_for_number(parsed_phone_number, 'en')
#         #num_network = carrier.name_for_number(parsed_phone_number, 'en')
#         geoCoder = OpenCageGeocode(key='07b90311690746829b129c202157f252')
#         loc = geoCoder.geocode(str(num_country))
#         latitude, longditude = loc[0]['geometry']['lat'], loc[0]['geometry']['lng']
#         number_location = folium.Map(location=[latitude, longditude], zoom_start=9)
#         folium.Marker([latitude, longditude], popup=num_country).add_to(number_location)
#         init_dir = os.getcwd()
#         desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
#         os.chdir(desktop_path)
#         number_location.save(f'{phone_number}_location.html')
#         webbrowser.open('file://' + os.path.realpath(f'{phone_number}_location.html'))
#         os.chdir(init_dir)
#
#         return True
#     except:
#         return False




#function for getting battery percentage:                  pc battery details
def get_Battery_details():
    def convertTime(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "%d:%02d:%02d" % (hours, minutes, seconds)

    battery_info = {}
    try:
        battery = psutil.sensors_battery()
        battery_info.update({'battery percentage': str(battery.percent) + ' percent'})
        battery_info.update({'battery charging': battery.power_plugged})
        battery_info.update({'battery time left': convertTime(battery.secsleft)})

        if len(battery_info)>0:
            return battery_info
        else:
            return False
    except:
        return False




#function for decreasing screen brightness:                  decrease brightness
def decrease_screen_brightness():
    pvr_brightness = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness
    current_brightness = int(pvr_brightness - 10)
    c = wmi.WMI(namespace='wmi')
    method = c.WmiMonitorBrightnessMethods()[0]
    try:
        method.WmiSetBrightness(current_brightness, 0)
        return True
    except:
        return False



#function for increasing screen brightness:               increase brightness
def increase_screen_brightness():
    pvr_brightness = wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness
    current_brightness = int(pvr_brightness + 50)
    c = wmi.WMI(namespace='wmi')
    method = c.WmiMonitorBrightnessMethods()[0]
    try:
        method.WmiSetBrightness(current_brightness, 0)
        return current_brightness
    except:
        return False



#function for decreasing pc volume:                decrease volume
def decrease_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    pvr_volume = volume.GetMasterVolumeLevel()
    current_value = int(pvr_volume - 2)
    try:
        volume.SetMasterVolumeLevel(current_value, None)
        return True
    except:
        return False



#function for increasing pc volume:                  increase volume
def increase_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    pvr_volume = volume.GetMasterVolumeLevel()
    current_value = int(pvr_volume + 2)
    try:
        volume.SetMasterVolumeLevel(current_value, None)
        return True
    except:
        return False



#function for muting pc                       mute pc
def Mute_pc():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    try:
        volume.SetMasterVolumeLevel(-65, None)
        return True
    except:
        return False



#function for unmuting pc                      unmute pc
def Unmute_pc():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    try:
        volume.SetMasterVolumeLevel(0, None)
        return True
    except:
        return False



#function for getting harddisk details                    pc harddisk details
def get_Harddisk_details():
    def format_bytes(size):
      try:
          logg = 0 if int(size) <= 0 else floor(log(int(size), 1024))
          return f"{round(int(size) / 1024 ** logg, 2)} {['B', 'KB', 'MB', 'GB', 'TB'][int(logg)]}"
      except:
          pass
    harddisk_info = {}
    try:
        c = wmi.WMI ()
        for d in c.Win32_LogicalDisk():
            if d.Size!=None:
                drive, totalSpace, usedSpace, freeSpace = d.Caption, format_bytes(d.Size), format_bytes((int(d.Size) - int(d.FreeSpace))), format_bytes(d.FreeSpace)
                info = { 'drive' + ' ' + drive[:-1]: f'total space: {totalSpace}, used space: {usedSpace}, free space: {freeSpace}' }
                harddisk_info.update(info)

        if len(harddisk_info)>0:
            return harddisk_info
        else:
            return False
    except:
        return False



#function for getting cpu details                    pc cpu details
def get_CPU_details():
    cpu_info = {}
    try:
        cpufreq = psutil.cpu_freq()
        temp = []
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            temp.append(percentage)
        cpu_info.update({
            "Physical cores": psutil.cpu_count(logical=False),
            "Total processors": psutil.cpu_count(logical=True),
            "Total CPU Usage": f'{(sum(temp)/psutil.cpu_count(logical=True)):.2f}%',
            "Max frequency": f'{cpufreq.max:.2f}Mhz',
            "Min Frequency": f'{cpufreq.min:.2f}Mhz',
            "Current Frequency": f'{cpufreq.current:.2f}Mhz'
        })

        if len(cpu_info)>0:
            return cpu_info
        else:
            return False
    except:
        return False



#function for getting gpu details                    gpu details
def get_GPU_details():
    gpu_info = {}
    gpus = GPUtil.getGPUs()
    try:
        for gpu in gpus:
            gpu_info.update({
                "gpu id": gpu.id,
                "gpu name": gpu.name,
                "Total gpu memory": f'{gpu.memoryTotal}MB',
                "Free gpu memory": f'{gpu.memoryFree}MB',
                "Used gpu memory": f'{gpu.memoryUsed}MB',
                "Used gpu memory percentage": f'{gpu.load*100}%',
                "gpu temperature": f'{gpu.temperature} °C',
                "gpu uuid": gpu.uuid
            })

        if len(gpu_info)>0:
            return gpu_info
        else:
            return False
    except:
        return False



#function for getting memory details                      memory details
def get_Memory_details():
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    memory_info = {}
    try:
        svmem = psutil.virtual_memory()
        memory_info.update({
            "Total memory": f'{get_size(svmem.total)}',
            "Available memory": f'{get_size(svmem.available)}',
            "Used memory": f'{get_size(svmem.used)}',
            "Used memory percentage": f'{svmem.percent}%'
        })

        if len(memory_info)>0:
            return memory_info
        else:
            return False
    except:
        return False



#function for getting network details                     network details
def get_Network_details():
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    network_info = {}
    try:
        if_addrs = psutil.net_if_addrs()
        net_io = psutil.net_io_counters()
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                network_info.update({"Interface": f'{interface_name}'})
                if str(address.family) == 'AddressFamily.AF_INET':
                    network_info.update({"IP Address": f'{address.address}'})
                    network_info.update({"Netmask": f'{address.netmask}'})
                    network_info.update({"Broadcast IP": f'{address.broadcast}'})
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    network_info.update({"MAC Address": f'{address.address}'})
                    network_info.update({"Netmask": f'{address.netmask}'})
                    network_info.update({"Broadcast MAC": f'{address.broadcast}'})
        network_info.update({"Total Bytes Sent since boot": f'{get_size(net_io.bytes_sent)}'})
        network_info.update({"Total Bytes Received since boot": f'{get_size(net_io.bytes_recv)}'})

        if len(network_info)>0:
            return network_info
        else:
            return False
    except:
        return False



#empty recycle bin:                 empty recycle bin
def empty_recycle_bin():
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=True, sound=True)
        return True
    except:
        return False



#function for google searching:.....................google search
def google_search(query):
    try:
        webbrowser.open('https://www.google.com/search?q=' + str(query))
        return True
    except:
        return False



#function for opening any website:                  website
def open_website(site):
    try:
        if site:
            webbrowser.open_new('https://' + site + '.com')
        return True
    except:
        return False



#function for texting a whatsapp contact:                whatsapp
def message_whatsapp_contact(number, text):
    contact=(str(number)).replace(' ', '')
    print(contact)
    message = (str(text)).replace(' ', '%20')
    try:
        subprocess.Popen(["cmd", "/C", "start https://wa.me/237"+ contact + "?text=" + message], shell=True)
        return True
    except:
        return False


#function for searching on youtube:                     youtube
def search_on_youtube(topic):
    topic = (str(topic)).replace(' ', '%20')
    try:
        webbrowser.open_new('https://www.youtube.com/results?search_query=' + topic)
        return True
    except:
        return False



#function for connecting bluetooth:                 connect bluetooth\
def connect_bluetooth():
    pass



#fuction for disconnecting bluetooth:              disconnect bluetooth\
def disconnect_bluetooth():
    pass



#function for connecting wifi:                 connect wifi
def connect_to_once_connected_wifi(wifi_name):
    target = str(wifi_name.upper())
    try:
        os.system("netsh wlan connect name=\"" + target + "\" ssid=\"" + target + "\" interface=Wi-Fi")
        return True
    except:
        return False



#function for disconnecting wifi:               disconnect wifi
def disconnect_from_connected_wifi():
    try:
        os.system("netsh wlan disconnect interface=Wi-Fi")
        return True
    except:
        return False



#function for taking screenshot..................screenshot
def take_Screenshot():
    keyboard = Controller()
    try:
        keyboard.press(Key.cmd)
        keyboard.release(Key.print_screen)
        keyboard.press(Key.print_screen)
        keyboard.release(Key.cmd)
    except:
        return False



#function for taking selfie.......................selfie
def take_Selfie():
    def snap():
        cap = cv2.VideoCapture(0)
        check = []
        while True:
            _, img = cap.read()

            temp = datetime.now().strftime("%H:%M:%S")
            current_time = temp.replace(':', '-')
            if len(check)==0:
                init_dir = os.getcwd()
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                os.chdir(desktop_path)
                try:
                    os.mkdir('Pictures')
                except:
                    pass
                cv2.imwrite(f'Pictures/{current_time}.jpg', img)
                os.startfile(os.path.realpath(f'Pictures/{current_time}.jpg'))
                os.chdir(init_dir)
                check.append(1)
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
    try:
        func = lambda: snap()
        thread = threading.Thread(target=func)
        thread.setDaemon(True)
        thread.start()

        return True
    except:
        return False




#close a program:                       close program
def close_program(target):
    program = str(target)
    try:
        subprocess.call(["taskkill","/F","/IM", program+".exe"])
        return True
    except:
        return False



#stop a video/videos:                 stop video
def close_video():
    try:
        subprocess.call(["taskkill","/F","/IM","Video.UI.exe"])
        return True
    except:
        return False



#stop an audio/audios:                stop audio
def close_audio():
    try:
        subprocess.call(["taskkill","/F", "/IM","Music.UI.exe"])
        return True
    except:
        return False



#close a picture/pictures:               close picture
def close_photo():
    try:
        subprocess.call(["taskkill","/F","/IM","Microsoft.Photos.exe"])
        return True
    except:
        return False




#function for opening pictures:                      picture
def view_picture(picture, pictures):

    temp = {}
    for k, v in pictures.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    if picture != 'any photo':

        choice = str(picture).lower()
        check = set()
        try:
            for key, values in temp.items():
                if choice in values:
                    pic = pictures[key]
                    check.add(pic)
        except:
            pass
        print(check)
        if len(check)>0:
            for path in check:
                try:
                    os.startfile(path)
                    return True
                except:
                    return False

    else:
        pics = []
        for p in pictures.values():
            pics.append(p)
        c = random.choice(pics)
        try:
            os.startfile(c)
            return True
        except:
            return False



#function for deleting pictures:                      delete
def delete_picture(picture, pictures):

    temp = {}
    for k, v in pictures.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    choice = str(picture).lower()
    check = set()
    try:
        for key, values in temp.items():
            if choice in values:
                pic = pictures[key]
                check.add(pic)
    except:
        pass

    if len(check)>0:
        try:
            for path in check:
                os.remove(path)
            return True
        except:
            return False




#function for playing audios:                    audio
def play_audio(audio, audios):

    temp = {}
    for k, v in audios.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    if audio != 'any audio':

        choice = str(audio).lower()
        check = set()
        try:
            for key, values in temp.items():
                if choice in values:
                    aud = audios[key]
                    check.add(aud)
        except:
            pass
        print(check)
        if len(check)>0:
            for path in check:
                try:
                    os.startfile(path)
                    return True
                except:
                    return False

    else:
        auds = []
        for a in audios.values():
            auds.append(a)
        c = random.choice(auds)
        try:
            os.startfile(c)
            return True
        except:
            return False



#function for deleting audios:                    delete
def delete_audio(audio, audios):

    temp = {}
    for k, v in audios.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    choice = str(audio).lower()
    check = set()
    try:
        for key, values in temp.items():
            if choice in values:
                aud = audios[key]
                check.add(aud)
    except:
        pass
    print(check)

    if len(check)>0:
        try:
            for path in check:
                os.remove(path)
            return True
        except:
            return False



#function for playing videos:                     video
def play_video(video, videos):

    temp = {}
    for k, v in videos.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    if video != 'any video':

        choice = str(video).lower()
        check = set()
        try:
            for key, values in temp.items():
                if choice in values:
                    vid = videos[key]
                    check.add(vid)
        except:
            pass
        print(check)
        if len(check)>0:
            for path in check:
                try:
                    os.startfile(path)
                    return True
                except:
                    return False

    else:
        vids = []
        for v in videos.values():
            vids.append(v)
        c = random.choice(vids)
        try:
            os.startfile(c)
            return True
        except:
            return False



#function for deleting videos:                     video
def delete_video(video, videos):

    temp = {}
    for k, v in videos.items():
        temp.update({k: str(v).lower()})
    #print(temp)
    choice = str(video).lower()
    check = set()
    try:
        for key, values in temp.items():
            if choice in values:
                vid = videos[key]
                check.add(vid)
    except:
        pass
    print(check)

    if len(check)>0:
        try:
            for path in check:
                os.remove(path)
            return True
        except:
            return False



#function for opening an application:                        program
def run_application(application_name, apps):

    temp = {}
    for k, v in apps.items():
        temp.update({str(k).lower(): v})
    #print(temp)
    choice = str(application_name).lower()
    check = set()
    try:
        if (choice+'.exe') in temp.keys():
            for i in apps.values():
                if (choice+'.exe') in str(i).lower():
                    app = temp[(str(choice+'.exe'))]
                    check.add(app)
    except:
        pass
    print(check)

    try:
        if len(check)>0:
            for path in check:
                os.startfile(path)
            return True

    except:
        return False



#fuction for opening a file:                     open file
def open_file(file_name, filesz):

    temp = {}
    for k, v in filesz.items():
        temp.update({str(k).lower(): v})
    #print(temp)
    choice = str(file_name).lower()
    check = set()
    try:
        for f in filesz:
            if (choice) in temp.keys():
                for i in filesz.values():
                    if (choice) in str(i).lower():
                        file = temp[str(choice)]
                        check.add(file)
    except:
        pass
    print(check)

    if len(check)>0:
        try:
            for path in check:
                os.startfile(path)
            return True
        except:
            return False



#fuction for deleting a file:                  delete file
def delete_file(file_name, filesz):

    temp = {}
    for k, v in filesz.items():
        temp.update({str(k).lower(): v})
    #print(temp)
    choice = str(file_name).lower()
    check = set()
    try:
        for f in filesz:
            if (choice) in temp.keys():
                for i in filesz.values():
                    if (choice) in str(i).lower():
                        file = temp[str(choice)]
                        check.add(file)
    except:
        pass
    print(check)

    if len(check)>0:
        try:
            for path in check:
                os.remove(path)
            return True
        except:
            return False



#---------------------------------------------------------------#
def new1(target):
    word = ''
    list1 = target.split(' ')
    list2 = []
    for i in list1:
        i = i.capitalize()
        word+=i
    return word

def new2(target):
    word = ''
    list1 = target.split(' ')
    list2 = []
    word1 = ''
    for i in list1:
        i = i.capitalize()
        list2.append(i)
    for i in list2:
        word+=i+" "
    return (word[:len(word)-1])


#functioning for opening a folder:                    open folder
def open_folder(folder_name, roots):

    folder_path = None
    folder_path_c = None
    folder_path_s = None
    folder_path_s2 = None
    folder_path_s3 = None
    folder_path_s4 = None
    folder_path_s5 = None

    choice=str(folder_name)
    choice_c = choice.upper()
    choice_s = choice.capitalize()
    choice_s2 = new1(choice)
    choice_s3 = new2(choice)
    choice_s4 = choice_s2.lower()
    choice_s5 = choice_s4.capitalize()

    check = set()

    try:
        for root in roots:
            if choice in root:
                folder_path = str(root[:root.index(choice)]) + choice
                check.add(folder_path)
            if choice_c in root:
                folder_path_c = str(root[:root.index(choice_c)]) + choice_c
                check.add(folder_path_c)
            if choice_s in root:
                folder_path_s = str(root[:root.index(choice_s)]) + choice_s
                check.add(folder_path_s)
            if choice_s2 in root:
                folder_path_s2 = str(root[:root.index(choice_s2)]) + choice_s2
                check.add(folder_path_s2)
            if choice_s3 in root:
                folder_path_s3 = str(root[:root.index(choice_s3)]) + choice_s3
                check.add(folder_path_s3)
            if choice_s4 in root:
                folder_path_s4 = str(root[:root.index(choice_s4)]) + choice_s4
                check.add(folder_path_s4)
            if choice_s5 in root:
                folder_path_s5 = str(root[:root.index(choice_s5)]) + choice_s5
                check.add(folder_path_s5)

    except:
        pass

    if len(check)>0:
        try:
            for path in check:
                os.startfile(path)
            return True
        except:
            return False



#functioning for deleting a folder:                   delete folder
def delete_folder(folder_name, roots):
    folder_path = None
    folder_path_c = None
    folder_path_s = None
    folder_path_s2 = None
    folder_path_s3 = None
    folder_path_s4 = None
    folder_path_s5 = None

    choice=str(folder_name)
    choice_c = choice.upper()
    choice_s = choice.capitalize()
    choice_s2 = new1(choice)
    choice_s3 = new2(choice)
    choice_s4 = choice_s2.lower()
    choice_s5 = choice_s4.capitalize()

    check = set()

    try:
        for root in roots:
            if choice in root:
                folder_path = str(root[:root.index(choice)]) + choice
                check.add(folder_path)
            if choice_c in root:
                folder_path_c = str(root[:root.index(choice_c)]) + choice_c
                check.add(folder_path_c)
            if choice_s in root:
                folder_path_s = str(root[:root.index(choice_s)]) + choice_s
                check.add(folder_path_s)
            if choice_s2 in root:
                folder_path_s2 = str(root[:root.index(choice_s2)]) + choice_s2
                check.add(folder_path_s2)
            if choice_s3 in root:
                folder_path_s3 = str(root[:root.index(choice_s3)]) + choice_s3
                check.add(folder_path_s3)
            if choice_s4 in root:
                folder_path_s4 = str(root[:root.index(choice_s4)]) + choice_s4
                check.add(folder_path_s4)
            if choice_s5 in root:
                folder_path_s5 = str(root[:root.index(choice_s5)]) + choice_s5
                check.add(folder_path_s5)

    except:
        pass

    if len(check)>0:
        try:
            try:
                for path in check:
                    os.rmdir(path)
                return True
            except:
                for path in check:
                    shutil.rmtree(path)
                return True
        except:
            return False



#function for locking pc.......................lock computer
def lock_pc():
    try:
        ctypes.windll.user32.LockWorkStation()
        return True
    except:
        return False


#function for logging pc off:                log off computer
def logoff_pc():
    try:
        os.system("shutdown /l /t 5")
        return True
    except:
        return False


#function for restarting pc:                   restart computer
def restart_pc():
    try:
        os.system("shutdown /r /t 5")
        return True
    except:
        return False


#fuction for hibernating pc:                 hibernate computer
def hibernate_pc():
    try:
        os.system("shutdown /h")
        return True
    except:
        return False


#fuction for shutting pc down:               shutdown computer
def shutdown_pc():
    try:
        os.system("shutdown /s /t 5")
        return True
    except:
        return False











#----------other important functions---------

def get_message_subject(sentence):
    global subject
    global name
    global other_noun

    p_sentence = list(([sentence])[0].split())
    sentx = nt.TextFrame(text=str(sentence))
    s = sentx.remove_stopwords()
    check =  ([s.text])[0].split()
    n = ''
    for i in check:
        n += i + " "
    new_string = n[:-1]

    nlp = spacy.load("en_core_web_sm")
    ppnouns = []
    check2 = ['play', 'run', 'sing', 'eat', 'drink', 'kick', 'wife', 'new', 'husband', 'launch', 'breakfast', 'supper', 'dinner']
    for word in nlp(new_string):
        if word.pos_ == 'PROPN':
            if word.text not in check2:
                ppnouns.append(word.text)
    nameList = list(set(ppnouns))

    if len(nameList)>0:
        n2 = ''
        for i in nameList:
            n2 += i + " "
        nme = n2[:-1]
        if nme!='ralph':
            subject = nme
        else:
            subject = 'None'
    else:
        subject = 'None'

    # text = nltk.word_tokenize(sentence)
    # pos_tagged = nltk.pos_tag(text)
    # nouns = filter(lambda x:x[1]=='NN',pos_tagged)
    # nounList = []
    # for i in nouns:
    #     nounList.append(i[0])
    # if len(nounList)>0:
    #     check4 = ['morning', 'afternoon', 'evening', 'night']
    #     for i in nounList:
    #         if i!=name and i not in check4:
    #             other_noun = i
    #         else:
    #             other_noun = 'None'
    # else:
    #     other_noun = 'None'
    # print(f'name: {name}')
    # print(f'other_noun: {other_noun}')
    # if name!='None' and other_noun!='None':
    #     if name in p_sentence and other_noun in p_sentence:
    #         if p_sentence.index(name)<p_sentence.index(other_noun):
    #             subject = name
    #         elif p_sentence.index(other_noun)>p_sentence.index(name):
    #             subject = other_noun
    #     else:
    #         subject = name
    # elif name!='None' and other_noun=='None':
    #     subject = name
    # elif name=='None' and other_noun!='None':
    #     subject = other_noun
    # else:
    #     subject = 'None'


    return subject



#extract number from sentence
def extract_number(sentence, numwords={}):
    global number
    check = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    temp = []
    try:
        for num in sentence:
            if num in check:
                temp.append(num)
        if len(temp)>0:
            number = ' '.join(temp)
        else:
            units = [
                "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
                "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen",
              ]
            tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
            scales = ["hundred", "thousand", "million", "billion", "trillion"]
            extractedNumWords = []
            for s in ([sentence][0].split()):
                if s in units or s in tens or s in scales:
                    if s !="":
                        extractedNumWords.append(s)
            textnum = ' '.join(extractedNumWords)
            numwords["and"] = (1, 0)
            for idx, word in enumerate(units):    numwords[word] = (1, idx)
            for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
            for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)
            current = result = 0
            for word in textnum.split():
                if word not in numwords:
                  raise Exception("Illegal word: " + word)
                scale, increment = numwords[word]
                current = current * scale + increment
                if scale > 100:
                    result += current
                    current = 0
            number = result + current
    except:
        number = None

    return number



#extract time from sentence
def extract_time(message):
    global time

    tokenizedMessage = ([str(message)])[0].split()
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    nums2 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':']
    temp = []
    temp2 = []
    for i in message:
        if i in nums:
            temp.append(i)
    n=''
    for i in temp:
        n += i
    for i in message:
        if i in nums2:
            temp2.append(i)
    n2=''
    for i in temp2:
        n2 += i
    periods = ['p.m', 'a.m', 'pm', 'am', 'p.m.', 'a.m.']
    p = []
    for i in periods:
        if i in tokenizedMessage:
            p.append(i)
    if 'p.m' not in tokenizedMessage and 'a.m' not in tokenizedMessage and 'pm' not in tokenizedMessage and 'am' not in tokenizedMessage and 'p.m.' not in tokenizedMessage and 'a.m.' not in tokenizedMessage:
        if ':' in temp2:
            tokenizedMessage.insert(tokenizedMessage.index(n2)+1, 'p.m')
        else:
            tokenizedMessage.append('p.m')
        p.append('p.m')
    if len(p)>0:
        num = tokenizedMessage[tokenizedMessage.index(p[0])-1]
    else:
        num = n
    #print(tokenizedMessage)
    if len(temp)>0:
        check = []
        for i in tokenizedMessage:
            if ':' in i:
                check.append(i)

        if len(check)>0:
            t = []
            period = tokenizedMessage[tokenizedMessage.index(check[0])+1]
            t.append(str(check[0] + ' ' + period))
            if len(t)>0:
                time = t[0]
            else:
                time = 'None'
        else:
            if num in tokenizedMessage:
                if len(temp)==1:
                    time = temp[0] + ':' + '00' + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]

                elif len(temp)==2:
                    if n in tokenizedMessage:
                        time = temp[0] + temp[1] + ':' + '00' + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]
                    else:
                        if n[0]==n[1]:
                            time = temp[0] + ':' + '0' + temp[1] + ' ' + tokenizedMessage[tokenizedMessage.index(num)+2]
                        else:
                           time = temp[0] + ':' + '0' + temp[1] + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]

                elif len(temp)==3:
                    if (n[0]+n[1]) in tokenizedMessage and tokenizedMessage.index((n[0]+n[1]))<tokenizedMessage.index(n[2]):
                        time = temp[0] + temp[1] + ':' + '0' + temp[2] + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]
                    elif (n[1]+n[2]) in tokenizedMessage and tokenizedMessage.index(n[0])<tokenizedMessage.index((n[1]+n[2])):
                        time = temp[0] + ':' + temp[1] + temp[2] + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]
                    else:
                        time = 'None'

                elif len(temp)==4:
                    time = temp[0]  + temp[1] + ':' + temp[2] + temp[3] + ' ' + tokenizedMessage[tokenizedMessage.index(num)+1]

                else:
                    time = 'None'
    else:
        time = 'None'


    return time







