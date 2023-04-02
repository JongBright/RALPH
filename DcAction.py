import os
import time
from pynput.keyboard import Key, Controller


keyboard = Controller()









#press letter or number
def press_key(k, n=1):
    try:
        for i in range(n):
            keyboard.press(k)
            keyboard.release(k)
        return True
    except:
        return False


#hold letter or number
def hold_key(k):
    try:
        keyboard.press(k)
        return True
    except:
        return False


#up                                        up
def up(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.up)
            keyboard.release(Key.up)
        return True
    except:
        return False


#down                                       down
def down(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.down)
            keyboard.release(Key.down)
        return True
    except:
        return False


#right                                        right
def right(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.right)
            keyboard.release(Key.right)
        return True
    except:
        return False


#left                                           left
def left(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.left)
            keyboard.release(Key.left)
        return True
    except:
        return False


#function 1 to 12                                f1 - f12
def func1(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f1)
            keyboard.release(Key.f1)
        return True
    except:
        return False

def func2(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f2)
            keyboard.release(Key.f2)
        return True
    except:
        return False

def func3(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f3)
            keyboard.release(Key.f3)
        return True
    except:
        return False

def func4(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f4)
            keyboard.release(Key.f4)
        return True
    except:
        return False

def func5(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f5)
            keyboard.release(Key.f5)
        return True
    except:
        return False

def func6(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f6)
            keyboard.release(Key.f6)
        return True
    except:
        return False

def func7(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f7)
            keyboard.release(Key.f7)
        return True
    except:
        return False

def func8(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f8)
            keyboard.release(Key.f8)
        return True
    except:
        return False

def func9(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f9)
            keyboard.release(Key.f9)
        return True
    except:
        return False

def func10(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f10)
            keyboard.release(Key.f10)
        return True
    except:
        return False

def func11(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f11)
            keyboard.release(Key.f11)
        return True
    except:
        return False

def func12(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f12)
            keyboard.release(Key.f12)
        return True
    except:
        return False



#print screen                                      prtsc
def print_screen(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.print_screen)
            keyboard.release(Key.print_screen)
        return True
    except:
        return False


#caps lock                                         caps lock
def caps_lock(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.caps_lock)
            keyboard.release(Key.caps_lock)
        return True
    except:
        return False


