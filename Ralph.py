import os
import subprocess
import sys
import win32api
import ast
import threading
from sys import exit as sysExit
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLineEdit, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import speech_recognition as sr
import pyttsx3
#from textblob import TextBlob
#from googletrans import Translator
#from langdetect import detect
import webbrowser
import Action
import Chat
import Intend_Extractor
import DcAction













pictures = {}
audios = {}
videos = {}
apps = {}
filesz = {}
roots = set()

#loading all data which may be needed
def updater():
    global pictures, audios, videos, apps, filesz, roots
    pictures, audios, videos, apps, filesz, roots = Action.update_paths()

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





try:
    with open('_ralph_memory.txt', 'r', encoding="utf-8") as rm:
        data = rm.readlines()
        #print(data)
        #loading pictures
        d1 = (data[0][:data[0].index('\n')])
        rd1 = ast.literal_eval(d1)
        pictures = rd1
        #loading audios
        d2 = (data[1][:data[1].index('\n')])
        rd2 = ast.literal_eval(d2)
        audios = rd2
        #loading videos
        d3 = (data[2][:data[2].index('\n')])
        rd3 = ast.literal_eval(d3)
        videos = rd3
        #loading apps
        d4 = (data[3][:data[3].index('\n')])
        rd4 = ast.literal_eval(d4)
        apps = rd4
        #loading files
        d5 = (data[4][:data[4].index('\n')])
        rd5 = ast.literal_eval(d5)
        filesz = rd5
        #loading folders
        d6 = (data[5][:data[5].index('\n')])
        rd6 = ast.literal_eval(d6)
        roots = rd6

        rm.close()

        # print(pictures)
        # print(audios)
        # print(videos)
        # print(apps)
        # print(filesz)
        # print(roots)
except:
    filesLoader()





#setting up ralph's voice
ralph_s = pyttsx3.init()
voices = ralph_s.getProperty('voices')
ralph_s.setProperty('voice', voices[0].id)
ralph_s.setProperty('rate', 140)

#initializing ralph's ears
ralph_l = sr.Recognizer()

#ralph's animation and icon
ralph_face_animation = 'animations/ralph-anim1.gif'
ralph_icon = 'app-icons/ralph-app-icon.ico'

#some important initializations
conversation = {}
enable_DirectControl = threading.Event()
recording = []
sentMessage = []
questionAvailable = []
answerToAvailableQuestion = []
micToggledOn = []
micToggledOff = []


















