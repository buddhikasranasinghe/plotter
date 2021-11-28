from tkinter import messagebox

def information_msg(information_text):
    return messagebox.showinfo(title='Information', message=information_text)

def error_msg(error_text):
    return messagebox.showerror(title='Error', message=error_text)

def yesno(msg):
    result = messagebox.askyesno(title='Question', message=msg)
    return result