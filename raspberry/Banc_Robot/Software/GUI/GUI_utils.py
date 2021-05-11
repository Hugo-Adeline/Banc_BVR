# -*- coding: utf-8 -*-

import tkinter as tk
from PIL import Image, ImageTk

decision = None
buttonHeight = 1
buttonWidth = 8

def SwitchWindow(frame,root):


    if root.activeFrame != None:
        root.activeFrame.pack_forget()
    root.activeFrame = frame
    root.activeFrame.config()
    frame.pack(fill= 'both', expand = 'yes')

    return


def Popup(self, popupType, titre= "Attention", texte= "Erreur", fermer= "Fermer", valider= "Valider"):
    popup = tk.Toplevel()
    popup.title(titre)
    popup.transient(self.root)
    popup.attributes('-topmost', 'true')
    popup.grab_set()
    popup.resizable(False, False)
    icon = tk.PhotoImage(file= self.root.imageDict['Warning'])
    popup.tk.call('wm', 'iconphoto', popup._w, icon)
    label = tk.Label(popup, text= texte)
    label.config(font = self.root.fontLabel)
    label.pack(pady = 6, padx = 5)
    if popupType == 1:
        button = tk.Button(popup, text= fermer, command=popup.destroy)
        button.config(font = self.root.fontButton, height= buttonHeight, width= buttonWidth)
        button.pack(padx=10, pady=10)
    elif popupType == 2:
        button = tk.Button(popup, text= valider, command= lambda: _Validate(popup))
        button.config(font = self.root.fontButton, height= buttonHeight, width= buttonWidth, fg= 'dark green')
        button.pack(side= 'left', padx = 40, pady=10)
        button = tk.Button(popup, text= fermer, command= lambda: _Close(popup))
        button.config(font = self.root.fontButton, height= buttonHeight, width= buttonWidth, fg= 'red3')
        button.pack(side = 'right', padx = 40, pady=10)
    if popupType == 3:
        image = Image.open()
        render = ImageTk.PhotoImage(image)
        imgLabel = tk.Label(self.shifterFrame, image=render)
        imgLabel.pack()
        button = tk.Button(popup, text= valider, command= lambda: _Validate(popup))
        button.config(font = self.root.fontButton, height= buttonHeight, width= buttonWidth, fg= 'dark green')
        button.pack(side= 'left', padx = 40, pady=10)
        button = tk.Button(popup, text= fermer, command= lambda: _Close(popup))
        button.config(font = self.root.fontButton, height= buttonHeight, width= buttonWidth, fg= 'red3')
        button.pack(side = 'right', padx = 40, pady=10)
    center(popup)
    self.root.wait_window(popup)
    return decision

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def _Validate(popup):
    global decision
    decision = True
    popup.destroy()
    return

def _Close(popup):
    global decision
    decision = False
    popup.destroy()
    return

def RefreshOptionMenu(self):
    self.robotList = self.root.dB.GetRobotNameList()
    self.robotList = sorted(self.robotList)
    menu = self.om["menu"]
    menu.delete(0, "end")
    for string in self.robotList:
        menu.add_command(label=string, command=lambda value=string: self.robotSelected.set(value))
    menu.config(bg= 'white', font= self.root.fontButton)
    return
