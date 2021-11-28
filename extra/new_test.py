"""
import tkinter as tk
import tkinter.ttk as ttk
from ctypes import windll

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

def main():
    root = tk.Tk()
    root.wm_title("AppWindow Test")
    button = ttk.Button(root, text='Exit', command=lambda: root.destroy())
    button.grid(row=0, column=0)
    btn_minimize = ttk.Button(root, text='minimize', command=lambda: root.iconify())
    btn_minimize.grid(row=0, column=1)
    root.overrideredirect(True)
    root.after(10, lambda: set_appwindow(root))
    root.mainloop()

if __name__ == '__main__':
    main()


import tkinter as tk
from ctypes import windll
from tkinter.constants import LEFT, X

GWL_EXSTYLE=-20
WS_EX_APPWINDOW=0x00040000
WS_EX_TOOLWINDOW=0x00000080

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

class Main():
    def __init__(self, root):
        self.root = root

        #self.overrideredirect()

        frame = tk.Frame(self.root, background='maroon1')
        frame.pack(fill=X)
        frame.bind('<ButtonPress-1>', self.get_pos)
        frame.bind('<ButtonRelease-1>', self.relese)
        frame.bind('<B1-Motion>', self.move_window)

        #frame.bind('<Button-3>', self.show_screen)
        #frame.bind('<Map>', self.screen_apear)
        lable = tk.Label(frame, text='Testing Window', background='maroon1', foreground='white')
        lable.pack(side=LEFT)

        content_frame = tk.Frame(self.root)
        content_frame.pack()

        btn_close = tk.Button(content_frame, text='Close', command=self.close)
        btn_close.grid(row=0, column=0)

        btn_min = tk.Button(content_frame, text='minimize', command=self.minimize)
        btn_min.grid(row=0, column=1)

        lbl_two = tk.Label(content_frame, text='test lable')
        lbl_two.grid(row=0, column=2)

    def overrideredirect(self):
        root.overrideredirect(True)
        
        #if boolean:
        print("Setting")
        hwnd = windll.user32.GetParent(root.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style = style & ~WS_EX_TOOLWINDOW
        style = style | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        root.wm_withdraw()
        root.wm_deiconify()

    def close(self):
        root.destroy()

    def minimize(self):
        root.overrideredirect(False)
        root.iconify()

    def get_pos(self, event):
        self.x = event.x
        self.y = event.y

    def relese(self, event):
        self.x = None
        self.y = None

    def show_screen(self, event):
        root.deiconify()
        root.overrideredirect(0)
        #root.after(10, lambda: set_appwindow(root))
        #root.wm_withdraw()
        #root.after(5000, lambda: root.wm_deiconify())

    def screen_apear(self, event):
        root.overrideredirect(1)
        #root.after(10, lambda: set_appwindow(root))

    def move_window(self, event):
        delx = event.x - self.x
        dely = event.y - self.y
        xw = root.winfo_x() + delx
        yw = root.winfo_y() + dely
        root.geometry('+{0}+{1}'.format(xw,yw))

if __name__=='__main__':
    root = tk.Tk()
    Main(root)
    root.overrideredirect(True)
    root.after(10, lambda: set_appwindow(root))
    #root.after(10, lambda: set_appwindow(root))
    #root.attributes('-alpha', 0.5)
    image = tk.PhotoImage(file='logo.ico')
    root.iconphoto(True, image)
    root.mainloop()
    
""" 

from tkinter import *
from ctypes import windll

# Some WindowsOS styles, required for task bar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

lastClickX = 0
lastClickY = 0


def SaveLastClickPos(event):
    global lastClickX, lastClickY
    lastClickX = event.x
    lastClickY = event.y


def Dragging(event):
    x, y = event.x - lastClickX + mainWindow.winfo_x(), event.y - lastClickY + mainWindow.winfo_y()
    mainWindow.geometry("+%s+%s" % (x , y))

def set_appwindow(mainWindow):
    # Honestly forgot what most of this stuff does. I think it's so that you can see
    # the program in the task bar while using overridedirect. Most of it is taken
    # from a post I found on stackoverflow.
    hwnd = windll.user32.GetParent(mainWindow.winfo_id())
    stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
    stylew = stylew & ~WS_EX_TOOLWINDOW
    stylew = stylew | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
    # re-assert the new window style
    mainWindow.wm_withdraw()
    mainWindow.after(10, lambda: mainWindow.wm_deiconify())


def main():
    global mainWindow, z
    # Default window configuration
    mainWindow = Tk()
    mainWindow.geometry('800x400')
    mainWindow.resizable(width=False, height=False)
    mainWindow.overrideredirect(True)
    mainWindow.after(10, lambda: set_appwindow(mainWindow))
    mainWindow.bind('<Button-1>', SaveLastClickPos)
    mainWindow.bind('<B1-Motion>', Dragging)
    z = 0

    def exitGUI():
        mainWindow.destroy()

    def minimizeGUI():
        global z
        mainWindow.state('withdrawn')
        mainWindow.overrideredirect(False)
        mainWindow.state('iconic')
        z = 1

    def frameMapped(event=None):
        global z
        mainWindow.overrideredirect(True)
        mainWindow.iconbitmap("logo.ico")
        if z == 1:
            set_appwindow(mainWindow)
            z = 0


    exitButton = Button(mainWindow, text='', bg='#212121', fg='#35DAFF',
                        command=exitGUI)
    minimizeButton = Button(mainWindow, text='', bg="#212121", fg='#35DAFF',
                            command=minimizeGUI)
    exitButton.place(x=780, y=0)
    minimizeButton.place(x=759, y=0)
    mainWindow.bind("<Map>", frameMapped)  # This brings back the window
    mainWindow.mainloop()  # Window Loop


if __name__ == '__main__':
    main()