def main():

    #setting up the GUI
    class CenterPanel(QWidget):
        def __init__(self, MainWindow):
            QWidget.__init__(self)
            MainWindow.setGeometry(25, 25, 800, 650)
            MainWindow.setFixedSize(800, 650)
            MainWindow.setWindowTitle('Ralph')
            MainWindow.setWindowIcon(QIcon(ralph_icon))
            #animation
            self.label = QtWidgets.QLabel(self)
            self.label.setMinimumSize(QtCore.QSize(800, 600))
            self.label.setMaximumSize(QtCore.QSize(200, 200))
            self.label.setObjectName("label")
            self.textbox = QLineEdit(self)
            self.textbox.move(12, 605)
            self.textbox.resize(280, 40)
            MainWindow.setCentralWidget(self)
            self.movie = QMovie(ralph_face_animation)
            self.label.setMovie(self.movie)
            self.movie.start()
            #send message button
            self.sendMessageButton = QPushButton('send', self)
            self.sendMessageButton.setIcon(QIcon('button-icons/send-message-button-icon.ico'))
            self.sendMessageButton.setIconSize(QtCore.QSize(22,22))
            self.sendMessageButton.move(300, 610)
            self.sendMessageButton.clicked.connect(self.sendMessageButton_clicked)
            #record button
            self.recordButton = QPushButton('record', self)
            self.recordButton.setIcon(QIcon('button-icons/record-button-icon.ico'))
            self.recordButton.setIconSize(QtCore.QSize(22,22))
            self.recordButton.move(630, 610)
            self.recordButton.clicked.connect(recordButton_clicked)
            #stop button
            self.stopButton = QPushButton('stop', self)
            self.stopButton.setIcon(QIcon('button-icons/stop-button-icon.ico'))
            self.stopButton.setIconSize(QtCore.QSize(22,22))
            self.stopButton.move(715, 610)
            self.stopButton.clicked.connect(stopButton_clicked)
            self.show()

        @pyqtSlot()
        def sendMessageButton_clicked(self):
            textboxValue = self.textbox.text()
            if textboxValue != '':
                try:
                    sentMsg = str(textboxValue)
                    if len(recording) == 0:
                        if len(questionAvailable)==0:
                            sentMessage.append(sentMsg)
                            ai()
                        else:
                            answerToAvailableQuestion.append(sentMsg)
                    else:
                        print('Wait for recording to stop')
                except:
                    print('Errorrrrr...')
            self.textbox.setText("")

    #handling the record and stop buttons
    def recordButton_clicked():
        try:
            if len(micToggledOff)>0:
                Action.toggle_microphone()
                micToggledOff.clear()

            if len(sentMessage) == 0:
                sentMessage.clear()
                recording.append(1)
                micToggledOn.append(1)
                ai()
            else:
                print('Wait for text mode to finish')
        except:
            print('Already on speech mode')

    def stopButton_clicked():
        try:
            if len(micToggledOn)>0:
                Action.toggle_microphone()
                recording.clear()
                micToggledOff.append(1)
                micToggledOn.clear()
                print('Stopped')
            else:
                print('Already stopped')
        except:
            print('Unable to stop now')


    class UI_MainWindow(QMainWindow):
        def __init__(self):
            super(UI_MainWindow, self).__init__()
            self.setCentralWidget(CenterPanel(self))
        def closeEvent(self, event):
             try:
                 if len(micToggledOff)>0:
                     Action.toggle_microphone()
                 sys.exit()
             except:
                 pass








    #assistant

    def get_speech():
        with sr.Microphone() as source:
            ralph_l.adjust_for_ambient_noise(source)
            ralph_l.pause_threshold = 1
            audio = ralph_l.listen(source)
            return audio

    def get_message(recorded_audio):
        try:
            userTextMessage = ralph_l.recognize_google(recorded_audio)
            msg = str(userTextMessage).lower()
            return msg
        except:
            ralph_s.say("Sorry, I couldn't understand you. Ensure that you are connected to the internet, then speak again.")
            ralph_s.runAndWait()
            recording.clear()
        # finally:
        #     userTextMessageLanguage = detect(userTextMessage)
        #     #print(userTextMessageLanguage)
        #     if userTextMessageLanguage != 'en':
        #         translatedText = Translator().translate(userTextMessage, dest='en')
        #         message = (translatedText.text).lower()
        #     else:
        #     message = userTextMessage.lower()




    def ralph():
        global gottenText
        if len(recording)>0 and len(micToggledOff)==0:
            try:
                aud = get_speech()
                gottenText = get_message(aud)
                ai_assistant(gottenText)
            except:
                print('Errorrr')

        elif len(sentMessage)>0 and len(micToggledOn)==0:
            ai_assistant(sentMessage[-1])

        elif len(sentMessage)==0 and len(recording)==0:
            none = None
            ai_assistant(none)

        else:
            print('Neither recording nor waiting for message....Error')






    def ai_assistant(msg):

        if msg != None:

            try:
                message = str(msg).lower()

                if message:

                    try:

                        commands = ["previous","next","pause","resume","repeat","update","fetch","presentation","use","research","navigate","turn","watch","track","convert","calculate","evaluate","compute","solve","simplify","maths","set","remind","change","convert","send","text","message","type","write","scan","enable","disable","construct","create","copy","draw","make","put","shift","press","click","left-click","right-click","scroll","activate","deactivate","play","open","launch","start","close","run","stop","terminate","search","mute","unmute","stream","end","find","check","text","message","delete","remove","increase","decrease","mute","reduce","add","higher","lower","brighter","connect","disconnect","empty","put","turn","switch","view","show","display","close","lock","log off","restart","sleep","hibernate","shutdown","go","move","time","date","network","ram","cpu","gpu","disk","drive","selfie","screenshot","network","specs","specifications","capacity","properties","ram","memory","battery","location","weather"]

                        check = []
                        processed_message = ([message])[0].split()
                        for i in commands:
                            if i in processed_message:
                                check.append(i)


                        message_intend = Intend_Extractor.Extract_Intend(message)[0]
                        dc_command = Intend_Extractor.Extract_Intend(message)[0]
                        print(f'your-message: {message}')
                        print(f'message-intend: {message_intend}')
                        #print(conversation)
                        #print(check)





                        #************************************* Command received ***************************************

                        if ((message_intend!='None') and (len(check)>0)):

                            #update paths
                            if message_intend == 'update paths':
                                ralph_s.say("Copy that. Commencing process.")
                                ralph_s.runAndWait()
                                try:
                                    updater()
                                    ralph_s.say("Paths have been updated successfully")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'successfully executed command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                except:
                                    ralph_s.say("Sorry. Something went wrong.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass



                            elif message_intend == 'time':
                                try:
                                    time = Action.get_time()
                                    ralph_s.say("The time is " + time)
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'successfully executed command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Unable to execute your command. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'date':
                                try:
                                    date = Action.get_date()
                                    ralph_s.say("The date is " + date)
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'successfully executed command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Unable to execute your command. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'set reminder':
                                global alarm_time
                                global reminder_message
                                global timeChoice
                                global reminderChoice
                                gottenTime = Action.extract_time(message)
                                if gottenTime == 'None':
                                    ralph_s.say('What is the time for the reminder?.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        timeChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                timeChoice = answerToAvailableQuestion[-1]
                                                break
                                    if timeChoice:
                                        alarm_time = timeChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No response received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    alarm_time = gottenTime
                                    answerToAvailableQuestion.clear()
                                print(alarm_time)

                                ralph_s.say('What should I remind you about?.')
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    reminderChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            reminderChoice = answerToAvailableQuestion[-1]
                                            break
                                if reminderChoice:
                                    reminder_message = reminderChoice
                                else:
                                    ralph_s.say("No response received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass

                                if reminder_message:
                                    try:
                                        func = lambda: Action.set_Reminder(reminder_message, alarm_time)
                                        thread = threading.Thread(target=func)
                                        thread.setDaemon(True)
                                        thread.start()
                                        ralph_s.say('Your reminder has been set for ' + alarm_time)
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass

                                    except:
                                        ralph_s.say("Sorry, something went wrong. Couldn't set reminder. Please try ensure you are connected to the internet, then again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    ralph_s.say("No response received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'location':
                                try:
                                    location = Action.get_CurrentLocation()
                                    if location:
                                        ralph_s.say(str(location))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, I couldn't get your current location. Please connect to the internet, then try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I couldn't get your current location. Please connect to the internet, then try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'weather':
                                global city
                                global cityChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target == 'None':
                                    ralph_s.say('Which city do you want weather details of?.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        cityChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                cityChoice = answerToAvailableQuestion[-1]
                                                break
                                    if cityChoice:
                                        city = cityChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No response received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    city = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(city)

                                try:
                                    weather = Action.get_Weather(city)
                                    if weather:
                                        ralph_s.say(str(weather))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, I couldn't get weather details for " + city + ". Probably, the city name is not a valid city or it could be that you are not connected to the internet. Try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I couldn't execute your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            # elif message_intend == 'track tel-number':
                            #     global numberr
                            #     global numberrChoice
                            #     num = Action.extract_number(message)
                            #     if num=='None':
                            #         ralph_s.say("Please tell me the valid phone number you want me to locate.")
                            #         ralph_s.runAndWait()
                            #         questionAvailable.append(1)
                            #         if len(recording)>0:
                            #             audio = get_speech()
                            #             numberrChoice = get_message(audio)
                            #         if len(sentMessage)>0:
                            #             while len(answerToAvailableQuestion)==0:
                            #                 print('')
                            #                 if len(answerToAvailableQuestion)>0:
                            #                     numberrChoice = answerToAvailableQuestion[-1]
                            #                     break
                            #         if numberrChoice:
                            #             numberr = numberrChoice
                            #             answerToAvailableQuestion.clear()
                            #         else:
                            #             ralph_s.say("No response received. Operation aborted")
                            #             ralph_s.runAndWait()
                            #             conversation.update({message: 'operation aborted'})
                            #             if len(recording)>0:
                            #                 questionAvailable.clear()
                            #                 answerToAvailableQuestion.clear()
                            #                 ralph()
                            #             else:
                            #                 pass
                            #     else:
                            #         numberr = num
                            #         answerToAvailableQuestion.clear()
                            #     print(numberr)
                            #
                            #     try:
                            #         numberLocation = Action.get_PhoneNumberLocation(numberr)
                            #         if numberLocation:
                            #             ralph_s.say(numberr + 'has been located.')
                            #             ralph_s.runAndWait()
                            #             conversation.update({message: 'successfully executed command'})
                            #             if len(recording)>0:
                            #                 questionAvailable.clear()
                            #                 answerToAvailableQuestion.clear()
                            #                 ralph()
                            #             else:
                            #                 pass
                            #         else:
                            #             ralph_s.say("Sorry, something went wrong. Couldn't locate " + numberr + ". Probably, you are not connected to the internet or the number is not a valid phone number. Try again")
                            #             ralph_s.runAndWait()
                            #             conversation.update({message: 'failed to execute command'})
                            #             if len(recording)>0:
                            #                 questionAvailable.clear()
                            #                 answerToAvailableQuestion.clear()
                            #                 ralph()
                            #             else:
                            #                 pass
                            #     except:
                            #         ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet then try again")
                            #         ralph_s.runAndWait()
                            #         conversation.update({message: 'failed to execute command'})
                            #         if len(recording)>0:
                            #             questionAvailable.clear()
                            #             answerToAvailableQuestion.clear()
                            #             ralph()
                            #         else:
                            #             pass




                            elif message_intend == 'whatsapp':
                                global number
                                global numberChoice
                                global messagge
                                global messaggeChoice
                                num = Action.extract_number(message)
                                if num=='None':
                                    ralph_s.say("Please tell me the contact number you want to message.")
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        numberChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                numberChoice = answerToAvailableQuestion[-1]
                                                break
                                    if numberChoice:
                                        number = numberChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No response received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    number = num
                                    answerToAvailableQuestion.clear()
                                print(number)

                                ralph_s.say("What ever you say now will be sent to " + number + ", immediately you finish speaking. Please speak now...")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    messaggeChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            messaggeChoice = answerToAvailableQuestion[-1]
                                            break
                                if messaggeChoice:
                                    messagge = messaggeChoice
                                else:
                                    ralph_s.say("No response received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(messagge)

                                if number and messagge:
                                    try:
                                        if Action.message_whatsapp_contact(number, messagge):
                                            ralph_s.say("Your message has been sent to " + number)
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say("Error. Something went wrong. Please ensure the contact you are trying to message is on whatsapp. Also ensure that you are connected to the internet. Try again.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    ralph_s.say("No information concerning request received. Operation aborted.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'google search':
                                global google_query
                                ralph_s.say("What do you want to search for on google.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    google_query = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            google_query = answerToAvailableQuestion[-1]
                                            break
                                print(google_query)

                                if google_query:
                                    try:
                                        if Action.google_search(google_query):
                                            ralph_s.say("Your query has been sent.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say("Error. Something went wrong. Connect to the internet, then try again.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    ralph_s.say("No information concerning request received. Operation aborted.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'maths' or message_intend == 'convert':
                                try:
                                    if Action.google_search(message):
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'youtube':
                                global youtube_query
                                ralph_s.say("What do you want to search for on youtube.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    youtube_query = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            youtube_query = answerToAvailableQuestion[-1]
                                            break
                                print(youtube_query)

                                if youtube_query:
                                    try:
                                        if Action.search_on_youtube(youtube_query):
                                            ralph_s.say("Your query has been sent to youtube.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say("Error. Something went wrong. Please connect to the internet, then try again.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Error. Something went wrong. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass

                                else:
                                    ralph_s.say("No information concerning request received. Operation aborted.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'show picture':
                                global photo
                                global photoChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                unknownName = Action.get_message_subject(message)

                                if unknownName != 'None':
                                    if unknownName in processed_message:
                                        pm = processed_message[processed_message.index(unknownName):]
                                        mm = ''
                                        for i in pm:
                                            mm += i + ' '
                                        picQuery = str(mm[:-1])
                                        webbrowser.open('https://www.google.com/search?q=picture of' + picQuery)
                                        conversation.update({message: 'google searched'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        pass
                                else:
                                    if 'any' not in processed_message:
                                        if message_intend_target=='None':
                                            ralph_s.say('What is the name of the picture or photo you want to see sir?')
                                            ralph_s.runAndWait()
                                            questionAvailable.append(1)
                                            if len(recording)>0:
                                                audio = get_speech()
                                                photoChoice = get_message(audio)
                                            if len(sentMessage)>0:
                                                while len(answerToAvailableQuestion)==0:
                                                    print('')
                                                    if len(answerToAvailableQuestion)>0:
                                                        photoChoice = answerToAvailableQuestion[-1]
                                                        break
                                            if photoChoice:
                                                photo = photoChoice
                                            else:
                                                ralph_s.say("No command received. Operation aborted")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'operation aborted'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                        else:
                                            photo = message_intend_target
                                        print(photo)

                                        ralph_s.say("Searching for " + photo + "...")
                                        ralph_s.runAndWait()
                                        try:
                                            if Action.view_picture(photo, pictures):
                                                ralph_s.say("Photo found and opened.")
                                                conversation.update({message: 'successfully executed command'})
                                                ralph_s.runAndWait()
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            else:
                                                ralph_s.say(photo + " not found sir.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'failed to execute command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                        except:
                                            ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    else:
                                         if Action.view_picture('any photo', pictures):
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                         else:
                                            ralph_s.say("Sorry, something went wrong. Unable to execute command.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass




                            elif message_intend == 'close picture':
                                try:
                                    task = Action.close_photo()
                                    if task:
                                        ralph_s.say('Photo has been closed sir.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say('Error. No photo found to close')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'play':
                                global target
                                global targetChoice
                                global ptarget
                                if 'play' in processed_message:
                                    temp = processed_message[(processed_message.index('play')+1):]
                                    m=''
                                    for i in temp:
                                        m += i + ' '
                                    tt = m[:-1]
                                    ptarget = tt
                                else:
                                    ptarget = 'None'
                                if ptarget=='None':
                                    ralph_s.say('Please say the title of what you want me to play.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        targetChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                targetChoice = answerToAvailableQuestion[-1]
                                                break
                                    if targetChoice:
                                        target = targetChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    target = ptarget
                                print(target)

                                ralph_s.say("Searching for " + target + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.play_audio(target, audios):
                                        ralph_s.say("Audio found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    elif Action.play_video(target, videos):
                                        ralph_s.say("Video found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(target + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'play audio':
                                if 'any' not in processed_message:
                                    global music
                                    global audioChoice
                                    message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                    if message_intend_target=='None':
                                        ralph_s.say('Please say the title of the audio you want me to play.')
                                        ralph_s.runAndWait()
                                        questionAvailable.append(1)
                                        if len(recording)>0:
                                            audio = get_speech()
                                            audioChoice = get_message(audio)
                                        if len(sentMessage)>0:
                                            while len(answerToAvailableQuestion)==0:
                                                print('')
                                                if len(answerToAvailableQuestion)>0:
                                                    audioChoice = answerToAvailableQuestion[-1]
                                                    break
                                        if audioChoice:
                                            music = audioChoice
                                        else:
                                            ralph_s.say("No command received. Operation aborted")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'operation aborted'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    else:
                                        music = message_intend_target
                                    print(music)

                                    ralph_s.say("Searching for " + music + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.play_audio(music, audios):
                                            ralph_s.say("Audio found and opened.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(music + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                     if Action.play_audio('any audio', audios):
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                     else:
                                        ralph_s.say("Sorry, something went wrong. Unable to execute command.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass




                            elif message_intend == 'stop audio':
                                try:
                                    task = Action.close_audio()
                                    if task:
                                        ralph_s.say('Audio has been closed.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say('Error. No audio found to close')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'play video':
                                if 'any' not in processed_message:
                                    global video
                                    global videoChoice
                                    message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                    if message_intend_target=='None':
                                        ralph_s.say('Please say the title of the video you want me to play.')
                                        ralph_s.runAndWait()
                                        questionAvailable.append(1)
                                        if len(recording)>0:
                                            audio = get_speech()
                                            videoChoice = get_message(audio)
                                        if len(sentMessage)>0:
                                            while len(answerToAvailableQuestion)==0:
                                                print('')
                                                if len(answerToAvailableQuestion)>0:
                                                    videoChoice = answerToAvailableQuestion[-1]
                                                    break
                                        if videoChoice:
                                            video = videoChoice
                                        else:
                                            ralph_s.say("No command received. Operation aborted")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'operation aborted'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    else:
                                        video = message_intend_target
                                    print(video)

                                    ralph_s.say("Searching for " + video + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.play_video(video, videos):
                                            ralph_s.say("Video found and opened.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(video + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                     if Action.play_video('any video', videos):
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                     else:
                                        ralph_s.say("Sorry, something went wrong. Unable to execute command.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass




                            elif message_intend == 'stop video':
                                try:
                                    task = Action.close_video()
                                    if task:
                                        ralph_s.say('Video has been closed.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say('Error. No video found to close')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete picture':
                                global photoo
                                global photooChoice
                                global pdecision
                                global pdecisionChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the picture you want me to delete.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        photooChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                photooChoice = answerToAvailableQuestion[-1]
                                                break
                                    if photooChoice:
                                        photoo = photooChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    photoo = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(photoo)

                                ralph_s.say(photoo + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    pdecisionChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            pdecisionChoice = answerToAvailableQuestion[-1]
                                            break
                                if pdecisionChoice:
                                    pdecision = pdecisionChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(pdecision)

                                if pdecision == "yes":
                                    ralph_s.say("Searching for " + photoo + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.delete_picture(photoo, pictures):
                                            ralph_s.say(photoo + " has been deleted.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(photoo + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                elif pdecision == "no":
                                    ralph_s.say("Your delete request has been terminated.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'request terminated'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                else:
                                    ralph_s.say("Invalid response. Operation has been aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete audio':
                                global musicc
                                global musiccChoice
                                global mdecision
                                global mdecisionChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the audio you want me to delete.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        musiccChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                musiccChoice = answerToAvailableQuestion[-1]
                                                break
                                    if musiccChoice:
                                        musicc = musiccChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    musicc = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(musicc)

                                ralph_s.say(musicc + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    mdecisionChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            mdecisionChoice = answerToAvailableQuestion[-1]
                                            break
                                if mdecisionChoice:
                                    mdecision = mdecisionChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(mdecision)

                                if mdecision == "yes":
                                    ralph_s.say("Searching for " + musicc + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.delete_audio(musicc, audios):
                                            ralph_s.say(musicc + " has been deleted.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(musicc + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                elif mdecision == "no":
                                    ralph_s.say("Your delete request has been terminated.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'request terminated'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                else:
                                    ralph_s.say("Invalid response. Operation has been aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete video':
                                global videoo
                                global videooChoice
                                global vdecision
                                global vdecisionChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the video you want me to delete.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        videooChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                videooChoice = answerToAvailableQuestion[-1]
                                                break
                                    if videooChoice:
                                        videoo = videooChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    videoo = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(videoo)

                                ralph_s.say(videoo + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    vdecisionChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            mdecisionChoice = answerToAvailableQuestion[-1]
                                            break
                                if vdecisionChoice:
                                    vdecision = vdecisionChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(vdecision)

                                if vdecision == "yes":
                                    ralph_s.say("Searching for " + videoo + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.delete_video(videoo, videos):
                                            ralph_s.say(videoo + " has been deleted.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(videoo + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                elif vdecision == "no":
                                    ralph_s.say("Your delete request has been terminated.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'request terminated'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                else:
                                    ralph_s.say("Invalid response. Operation has been aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'close' or message_intend == 'close website':
                                global targettt
                                global targetttChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of what you want me to close.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        targetttChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                targetttChoice = answerToAvailableQuestion[-1]
                                                break
                                    if targetttChoice:
                                        targettt = targetttChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    targettt = message_intend_target
                                print(targettt)

                                try:
                                    if Action.close_program(targettt):
                                        ralph_s.say(targettt + 'has been closed.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        if DcAction.Close():
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Sorry, something went wrong. Try again.')
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'open':
                                global targett
                                global targettChoice
                                global utarget
                                if 'open' in processed_message:
                                    temp = processed_message[(processed_message.index('open')+1):]
                                    m=''
                                    for i in temp:
                                        m += i + ' '
                                    tt = m[:-1]
                                    utarget = tt
                                else:
                                    utarget = 'None'

                                if utarget=='None':
                                    ralph_s.say('Please say the name of what you want me to open.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        targettChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                targettChoice = answerToAvailableQuestion[-1]
                                                break
                                    if targettChoice:
                                        targett = targettChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    targett = utarget
                                print(targett)
                                popularSites = ['google', 'instagram', 'facebook', 'twitter', 'tiktok', 'telegram', 'youtube', 'snapchat', 'whatsapp', 'wikipedia', 'bing', 'github']
                                sitesCheck = []
                                fileCheck = []
                                fileExtensions = ['txt', 'csv', 'xlsx', 'docx', 'pdf', 'rar', 'iso', 'zip']
                                exts = []
                                for s in popularSites:
                                    if s in processed_message:
                                        sitesCheck.append(s)
                                for f in processed_message:
                                    if '.' in f:
                                        try:
                                            ext = f[f.index('.')+1]
                                            fileCheck.append(f)
                                        except IndexError:
                                            for e in fileExtensions:
                                                if e in processed_message:
                                                    exts.append(e)
                                            if len(exts)>0:
                                                t = f + exts[0]
                                                fileCheck.append(t)
                                            else:
                                                pass

                                try:
                                    if len(sitesCheck)>0:
                                        if Action.open_website(targett):
                                            ralph_s.say(targett + " found and opened.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(targett + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    elif len(fileCheck)>0:
                                        f_targett = fileCheck[0]
                                        if Action.open_file(f_targett, filesz):
                                            ralph_s.say(f_targett + " has been found and opened.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(f_targett + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    else:
                                        if Action.run_application(targett, apps):
                                            ralph_s.say("Program found and opened.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            if Action.open_folder(targett, roots):
                                                ralph_s.say("Folder found and opened.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            else:
                                                ralph_s.say(targett + " not found.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'failed to execute command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'run app':
                                global app
                                global appChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the program or application you want me to open.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        appChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                appChoice = answerToAvailableQuestion[-1]
                                                break
                                    if appChoice:
                                        app = appChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    app = message_intend_target
                                print(app)

                                ralph_s.say("Searching for " + app + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.run_application(app, apps):
                                        ralph_s.say("Program found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(app + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'stop app':
                                global appp
                                global apppChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the program you want me to stop.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        apppChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                apppChoice = answerToAvailableQuestion[-1]
                                                break
                                    if apppChoice:
                                        appp = apppChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    appp = message_intend_target
                                print(appp)

                                try:
                                    task = Action.close_program(appp)
                                    if task:
                                        ralph_s.say(appp + 'has been closed.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(appp + 'is not running so cannot be closed')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'open file':
                                global file
                                global fileChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the file you want me to search for. Include its extension')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        fileChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                fileChoice = answerToAvailableQuestion[-1]
                                                break
                                    if fileChoice:
                                        file = fileChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    file = message_intend_target
                                print(file)

                                ralph_s.say("Searching for " + file + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.open_file(file, filesz):
                                        ralph_s.say(file + " has been found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(file + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete file':
                                global filee
                                global fileeChoice
                                global ddecision
                                global ddecisionChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the file you want me to delete. Include its extension')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        fileeChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                fileeChoice = answerToAvailableQuestion[-1]
                                                break
                                    if fileeChoice:
                                        filee = fileeChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    filee = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(filee)

                                ralph_s.say(filee + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    ddecisionChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            ddecisionChoice = answerToAvailableQuestion[-1]
                                            break
                                if ddecisionChoice:
                                    ddecision = ddecisionChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(ddecision)

                                if ddecision == "yes":
                                    ralph_s.say("Searching for " + filee + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.delete_file(filee, filesz):
                                            ralph_s.say(filee + " has been deleted.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(filee + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                elif ddecision == "no":
                                    ralph_s.say("Your delete request has been terminated.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'request terminated'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                else:
                                    ralph_s.say("Invalid response. Operation has been aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'open folder':
                                global folder
                                global folderChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the folder you want me to open.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        folderChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                folderChoice = answerToAvailableQuestion[-1]
                                                break
                                    if folderChoice:
                                        folder = folderChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    folder = message_intend_target
                                print(folder)

                                ralph_s.say("Searching for " + folder + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.open_folder(folder, roots):
                                        ralph_s.say("Folder found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(folder + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete folder':
                                global folderr
                                global folderrChoice
                                global fdecision
                                global fdecisionChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the folder you want me to delete.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        folderrChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                folderrChoice = answerToAvailableQuestion[-1]
                                                break
                                    if folderrChoice:
                                        folderr = folderrChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    folderr = message_intend_target
                                    answerToAvailableQuestion.clear()
                                print(folderr)

                                ralph_s.say(folderr + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this folder?. Yes or No?.")
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    fdecisionChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            fdecisionChoice = answerToAvailableQuestion[-1]
                                            break
                                if fdecisionChoice:
                                    fdecision = fdecisionChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(fdecision)

                                if fdecision == "yes":
                                    ralph_s.say("Searching for " + folderr + "...")
                                    ralph_s.runAndWait()
                                    try:
                                        if Action.delete_folder(folderr, roots):
                                            ralph_s.say(folderr + " has been deleted.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say(folderr + " not found.")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                elif fdecision == "no":
                                    ralph_s.say("Your delete request has been terminated.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'request terminated'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                else:
                                    ralph_s.say("Invalid response. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'delete':
                                global targetttt
                                global targettttChoice
                                global decision
                                global decisionChoice
                                global uutarget
                                if 'delete' in processed_message:
                                    temp = processed_message[(processed_message.index('delete')+1):]
                                    m=''
                                    for i in temp:
                                        m += i + ' '
                                    tt = m[:-1]
                                    uutarget = tt
                                else:
                                    uutarget = 'None'

                                if uutarget=='None':
                                    ralph_s.say('Please say the name what you want me to delete.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        targettttChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                targettttChoice = answerToAvailableQuestion[-1]
                                                break
                                    if targettttChoice:
                                        targetttt = targettttChoice
                                        answerToAvailableQuestion.clear()
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    targetttt = uutarget
                                    answerToAvailableQuestion.clear()
                                print(targetttt)

                                fileCheck = []
                                fileExtensions = ['txt', 'csv', 'xlsx', 'docx', 'pdf', 'rar', 'iso', 'zip']
                                exts = []
                                for f in processed_message:
                                    if '.' in f:
                                        try:
                                            ext = f[f.index('.')+1]
                                            fileCheck.append(f)
                                        except IndexError:
                                            for e in fileExtensions:
                                                if e in processed_message:
                                                    exts.append(e)
                                            if len(exts)>0:
                                                t = f + exts[0]
                                                fileCheck.append(t)
                                            else:
                                                pass

                                if len(fileCheck)>0:
                                    f_target = fileCheck[0]
                                    ralph_s.say(f_target + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        decisionChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                decisionChoice = answerToAvailableQuestion[-1]
                                                break
                                    if decisionChoice:
                                        decision = decisionChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    print(decision)

                                    if decision == "yes":
                                        ralph_s.say("Searching for " + f_target + "...")
                                        ralph_s.runAndWait()
                                        try:
                                            if Action.delete_file(f_target, filesz):
                                                ralph_s.say(f_target + " has been deleted.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            else:
                                                ralph_s.say(f_target + " not found.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'failed to execute command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                        except:
                                            ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    elif decision == "no":
                                        ralph_s.say("Your delete request has been terminated.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'request terminated'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Invalid response. Operation has been aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    ralph_s.say(targetttt + " will be completely removed from your computer and cannot be recovered. Are you sure you want to delete this file?. Yes or No?.")
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        decisionChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                decisionChoice = answerToAvailableQuestion[-1]
                                                break
                                    if decisionChoice:
                                        decision = decisionChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    print(decision)

                                    if decision == "yes":
                                        ralph_s.say("Searching for " + targetttt + "...")
                                        ralph_s.runAndWait()
                                        try:
                                            if Action.delete_folder(targetttt, roots):
                                                ralph_s.say(targetttt + " has been deleted.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            elif Action.delete_audio(targetttt, audios):
                                                ralph_s.say(targetttt + " has been deleted.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            elif Action.delete_video(targetttt, videos):
                                                ralph_s.say(targetttt + " has been deleted.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            elif Action.delete_picture(targetttt, pictures):
                                                ralph_s.say(targetttt + " has been deleted.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'successfully executed command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            else:
                                                ralph_s.say(targetttt + " not found.")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'failed to execute command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                        except:
                                            ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    elif decision == "no":
                                        ralph_s.say("Your delete request has been terminated.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'request terminated'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Invalid response. Operation has been aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass




                            elif message_intend == 'open website':
                                global site
                                global siteChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the website you want me to open.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        siteChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                siteChoice = answerToAvailableQuestion[-1]
                                                break
                                    if siteChoice:
                                        site = siteChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    site = message_intend_target
                                print(site)

                                ralph_s.say("Searching for " + site + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.open_website(site):
                                        ralph_s.say(site + " found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(site + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'open browser':
                                global browserr
                                global browserrChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the browser you want me to open.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        browserrChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                browserrChoice = answerToAvailableQuestion[-1]
                                                break
                                    if browserrChoice:
                                        browserr = browserrChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    browserr = message_intend_target
                                print(browserr)

                                ralph_s.say("Searching for " + browserr + "...")
                                ralph_s.runAndWait()
                                try:
                                    if Action.run_application(browserr, apps):
                                        ralph_s.say("Program found and opened.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(browserr + " not found.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'close browser':
                                global browserrr
                                global browserrrChoice
                                message_intend_target = Intend_Extractor.Extract_Intend(message)[1]
                                if message_intend_target=='None':
                                    ralph_s.say('Please say the name of the browser you want me to close.')
                                    ralph_s.runAndWait()
                                    questionAvailable.append(1)
                                    if len(recording)>0:
                                        audio = get_speech()
                                        browserrrChoice = get_message(audio)
                                    if len(sentMessage)>0:
                                        while len(answerToAvailableQuestion)==0:
                                            print('')
                                            if len(answerToAvailableQuestion)>0:
                                                browserrrChoice = answerToAvailableQuestion[-1]
                                                break
                                    if browserrrChoice:
                                        browserrr = browserrrChoice
                                    else:
                                        ralph_s.say("No command received. Operation aborted")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'operation aborted'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    browserrr = message_intend_target
                                print(browserrr)

                                try:
                                    task = Action.close_program(browserrr)
                                    if task:
                                        ralph_s.say(browserrr + 'has been closed.')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say(browserrr + 'is not running so it cannot be closed')
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'decrease brightness':
                                try:
                                    if Action.decrease_screen_brightness():
                                        ralph_s.say("Done. Your pc screen brightness has been decreased.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'increase brightness':
                                try:
                                    if Action.increase_screen_brightness():
                                        ralph_s.say("Done. Your pc screen brightness has been increased.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'decrease volume':
                                try:
                                    if Action.decrease_volume():
                                        ralph_s.say("Done. Your pc master volume has been decreased.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Somethin went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass


                            elif message_intend == 'increase volume':
                                try:
                                    if Action.increase_volume():
                                        ralph_s.say("Done. Your pc master volume has been increased.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'mute pc':
                                try:
                                    if Action.Mute_pc():
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'unmute pc':
                                try:
                                    if Action.Unmute_pc():
                                        ralph_s.say("Your pc has been unmuted.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'connect wifi':
                                global wifiName
                                global wifinameChoice
                                ralph_s.say('Please say the name of the device name you want to connect to through wi-fi.')
                                ralph_s.runAndWait()
                                questionAvailable.append(1)
                                if len(recording)>0:
                                    audio = get_speech()
                                    wifinameChoice = get_message(audio)
                                if len(sentMessage)>0:
                                    while len(answerToAvailableQuestion)==0:
                                        print('')
                                        if len(answerToAvailableQuestion)>0:
                                            wifinameChoice = answerToAvailableQuestion[-1]
                                            break
                                if wifinameChoice:
                                    wifiName = wifinameChoice
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                print(wifiName)

                                if wifiName:
                                    try:
                                        if Action.connect_to_once_connected_wifi(wifiName):
                                            ralph_s.say("Done. Your pc is now connected to " + wifiName)
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'successfully executed command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say("Unable to connect to " + wifiName + ". Please ensure that the device you are trying to connect to is available. This device should be one which you have connected to before")
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'failed to execute command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                    except:
                                        ralph_s.say("Sorry, I didn't get your command. Please ensure that you are connected to the internet then try again")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    ralph_s.say("No command received. Operation aborted")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'operation aborted'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'disconnect wifi':
                                try:
                                    if Action.disconnect_from_connected_wifi():
                                        ralph_s.say("Done. Your pc has been disconnected from the device it was connected to.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Your pc is probably not connected to any wifi currently.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Your pc is probably not connected to any wifi currently.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass



                            elif message_intend == 'pc battery details':
                                try:
                                    batteryInfo = Action.get_Battery_details()
                                    if batteryInfo:
                                        ralph_s.say(str(batteryInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, something went wrong. Couldn't get battery details. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get battery details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'pc harddisk details':
                                try:
                                    harddiskzInfo = Action.get_Harddisk_details()
                                    if harddiskzInfo:
                                        ralph_s.say(str(harddiskzInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, something went wrong. Couldn't get your hard disk details. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get your hard disk details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass



                            elif message_intend == 'pc cpu details':
                                try:
                                    cpuInfo = Action.get_CPU_details()
                                    if cpuInfo:
                                        ralph_s.say(str(cpuInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, something went wrong. Couldn't get your computer cpu details. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get your computer cpu details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'pc gpu details':
                                try:
                                    gpuInfo = Action.get_GPU_details()
                                    if gpuInfo:
                                        ralph_s.say(str(gpuInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("No details found. Your computer probably has no GPU.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("No details found. Your computer probably has no GPU.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'pc memory details':
                                try:
                                    ramInfo = Action.get_Memory_details()
                                    if ramInfo:
                                        ralph_s.say(str(ramInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, something went wrong. Couldn't get your computer RAM details. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get your computer RAM details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass



                            elif message_intend == 'pc network details':
                                try:
                                    networkInfo = Action.get_Network_details()
                                    if networkInfo:
                                        ralph_s.say(str(networkInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, something went wrong. Couldn't get your pc network details. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get your pc network details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'pc specs':
                                pcInfo = {}
                                try:
                                    memoryInfo = Action.get_Memory_details()
                                    networkInfo = Action.get_Network_details()
                                    cpuInfo = Action.get_CPU_details()
                                    gpuInfo = Action.get_GPU_details()
                                    hdInfo = Action.get_Harddisk_details()
                                    if 1 == 1:
                                        pcInfo.update({'memory': memoryInfo, 'cpu': cpuInfo, 'gpu': gpuInfo, 'hard disks': hdInfo, 'network': networkInfo})
                                        ralph_s.say(str(pcInfo))
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass

                                except:
                                    ralph_s.say("Sorry, something went wrong. Couldn't get all your pc details. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass



                            elif message_intend == 'take screenshot':
                                try:
                                    Action.take_Screenshot()
                                    ralph_s.say("Done. Screenshot has been saved in screenshots, in the pictures folder in your computer.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'successfully executed command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                except:
                                    ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'take selfie':
                                try:
                                    if Action.take_Selfie():
                                        ralph_s.say("Selfie will be taken shortly. Your selfies are stored in the pictures folder on your desktop.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Sorry, unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'empty recycle bin':
                                try:
                                    if Action.empty_recycle_bin():
                                        ralph_s.say("Done. Your recycle bin is now empty.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Your recycle bin is already empty.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Your recycle bin is already empty.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'lock pc':
                                try:
                                    if Action.lock_pc():
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'log off pc':
                                try:
                                    if Action.logoff_pc():
                                        ralph_s.say("Done. Your pc will logoff in few seconds.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'hibernate pc':
                                try:
                                    if Action.hibernate_pc():
                                        ralph_s.say("Done.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'restart pc':
                                try:
                                    if Action.restart_pc():
                                        ralph_s.say("Done. Your pc will restart in few seconds.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'turn-on pc':
                                try:
                                    ralph_s.say("Your computer is already on.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'successfully executed command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass




                            elif message_intend == 'shutdown pc':
                                try:
                                    if Action.shutdown_pc():
                                        ralph_s.say("Done. Your pc will shutdown in few seconds.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'successfully executed command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                        ralph_s.runAndWait()
                                        conversation.update({message: 'failed to execute command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                except:
                                    ralph_s.say("Unable to execute command. Something went wrong. Please try again.")
                                    ralph_s.runAndWait()
                                    conversation.update({message: 'failed to execute command'})
                                    if len(recording)>0:
                                        questionAvailable.clear()
                                        answerToAvailableQuestion.clear()
                                        ralph()
                                    else:
                                        pass


                            else:
                                if dc_command=='press key':
                                    key = Intend_Extractor.Extract_Intend(message, intendExtractorReqs)[1]
                                    if DcAction.press_key(key):
                                        conversation.update({message: 'dc command successfully executed'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                    else:
                                        ralph_s.say('Error. Please try again.')
                                        conversation.update({message: 'failed to execute dc command'})
                                        if len(recording)>0:
                                            questionAvailable.clear()
                                            answerToAvailableQuestion.clear()
                                            ralph()
                                        else:
                                            pass
                                else:
                                    if dc_command == 'up':
                                        if DcAction.up():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'down':
                                        if DcAction.down():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'right':
                                        if DcAction.right():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'left':
                                        if DcAction.left():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f1':
                                        if DcAction.func1():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f2':
                                        if DcAction.func2():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f3':
                                        if DcAction.func3():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f4':
                                        if DcAction.func4():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f5':
                                        if DcAction.func5():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f6':
                                        if DcAction.func6():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f7':
                                        if DcAction.func7():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f8':
                                        if DcAction.func8():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f9':
                                        if DcAction.func9():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f10':
                                        if DcAction.func10():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f11':
                                        if DcAction.func11():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'f12':
                                        if DcAction.func12():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'prtsc':
                                        if DcAction.print_screen():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'start menu':
                                        if DcAction.start_menu():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'caps lock':
                                        if DcAction.caps_lock():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'backspace':
                                        if DcAction.backspace():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'space':
                                        if DcAction.space():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'escape':
                                        if DcAction.escape():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'tab' or dc_command == 'indent':
                                        if DcAction.tab():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'alt':
                                        if DcAction.alt():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'ctrl':
                                        if DcAction.ctrl():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'home':
                                        if DcAction.home():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'end':
                                        if DcAction.end():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'insert':
                                        if DcAction.insert():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'scroll lock':
                                        if DcAction.scroll_lock():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'num lock':
                                        if DcAction.num_lock():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'pause':
                                        if DcAction.pause():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'enter':
                                        if DcAction.enter():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'delete':
                                        if DcAction.delete():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'shift':
                                        if DcAction.shift():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'page up' or dc_command == 'scroll up':
                                        if DcAction.page_up():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'page down' or dc_command == 'scroll down':
                                        if DcAction.page_down():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'left click' or dc_command == 'select':
                                        if DcAction.left_click():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'right click':
                                        if DcAction.right_click():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'click':
                                        if DcAction.click():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'properties':
                                        if DcAction.open_Properties():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'change window':
                                        if DcAction.change_Window():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'change taskbar app':
                                        if DcAction.change_Taskbar_App():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'opened windows':
                                        if DcAction.show_Opened_windows():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'close.1':
                                        if DcAction.Close():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'shortcut menu':
                                        if DcAction.Shortcut_menu():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'select all':
                                        if DcAction.Select_all():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'refresh':
                                        if DcAction.Refresh():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'quick link menu':
                                        if DcAction.Quick_link_menu():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'action center':
                                        if DcAction.Action_center():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'desktop':
                                        if DcAction.Desktop():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'restore minimized windows':
                                        if DcAction.Restore_minimized_windows():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'maximize':
                                        if DcAction.Maximize_window():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'pc':
                                        if DcAction.thisPC():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'command prompt':
                                        if DcAction.cmd():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'powershell':
                                        if DcAction.powershell():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'pc settings':
                                        if DcAction.pc_Settings():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'connect settings':
                                        if DcAction.Connect_settings():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'projector settings':
                                        if DcAction.Projector_settings():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'search bar':
                                        if DcAction.pc_Search_Bar():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'snip':
                                        if DcAction.Snip():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'copy':
                                        if DcAction.Copy():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'cut':
                                        if DcAction.Cut():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'paste':
                                        if DcAction.Paste():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'save':
                                        if DcAction.Save():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'undo':
                                        if DcAction.Undo():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'redo':
                                        if DcAction.Redo():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'rename':
                                        if DcAction.Rename():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'backward':
                                        if DcAction.backward():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'forward':
                                        if DcAction.forward():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'explorer search':
                                        if DcAction.Explorer_search():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'address bar':
                                        if DcAction.Address_bar():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'task manager':
                                        if DcAction.Task_manager():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'hidden icons':
                                        if DcAction.show_Hidden_icons():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'task view':
                                        if DcAction.Task_view():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'run':
                                        if DcAction.Run():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'new folder':
                                        if DcAction.create_New_folder():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'clipboard':
                                        if DcAction.Clipboard():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'unindent':
                                        if DcAction.Unindent():
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass

                                    elif dc_command == 'type':
                                        global text
                                        global textChoice
                                        c = ['type', 'write']
                                        chk = []
                                        for i in c:
                                            if i in processed_message:
                                                chk.append(i)
                                        if len(chk)>0:
                                            temp = processed_message[(processed_message.index(chk[0])+1):]
                                            m=''
                                            for i in temp:
                                                m += i + ' '
                                            text = m[:-1]

                                        else:
                                            ralph_s.say('Dictate the text you want me to type. Start now')
                                            ralph_s.runAndWait()
                                            questionAvailable.append(1)
                                            if len(recording)>0:
                                                audio = get_speech()
                                                textChoice = get_message(audio)
                                            if len(sentMessage)>0:
                                                while len(answerToAvailableQuestion)==0:
                                                    print('')
                                                    if len(answerToAvailableQuestion)>0:
                                                        textChoice = answerToAvailableQuestion[-1]
                                                        break
                                            if textChoice:
                                                text = textChoice
                                                answerToAvailableQuestion.clear()
                                            else:
                                                ralph_s.say("No response received. Operation aborted")
                                                ralph_s.runAndWait()
                                                conversation.update({message: 'operation aborted'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                        print(text)
                                        if DcAction.Type(text):
                                            conversation.update({message: 'dc command successfully executed'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass
                                        else:
                                            ralph_s.say('Error. Please try again.')
                                            conversation.update({message: 'failed to executed dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass


                                    else:
                                        if dc_command == 'minimize':
                                            if DcAction.Minimize_windows():
                                                conversation.update({message: 'dc command successfully executed'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass
                                            else:
                                                ralph_s.say('Error. Please try again.')
                                                conversation.update({message: 'failed to executed dc command'})
                                                if len(recording)>0:
                                                    questionAvailable.clear()
                                                    answerToAvailableQuestion.clear()
                                                    ralph()
                                                else:
                                                    pass

                                        else:
                                            ralph_s.say('Sorry. I cant help with that.')
                                            ralph_s.runAndWait()
                                            conversation.update({message: 'unable to execute dc command'})
                                            if len(recording)>0:
                                                questionAvailable.clear()
                                                answerToAvailableQuestion.clear()
                                                ralph()
                                            else:
                                                pass








                        #********************************* No command received **********************************


                        elif ((message_intend == 'None') and ('windows' not in processed_message)):


                            response = Chat.Converse(message, conversation)
                            #print(response)
                            if response != None:
                                ralph_s.say(str(response))
                                ralph_s.runAndWait()
                            else:
                                pass















                    except sr.UnknownValueError:
                        pass


                    except sr.RequestError:
                        ralph_s.say("Sorry, I didn't get you. Please ensure that you are connected to the internet then try again")
                        ralph_s.runAndWait()
                        if len(recording)>0:
                            questionAvailable.clear()
                            answerToAvailableQuestion.clear()
                            ralph()
                        else:
                            pass


                else:
                    pass



            except:
                pass

            finally:
                recording.clear()
                sentMessage.clear()
                questionAvailable.clear()
                answerToAvailableQuestion.clear()

        else:
            pass







    #assistant runner
    def ai():
        func = lambda: ralph()
        thread = threading.Thread(target=func)
        thread.start()

    #animation runner
    def ralph_animation():
        MainApp = QApplication([])
        MainGui = UI_MainWindow()
        MainGui.show()
        sysExit(MainApp.exec_())
    #running the animation
    ralph_animation()




















if __name__ == '__main__':
    main()