#start menu                                         start menu
def start_menu(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.release(Key.cmd)
        return True
    except:
        return False


#backspace                                           backspace
def backspace(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.backspace)
            keyboard.release(Key.backspace)
        return True
    except:
        return False



#space bar                                     space
def space(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.space)
            keyboard.release(Key.space)
        return True
    except:
        return False


#escape                                        escape
def escape(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
        return True
    except:
        return False



#tab                                            tab, indent
def tab(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
        return True
    except:
        return False



#alternative                                     alt
def alt(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.release(Key.alt)
        return True
    except:
        return False


#control                                          ctrl
def ctrl(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.release(Key.ctrl)
        return True
    except:
        return False


#home                                               home
def home(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.home)
            keyboard.release(Key.home)
        return True
    except:
        return False


#end                                                end
def end(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.end)
            keyboard.release(Key.end)
        return True
    except:
        return False


#insert                                             insert
def insert(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.insert)
            keyboard.release(Key.insert)
        return True
    except:
        return False


#scroll lock                                         scroll lock
def scroll_lock(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.scroll_lock)
            keyboard.release(Key.scroll_lock)
        return True
    except:
        return False


#num lock                                            num lock
def num_lock(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.num_lock)
            keyboard.release(Key.num_lock)
        return True
    except:
        return False


#pause                                                pause
def pause(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.pause)
            keyboard.release(Key.pause)
        return True
    except:
        return False


#enter                                                enter
def enter(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        return True
    except:
        return False


#delete                                                delete
def delete(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.delete)
            keyboard.release(Key.delete)
        return True
    except:
        return False


#shift                                                  shift
def shift(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.shift)
            keyboard.release(Key.shift)
        return True
    except:
        return False


#page up                                                page up, scroll up
def page_up(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.page_up)
            keyboard.release(Key.page_up)
        return True
    except:
        return False


#page down                                              page down, scroll down
def page_down(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.page_down)
            keyboard.release(Key.page_down)
        return True
    except:
        return False


#left click                                            left click, select
def left_click(n=1):
    from pynput.mouse import Button, Controller
    mouse = Controller
    try:
        for i in range(n):
            mouse.click(Button.left, 1)
        return True
    except:
        return False


#right click                                            right click
def right_click(n=1):
    from pynput.mouse import Button, Controller
    mouse = Controller()
    try:
        for i in range(n):
            mouse.click(Button.right, 1)
        return True
    except:
        return False


#click                                                 click
def click(n=1):
    from pynput.mouse import Button, Controller
    mouse = Controller()
    try:
        for i in range(n):
            mouse.click(Button.left, 2)
        return True
    except:
        return False



#open properties                                        properties
def open_Properties(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#change window                                          change window
def change_Window(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#cycle through taskbar apps                                 change taskbar app
def change_Taskbar_App(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('t')
            keyboard.release('t')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#show opened windows                                          opened windows
def show_Opened_windows(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press(Key.alt)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.release(Key.ctrl)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#close window                                       close
def Close(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.f4)
            keyboard.release(Key.f4)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#shortcut menu for active window                        shortcut menu
def Shortcut_menu(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#select all                              select all
def Select_all(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('a')
            keyboard.release('a')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#refresh                                 refresh
def Refresh(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f5)
            keyboard.release(Key.f5)
        return True
    except:
        return False


#quick link menu                            quick link menu
def Quick_link_menu(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('x')
            keyboard.release('x')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#open action center                           action center
def Action_center(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('a')
            keyboard.release('a')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#navigate to/from desktop                            desktop
def Desktop(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('d')
            keyboard.release('d')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#minimize all opened windows                     minimize
def Minimize_windows(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('m')
            keyboard.release('m')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#restore all the minimized windows                           restore minimized windows
def Restore_minimized_windows(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press(Key.shift)
            keyboard.press('m')
            keyboard.release('m')
            keyboard.release(Key.cmd)
            keyboard.release(Key.shift)
        return True
    except:
        return False



#maximize current window                             maximize
def Maximize_window(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#open this pc/file explorer                       pc
def thisPC(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('e')
            keyboard.release('e')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#open pc settings                           pc settings
def pc_Settings(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('i')
            keyboard.release('i')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#open connect settings                    connect settings
def Connect_settings(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('k')
            keyboard.release('k')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#open projector settings                         projector settings
def Projector_settings(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('p')
            keyboard.release('p')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#windows search bar                          search bar
def pc_Search_Bar(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('s')
            keyboard.release('s')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#use snipper tool                         snip
def Snip(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press(Key.print_screen)
            keyboard.release(Key.print_screen)
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#copy                           copy
def Copy(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('c')
            keyboard.release('c')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False


#cut                              cut
def Cut(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('x')
            keyboard.release('x')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#paste                          paste
def Paste(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#save                         save
def Save(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('s')
            keyboard.release('s')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#undo                               undo
def Undo(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('z')
            keyboard.release('z')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False


#redo                          redo
def Redo(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press('y')
            keyboard.release('y')
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#rename                      rename
def Rename(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f2)
            keyboard.release(Key.f2)
        return True
    except:
        return False



#backward                                            backward
def backward(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.left)
            keyboard.release(Key.left)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#forward                                              forward
def forward(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.alt)
            keyboard.press(Key.right)
            keyboard.release(Key.right)
            keyboard.release(Key.alt)
        return True
    except:
        return False



#search in file explorer                     explorer search
def Explorer_search(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f3)
            keyboard.release(Key.f3)
        return True
    except:
        return False



#focus on address bar                         address bar
def Address_bar(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.f4)
            keyboard.release(Key.f4)
        return True
    except:
        return False



#open task manager                         task manager
def Task_manager(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.shift)
            keyboard.press(Key.ctrl)
            keyboard.press(Key.esc)
            keyboard.release(Key.esc)
            keyboard.release(Key.shift)
            keyboard.release(Key.ctrl)
        return True
    except:
        return False



#focus on notification center / show hidden icons                   hidden icons
def show_Hidden_icons(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('b')
            keyboard.release('b')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#task view / recent activity                        task view
def Task_view(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#run                        run
def Run(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('r')
            keyboard.release('r')
            keyboard.release(Key.cmd)
        return True
    except:
        return False



#create new folder                        new folder
def create_New_folder(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.ctrl)
            keyboard.press(Key.shift)
            keyboard.press('n')
            keyboard.release('n')
            keyboard.release(Key.ctrl)
            keyboard.release(Key.shift)
        return True
    except:
        return False



#open the clipboard                      clipboard
def Clipboard(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.cmd)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.cmd)
        return True
    except:
        return False


#unindent                                 unindent
def Unindent(n=1):
    try:
        for i in range(n):
            keyboard.press(Key.shift)
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            keyboard.release(Key.shift)
        return True
    except:
        return False


#commandline                   command prompt
def cmd(n=1):
    try:
        for i in range(n):
            os.startfile('C:\Windows\system32\cmd.exe')
        return True
    except:
        return False

#powershell                   powershell
def powershell(n=1):
    try:
        for i in range(n):
            os.startfile('C:\\Windows\\system32\\WindowsPowerShell\\v1.0\\powershell.exe')
        return True
    except:
        return False

#typing                               type
def Type(text, n=1):
    try:
        for i in range(n):
            for char in text:
                keyboard.press(char)
                keyboard.release(char)
                time.sleep(0.02)
        return True
    except:
        return False



