from error_massage import error_msg
import tkinter as tk
from tkinter.constants import SEL_FIRST
from tkinter import ttk

def frame(root):
    return tk.Frame(root)

def label(root, lbl_text):
    return tk.Label(root, text=lbl_text)

def entry(root, text_var):
    return tk.Entry(root, textvariable=text_var)

def button(root, btn_text, btn_cmnd):
    return tk.Button(root, text=btn_text, command=btn_cmnd)

def lblframe(root, frame_text):
    return tk.LabelFrame(root, text=frame_text)

def pane(root):
    return tk.PanedWindow(root)

def list_box(root):
    return tk.Listbox(root)

def scroll_bar(root):
    return tk.Scrollbar(root)

def top_level():
    return tk.Toplevel()

def listbox(root,listbox_items : list):
    
    list_box = tk.Listbox(root)
    
    for index,items in enumerate(listbox_items):
        list_box.insert(index + 1, str(items))
    
    return list_box

def drop_down(root, var, data):
    if not data:
        error_msg('Empty Columns')
    else:
        return tk.OptionMenu(root, var, *data)

def canvas(root):
    return tk.Canvas(root)