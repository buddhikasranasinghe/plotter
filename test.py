from tkinter import Toplevel, font
from tkinter import tix
from typing import Counter
from back import Back
import tkinter as tk
from tkinter import PhotoImage, ttk
from tkinter import messagebox as msg
from tkinter.constants import ACTIVE, ANCHOR, BOTH, BOTTOM, DISABLED, END, FLAT, HORIZONTAL, INSERT, LEFT, NORMAL, RIGHT, TOP, VERTICAL, X, Y
import statistics
import re
import matplotlib.pyplot as plt
from tkinter.tix import *

class Tooltip(object):
    def __init__(self, widget, text='Widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.leave)
        self.widget.bind('<ButtonPress>', self.leave)
        self.id = None
        self.tw = None

    def enter(self, event = None):
        self.shedule()

    def leave(self, event = None):
        self.unshedule()
        self.hidetip()

    def shedule(self):
        self.unshedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unshedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="gray80", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


class PopupWindow(object):
    def __init__(self, master):
        
        self.new_entered_val = tk.StringVar()

        self.top = Toplevel(master)
        self.top.overrideredirect(True)

        self.top.geometry('269x117+610+400')
        frame = tk.Frame(self.top, background='#00022e')
        frame.pack()
        
        #========= custom title bar =============
        frame_custom = tk.Frame(frame, background='cyan4')
        frame_custom.pack(fill=X)

        frame_custom.bind('<ButtonPress-1>', self.popup_get_pos)
        frame_custom.bind('<ButtonRelease-1>', self.popup_relese)
        frame_custom.bind('<B1-Motion>', self.popup_move_window)

        frame_custom.bind('<Button-3>', self.popup_show_screen)
        frame_custom.bind('<Map>', self.popup_screen_apear)

        title_pane = tk.PanedWindow(frame_custom, background='cyan4')
        title_pane.pack(side=LEFT)

        title_lbl = tk.Label(title_pane, text='Update', background='cyan4', foreground='White')
        title_lbl.pack()

        btn_pane = tk.PanedWindow(frame_custom, background='cyan4')
        btn_pane.pack(side=RIGHT)
        
        popup_minimize = tk.Button(btn_pane, text='-', command=self.mnimize, relief=FLAT, border=0, background='cyan4', activebackground='cyan4', foreground='white', activeforeground='maroon1')
        popup_minimize.pack(side=LEFT, padx=5)

        popup_close = tk.Button(btn_pane, text='X', command=self.top.destroy, relief=FLAT, border=0, background='cyan4', activebackground='cyan4', foreground='white', activeforeground='maroon1')
        popup_close.pack(side=LEFT, padx=5)
        

        lbl_frame = tk.Frame(frame, background='#00022e')
        lbl_frame.pack(padx=5, pady=5)

        lbl = tk.Label(lbl_frame, text='Enter New Value ', background='#00022e', foreground='White')
        lbl.grid(row=0, column=0, padx=10, pady=10)

        self.entry_new_value = tk.Entry(lbl_frame, textvariable=self.new_entered_val)
        self.entry_new_value.grid(row=0, column=1, padx=10, pady=10)
        Tooltip(self.entry_new_value, 'Enter New Value Here')

        btn_ok = tk.Button(lbl_frame, text='OK', command= self.btn_ok, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', relief=FLAT, border=0)
        btn_ok.grid(row=1, column=0, padx=10, pady=10, sticky='we')

        btn_cancel = tk.Button(lbl_frame, text='Cancel', command= self.btn_cancel, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', relief=FLAT, border=0)
        btn_cancel.grid(row=1, column=1, padx=10, pady=10, sticky='we')

    def btn_ok(self):
        self.new_value = self.entry_new_value.get()
        self.top.destroy()

    def btn_cancel(self):
        self.top.destroy()

    def mnimize(self):
        self.top.overrideredirect(False)
        self.top.iconify()

    def popup_get_pos(self, event):
        self.x = event.x
        self.y = event.y

    def popup_relese(self, event):
        self.x = None
        self.y = None

    def popup_move_window(self, event):
        delx = event.x - self.x
        dely = event.y - self.y
        xw = self.top.winfo_x() + delx
        yw = self.top.winfo_y() + dely
        self.top.geometry('+{0}+{1}'.format(xw,yw))

    def popup_show_screen(self, event):
        self.top.deiconify()
        self.top.overrideredirect(1)

    def popup_screen_apear(self, event):
        self.top.overrideredirect(1)


class Main():
    def __init__(self, root):
        self.root = root

        # etry variables
        self.table_name = tk.StringVar()
        self.column_name = tk.StringVar()
        self.column_value = tk.StringVar()
        self.graph_name = tk.StringVar()
        self.show_operation = tk.StringVar()
        self.update_value = tk.StringVar()

        # list variables
        self.data_frame_name_list = []
        self.column_value_list = []
        self.dataframes_object_list = []

        # dictionary variables
        self.dataframe_key_value_dict = {}

        # combobox variables
        self.combo_get_x = tk.StringVar()
        self.combo_get_y = tk.StringVar()
        self.combo_get_operation_column = tk.StringVar()

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        tip = Balloon(root)

        #============ Header Window ===========
        header_pane = tk.PanedWindow(self.frame, background='cyan4')
        header_pane.pack(fill=BOTH, expand=True)

        header_pane.bind('<ButtonPress-1>', self.get_pos)
        header_pane.bind('<ButtonRelease-1>', self.relese)
        header_pane.bind('<B1-Motion>', self.move_window)

        header_pane.bind('<Button-3>', self.show_screen)
        header_pane.bind('<Map>', self.screen_apear)
        

            #--------- header title pane ----------
        header_title_pane = tk.PanedWindow(header_pane, background='cyan4')
        header_title_pane.pack(side=LEFT)
        
        header_title = tk.Label(header_title_pane ,text='OrcaPlotter', background='cyan4', foreground='White', font='Arial 10 bold')
        header_title.pack(expand=True, fill=BOTH, padx=5)

            #--------- header system button pane ----------
        header_system_button_pane = tk.PanedWindow(header_pane, background='cyan4')
        header_system_button_pane.pack(side=RIGHT)

        header_button_minimize = tk.Button(header_system_button_pane, text='-', command=self.minimize, background='cyan4', activebackground='cyan4', relief=FLAT, border=0, font='Arial 10 bold', foreground='White', activeforeground='maroon1')
        header_button_minimize.pack(side=LEFT, padx=5)
        Tooltip(header_button_minimize, 'Minimize')

        self.header_button_close = tk.Button(header_system_button_pane, text='X', command=self.quite, background='cyan4', activebackground='cyan4', relief=FLAT, border=0, font='Arial 10 bold', foreground='White', activeforeground='maroon1')
        self.header_button_close.pack(side=LEFT, padx=5)
        Tooltip(self.header_button_close, 'Exit')

        #============ Content Window ===========
        content_pane = tk.PanedWindow(self.frame, background='#00022e')
        content_pane.pack(fill=BOTH, expand=True)

            #-------- content controll pane -------------
        content_controll_pane = tk.PanedWindow(content_pane, background='#00022e')
        content_controll_pane.pack(fill=BOTH, expand=True)
            
            # button pane
        control_button_pane = tk.PanedWindow(content_controll_pane, background='#00022e')
        control_button_pane.pack(side=LEFT)

        self.controll_button_prev = tk.Button(control_button_pane, text='<', state=DISABLED, command=self.back, background='#00022e',  activebackground='#00022e', relief=FLAT, border=0, foreground='White', font='Arial 15 bold', activeforeground='maroon1')
        self.controll_button_prev.pack(side=LEFT, padx=5, pady=5)
        Tooltip(self.controll_button_prev, 'Previous')

        self.show_table_name = tk.Label(control_button_pane, text='No Table', background='#00022e', foreground='cyan2', font='Arial 13 bold')
        self.show_table_name.pack(side=LEFT, padx=5, pady=5)

        self.controll_button_next = tk.Button(control_button_pane, text='>', state=DISABLED, command=self.next, background='#00022e', activebackground='#00022e', relief=FLAT, border=0, foreground='White', font='Arial 15 bold', activeforeground='maroon1')
        self.controll_button_next.pack(side=LEFT, padx=5, pady=5)
        Tooltip(self.controll_button_next, 'Next')

            # table name pane
        control_table_name_pane = tk.PanedWindow(content_controll_pane, background='#00022e')
        control_table_name_pane.pack(side=RIGHT)

        self.input_table_name = tk.Label(control_table_name_pane, text='Table name ', background='#00022e', foreground='White', font='Arial 13 normal')
        self.input_table_name.pack(side=LEFT, padx=5, pady=5)

        self.get_table_name = tk.Entry(control_table_name_pane, textvariable=self.table_name, background='gray70', font='Arial 10 normal')
        self.get_table_name.pack(side=LEFT, padx=5, pady=5)
        Tooltip(self.get_table_name, 'Table Name')

        self.btn_create_table = tk.Button(control_table_name_pane, text='Create', command= lambda: self.create_table(self.table_name.get(), self.data_frame_name_list), font='Arial 10 bold', background='#00022e', foreground='cyan2', activebackground='#00022e', activeforeground='maroon1', relief=FLAT, border=0)
        self.btn_create_table.pack(side=LEFT, padx=5, pady=5)
        Tooltip(self.btn_create_table, 'Create Table')

        self.btn_create_new_table = tk.Button(control_table_name_pane, text='Create New Table', command=self.show_create_table, font='Arial 10 bold', background='#00022e', activebackground='#00022e', activeforeground='maroon1', foreground='cyan2', relief=FLAT, border=0)
        Tooltip(self.btn_create_new_table, 'Create Table')

            #-------------- content visible pane --------------
        content_visible_pane = tk.PanedWindow(content_pane, background='#00022e')
        content_visible_pane.pack(fill=BOTH, expand=True)

            # --------- column details --------------------
        lbl_column_details = tk.LabelFrame(content_visible_pane, text='Column Details', background='#00022e', foreground='White', font='Arial 13 bold')
        lbl_column_details.pack(side=LEFT, expand=True, padx=5, pady=2.5)

            # get column values pane
        pane_get_data = tk.PanedWindow(lbl_column_details, background='#00022e')
        pane_get_data.pack(expand=True)

        text_column_name = tk.Label(pane_get_data, text='Column Name ', background='#00022e', foreground='Gray64', font='Arial 10 bold')
        text_column_name.grid(row=0, column=0, sticky='we', padx=5, pady=5)

        self.get_column_name = tk.Entry(pane_get_data, textvariable=self.column_name, font='Arial 10 normal', background='gray75')
        self.get_column_name.grid(row=0, column=1, sticky='we', padx=5, pady=5)
        Tooltip(self.get_column_name, 'Enter Column Name Here')

        text_column_value = tk.Label(pane_get_data, text='Column Value ', background='#00022e', foreground='Gray64', font='Arial 10 bold')
        text_column_value.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        
        self.get_column_value = tk.Entry(pane_get_data, textvariable=self.column_value, font='Arial 10 normal', background='gray75')
        self.get_column_value.grid(row=1, column=1, sticky='we', padx=5, pady=5)
        Tooltip(self.get_column_value, 'Enter Column Value Here')

            # column value add button
        pane_btn_add = tk.PanedWindow(lbl_column_details, background='#00022e')
        pane_btn_add.pack(fill=BOTH, expand=True)

        btn_add_column_value = tk.Button(pane_btn_add, text='Add', command= lambda : self.add_value(self.column_value.get()), font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_add_column_value.pack(padx=5, pady=5)
        Tooltip(btn_add_column_value, 'Add Column Value')

            # show add values with list box
        pane_show_column_details = tk.PanedWindow(lbl_column_details, background='#00022e')
        pane_show_column_details.pack(expand=True)

        text_column_values = tk.Label(pane_show_column_details, text='Column Values ', background='#00022e', foreground='gray64')
        text_column_values.grid(row=0, column=0)

        text_column_names = tk.Label(pane_show_column_details, text='Column Names ', background='#00022e', foreground='gray64')
        text_column_names.grid(row=0, column=1)

        pane_show_column_values = tk.PanedWindow(pane_show_column_details, background='#00022e')
        pane_show_column_values.grid(row=1, column=0)

        self.column_values_list_box = tk.Listbox(pane_show_column_values, width=15, font='Arial 10 normal', background='Gray64')
        self.column_values_list_box.pack(side=LEFT)
        self.column_values_list_box.bind('<<ListboxSelect>>', self.click_column_values)

        column_value_scroll = tk.Scrollbar(pane_show_column_values)
        column_value_scroll.pack(side=RIGHT, fill=Y)
        self.column_values_list_box.config(yscrollcommand=column_value_scroll.set)
        column_value_scroll.config(command=self.column_values_list_box.yview)

        pane_show_column_names = tk.PanedWindow(pane_show_column_details, background='#00022e')
        pane_show_column_names.grid(row=1, column=1)

        self.column_names_list_box = tk.Listbox(pane_show_column_names, width=15, font='Arial 10 normal', background='Gray64')
        self.column_names_list_box.pack(side=LEFT)
        self.column_names_list_box.bind('<<ListboxSelect>>', self.click_column_name)

        column_name_scroll = tk.Scrollbar(pane_show_column_names)
        column_name_scroll.pack(side=RIGHT, fill=Y)
        self.column_names_list_box.config(yscrollcommand=column_name_scroll.set)
        column_name_scroll.config(command=self.column_names_list_box.yview)

            # column operation buttons
        pane_bottom_buttons = tk.PanedWindow(lbl_column_details, background='#00022e')
        pane_bottom_buttons.pack( expand=True)

        btn_cancel = tk.Button(pane_bottom_buttons, text='Cancel', command=self.cancel, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_cancel.grid(row=0, column=0, sticky='we', padx=5, pady=5)
        Tooltip(btn_cancel, 'Cancel')

        btn_add_column = tk.Button(pane_bottom_buttons, text='Add Column', command=lambda :self.add_column(self.column_name.get()), font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_add_column.grid(row=0, column=1, sticky='we', padx=5, pady=5)
        Tooltip(btn_add_column, 'Add Column')

        btn_delete_table = tk.Button(pane_bottom_buttons, text='Drop Table', command=self.drop_table, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_delete_table.grid(row=0, column=2, sticky='we', padx=5, pady=5)
        Tooltip(btn_delete_table, 'Delete Table')

        self.btn_update_column = tk.Button(pane_bottom_buttons, text='Update', command=self.update, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        self.btn_update_column.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        Tooltip(self.btn_update_column, 'Update Selected\nValue or Column')

        btn_delete = tk.Button(pane_bottom_buttons, text='Delete', command=self.delete, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_delete.grid(row=1, column=1, sticky='we', padx=5, pady=5)
        Tooltip(btn_delete, 'Delete Selected\nValue or Column')

        btn_delete_column = tk.Button(pane_bottom_buttons, text='Drop Column', command=self.drop_column, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        btn_delete_column.grid(row=1, column=2, sticky='we', padx=5, pady=5)
        Tooltip(btn_delete_column, 'Delete Column')

            # --------- table details --------------------
        lbl_table_details = tk.LabelFrame(content_visible_pane, text='Table Details', background='#00022e', foreground='White', font='Arial 13 bold')
        lbl_table_details.pack(fill=BOTH, side=LEFT, expand=True, padx=5, pady=2.5)

        self.text_table_name = tk.Label(lbl_table_details, text='Table Name', background='#00022e', foreground='maroon1', font='Arial 13 bold')
        self.text_table_name.pack(padx=5, pady=5)

        lblf_virtual_table = tk.LabelFrame(lbl_table_details, text='', background='#00022e', foreground='White', font='Arial 13 bold')
        lblf_virtual_table.pack(fill=BOTH, expand=True)

        canvas_table = tk.Canvas(lblf_virtual_table)
        canvas_table.pack(side=LEFT, fill=BOTH)

        table_h_scroll = ttk.Scrollbar(lblf_virtual_table, orient=VERTICAL, command=canvas_table.yview)
        table_h_scroll.pack(side=RIGHT, fill=Y)
        
        self.table_frame = ttk.Frame(canvas_table)
        canvas_table.configure(yscrollcommand=table_h_scroll.set)
        self.table_frame.bind('<Configure>', lambda e: canvas_table.configure(scrollregion=canvas_table.bbox('all')))
        canvas_table.create_window((0,0), window=self.table_frame, anchor='nw')

        table_v_scroll = tk.Scrollbar(lbl_table_details, orient=HORIZONTAL, command=canvas_table.xview)
        table_v_scroll.pack(fill=X)
        canvas_table.configure(xscrollcommand=table_v_scroll.set)

            # --------- graph details --------------------
        lbl_graph_details = tk.LabelFrame(content_visible_pane, text='Operations', background='#00022e', foreground='White', font='Arial 13 bold')
        lbl_graph_details.pack(side=LEFT, expand=True, padx=5, pady=2.5, fill=BOTH)

            # get graph details
        pane_get_graph_details = tk.PanedWindow(lbl_graph_details,  background='#00022e')
        pane_get_graph_details.pack(fill=BOTH, expand=True)

        """text_graph_title = tk.Label(pane_get_graph_details, text='Graph Name ', background='#00022e', foreground='gray64', font='Arial 10 normal')
        text_graph_title.grid(row=3, column=0, sticky='we', padx=5, pady=5)

        self.enty_graph_title = tk.Entry(pane_get_graph_details, textvariable=self.graph_name, background='gray64', font='Arial 10 normal')
        self.enty_graph_title.grid(row=3, column=1, sticky='we', padx=5, pady=5)

        text_graph_x = tk.Label(pane_get_graph_details, text='Select X Axis ', background='#00022e', foreground='gray64', font='Arial 10 normal')
        text_graph_x.grid(row=1, column=0, sticky='we', padx=5, pady=5)

        self.combo_x_axis = ttk.Combobox(pane_get_graph_details, textvariable=self.combo_get_x, background='gray64', font='Arial 10 normal')
        self.combo_x_axis.grid(row=1, column=1, sticky='we', padx=5, pady=5)

        text_graph_y = tk.Label(pane_get_graph_details, text='Select Y Axis ', background='#00022e', foreground='gray64', font='Arial 10 normal')
        text_graph_y.grid(row=2, column=0, sticky='we', padx=5, pady=5)

        self.combo_y_axis = ttk.Combobox(pane_get_graph_details, textvariable=self.combo_get_y, background='gray64', font='Arial 10 normal')
        self.combo_y_axis.grid(row=2, column=1, sticky='we', padx=5, pady=5)

            # button plot
        pane_btn_plot = tk.PanedWindow(lbl_graph_details, background='#00022e')
        pane_btn_plot.pack(expand=True)

        btn_plot = tk.Button(pane_btn_plot, text='Plot', command=self.plot,relief=FLAT, background='#00022e', font='Arial 10 bold', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1')
        btn_plot.pack(side=TOP)"""

            # column operations
        pane_column_operation = tk.PanedWindow(lbl_graph_details, background='#00022e')
        pane_column_operation.pack(fill=BOTH, expand=True)

        lblf_column_opetration = tk.LabelFrame(pane_column_operation, text='', background='#00022e', foreground='White', font='Arial 13 bold')
        lblf_column_opetration.pack(fill=BOTH)
            
            # get and show operation
        pane_select_column = tk.PanedWindow(lblf_column_opetration, background='#00022e')
        pane_select_column.pack(fill=BOTH)

        text_select_column = tk.Label(pane_select_column, text='Select Column ', background='#00022e', foreground='gray64', font='Arial 10 normal')
        text_select_column.grid(row=0, column=0, padx=5, pady=5, sticky='we')

        self.combo_columns = ttk.Combobox(pane_select_column, textvariable=self.combo_get_operation_column)
        self.combo_columns.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        self.text_operation = tk.Label(pane_select_column, text='Pending... ', background='#00022e', foreground='gray64', font='Arial 10 normal')
        self.text_operation.grid(row=1, column=0, padx=5, pady=5, sticky='we')

        self.entry_show_operation = tk.Entry(pane_select_column, textvariable=self.show_operation, background='gray75')
        self.entry_show_operation.grid(row=1, column=1, padx=5, pady=5, sticky='we')

            # pane operation buttons
        pane_operation_buttons = tk.PanedWindow(lblf_column_opetration, background='#00022e')
        pane_operation_buttons.pack(expand=True)

        btn_sum = tk.Button(pane_operation_buttons, text='Summation',relief=FLAT, command=self.summation, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', font='Arial 10 bold')
        btn_sum.grid(row=0, column=0, padx=5, pady=5, sticky='we')
        Tooltip(btn_sum, 'Total')

        btn_max = tk.Button(pane_operation_buttons, text='Maximum', relief=FLAT, command=self.maximum, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', font='Arial 10 bold')
        btn_max.grid(row=0, column=1, padx=5, pady=5, sticky='we')
        Tooltip(btn_max, 'Maximum Value')

        btn_min = tk.Button(pane_operation_buttons, text='Minimum',relief=FLAT, command=self.minimum, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', font='Arial 10 bold')
        btn_min.grid(row=1, column=0, padx=5, pady=5, sticky='we')
        Tooltip(btn_min, 'Minimum value')

        btn_mean = tk.Button(pane_operation_buttons, text='Mean', relief=FLAT, command=self.mean, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', font='Arial 10 bold')
        btn_mean.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        Tooltip(btn_mean, 'Mean value')

        btn_standev = tk.Button(pane_operation_buttons, text='Standed \nDeviation', relief=FLAT, command=self.stdev, background='#00022e', activebackground='#00022e', foreground='cyan2', activeforeground='maroon1', font='Arial 10 bold')
        btn_standev.grid(row=2, column=0, padx=5, pady=5, sticky='we')
        Tooltip(btn_standev, 'Standed Deviation')

        #============ Footer Window ===========
        footer_pane = tk.PanedWindow(self.frame, background='#00022e')
        footer_pane.pack(fill=BOTH, expand=True)

        self.btn_quite = tk.Button(footer_pane, text='QUITE', command=self.quite, font='Arial 10 bold', background='#00022e', foreground='cyan2', relief=FLAT, activebackground='#00022e', activeforeground='maroon1')
        self.btn_quite.pack(side=RIGHT, padx=5, pady=5)
        Tooltip(self.btn_quite, 'Exit')
        
    # graph details buttons
    def plot(self):
        widget = self.frame
        height = widget.winfo_height()
        width = widget.winfo_width()
        print(f'Width : {width}\nHeight : {height}')

        name = self.graph_name.get()
        if name == '':
            msg.showerror(title='Error', message='Graph Name is Empty !!')
        else:
            x_axis = self.combo_get_x.get()
            y_axis = self.combo_get_y.get()
            if x_axis == '' or y_axis == '':
                msg.showerror(title='Error', message='Select Axis !!')
            else:
                table = self.show_table_name.cget('text')
                index = self.get_dataframe_index(table)
                data_frame = Back.get_data_frame(self, index)
                columns = Back.get_column_names(self, data_frame)
                name_list = [x_axis, y_axis]
                if set(name_list).issubset(set(columns)):
                    x_values = Back.get_column_values(self, data_frame, x_axis)
                    y_values = Back.get_column_values(self, data_frame, y_axis)

                    plt.plot(x_values, y_values)
                    plt.xlabel(f'{x_axis}')
                    plt.ylabel(f'{y_axis}')
                    plt.title(f'{name}')
                    plt.show()
                else:
                    msg.showerror(title='Error', message='Invalid Column name') 

    def summation(self):
        column = self.combo_columns.get()
        if column == '':
            msg.showerror(title='Error', message='Select a Column')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            cl_list = Back.get_column_names(self, data_frame)
            if column in cl_list:
                value_list = Back.get_column_values(self, data_frame, column)
                total = sum(value_list)
                self.update_operation_label(f'Summation of\n {column}')
                self.entry_show_operation.delete(0, END)
                self.entry_show_operation.insert(0, total)
            else:
                msg.showerror(title='Error', message=f'Invalid Column\n{column} is not in {table} !!')

    def maximum(self):
        column = self.combo_columns.get()
        if column == '':
            msg.showerror(title='Error', message='Select a Column')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            cl_list = Back.get_column_names(self, data_frame)
            if column in cl_list:
                value_list = Back.get_column_values(self, data_frame, column)
                max_val = max(value_list)
                self.update_operation_label(f'Maximum of\n {column}')
                self.entry_show_operation.delete(0, END)
                self.entry_show_operation.insert(0, max_val)
            else:
                msg.showerror(title='Error', message=f'Invalid Column\n{column} is not in {table} !!')

    def minimum(self):
        column = self.combo_columns.get()
        if column == '':
            msg.showerror(title='Error', message='Select a Column')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            cl_list = Back.get_column_names(self, data_frame)
            if column in cl_list:
                value_list = Back.get_column_values(self, data_frame, column)
                min_val = min(value_list)
                self.update_operation_label(f'Minimum of\n {column}')
                self.entry_show_operation.delete(0, END)
                self.entry_show_operation.insert(0, min_val)
            else:
                msg.showerror(title='Error', message=f'Invalid Column\n{column} is not in {table} !!')

    def mean(self):
        column = self.combo_columns.get()
        if column == '':
            msg.showerror(title='Error', message='Select a Column')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            cl_list = Back.get_column_names(self, data_frame)
            if column in cl_list:
                value_list = Back.get_column_values(self, data_frame, column)
                mean = statistics.mean(value_list)
                self.update_operation_label(f'Mean of\n {column}')
                self.entry_show_operation.delete(0, END)
                self.entry_show_operation.insert(0, mean)
            else:
                msg.showerror(title='Error', message=f'Invalid Column\n{column} is not in {table} !!')

    def stdev(self):
        column = self.combo_columns.get()
        if column == '':
            msg.showerror(title='Error', message='Select a Column')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            cl_list = Back.get_column_names(self, data_frame)
            if column in cl_list:
                valuelist = Back.get_column_values(self, data_frame, column)
                stndev =statistics.stdev(valuelist)
                self.update_operation_label(f'Standerd deviation\n{column}')
                self.entry_show_operation.delete(0, END)
                self.entry_show_operation.insert(0, stndev)
            else:
                msg.showerror(title='Error', message=f'invalied Column\n{column} is not in {table} !!')


    # column details buttons
    def add_value(self, value):
        if value == '':
            msg.showerror(title='Error', message='Value is Empty !!')
        else:
            try:
                value = int(value)
                self.column_value_list.append(value)
                self.insert_column_values_to_list_box(value)
                self.clear_entry(self.get_column_value)
            except:
                try:
                    value = float(value)
                    self.column_value_list.append(value)
                    self.insert_column_values_to_list_box(value)
                    self.clear_entry(self.get_column_value)
                except:
                    self.expression(value)
    
    def cancel(self):
        result = self.column_values_list_box.get(0, END)
        if (self.get_column_name.get() == '') and (self.get_column_value.get() == '') and (len(result) == 0) :
            pass
        else:
            result = msg.askyesno(title='Quction', message='Do you sure want to cancel ?')
            if result == True:
                entry_list = [self.get_column_name, self.get_column_value]
                for i in entry_list:
                    self.clear_entry(i)
                self.column_values_list_box.delete(0, END)
            else:
                pass

    def add_column(self, name):
        if len(self.data_frame_name_list) == 0:
            msg.showerror(title='Error', message='Create Table !!')
        else:
            if name == '':
                msg.showerror(title='Error', message='Empty Column Name !!')
            else:
                if name.isalpha():
                    if len(self.column_value_list) == 0:
                        msg.showerror(title='Error', message='Column Values are Empty !!')
                    else:
                        table = self.show_table_name.cget('text')
                        index = self.get_dataframe_index(table)
                        try:
                            data_frame = Back.get_data_frame(self, index)
                            column_names = Back.get_column_names(self, data_frame)
                            if len(column_names) == 0:
                                result = Back.add_column_data(self, data_frame, name, self.column_value_list)
                                if result == True:
                                    self.column_value_list.clear()
                                    self.clear_entry(self.get_column_name)
                                    self.clear_entry(self.get_column_value)
                                    self.clear_list_box(self.column_values_list_box)
                                    self.update_dropdown(data_frame)
                                    self.insert_column_names_to_list_box(name)
                                    self.disply_table(data_frame)
                                    name = ''
                                else:
                                    msg.showerror(title='Error', message='Something Went Wrong !!')
                            else:
                                if name in column_names:
                                    msg.showerror(title='Error', message='This Column Name is Alredy Exist !!')
                                else:
                                    number = Back.get_number_of_rows(self, data_frame)
                                    if number != len(self.column_value_list):
                                        msg.showerror(title='Error' ,message='Different Value Lenght')
                                    else:
                                        res = Back.add_column_data(self, data_frame, name, self.column_value_list)
                                        if res == True:
                                            self.column_value_list.clear()
                                            self.clear_entry(self.get_column_name)
                                            self.clear_entry(self.get_column_value)
                                            self.clear_list_box(self.column_values_list_box)
                                            self.update_dropdown(data_frame)
                                            self.insert_column_names_to_list_box(name)
                                            self.disply_table(data_frame)
                                            name = ''
                                        else:
                                            msg.showerror(title='Error', message='Something Went Wrong !!') 
                        except:
                            msg.showerror(title='Error', message='Something Went Wrong !!') 
                else:
                    msg.showerror(title='Error', message='Sorry !!\nColumn name Must be Alphebetical Word.')

    def update(self):
        value = self.column_value.get()
        if value == '':
            msg.showerror(title='Error', message='Please Select a Value !!')
        else:
            if re.findall('[a-zA-Z0-9]', value):
                result = msg.askyesno(title='Question', message=f'Do you want to update value : {value} ')
                if result == True:
                    if value.isalpha():
                        table = self.show_table_name.cget('text')
                        try:
                            index = self.get_dataframe_index(table)
                            data_frame = Back.get_data_frame(self, index)
                            column_names = Back.get_column_names(self, data_frame)
                            if value in column_names:
                                name_id = self.column_names_list_box.index(ANCHOR)
                                self.new_name = PopupWindow(self.root)
                                self.btn_update_column.config(state=DISABLED)
                                self.btn_quite.config(state=DISABLED)
                                self.header_button_close.config(state=DISABLED)
                                self.root.wait_window(self.new_name.top)
                                self.btn_update_column.config(state=NORMAL)
                                self.btn_quite.config(state=NORMAL)
                                self.header_button_close.config(state=NORMAL)
                                try:
                                    n_name = self.new_name.new_value
                                    if n_name == '':
                                        pass
                                    else:
                                        if n_name in column_names:
                                            msg.showerror(title='Error', message='This Name is Already Exist !!')
                                        else:
                                            if n_name.isalpha():
                                                column_names.pop(name_id)
                                                column_names.insert(name_id, n_name)
                                                res = Back.rename_column(self, data_frame, column_names)
                                                if res == True:
                                                    self.clear_entry(self.get_column_value)
                                                    self.column_names_list_box.delete(name_id)
                                                    self.column_names_list_box.insert(name_id, f'{n_name}')
                                                    self.update_dropdown(data_frame)
                                                    self.disply_table(data_frame)
                                                    self.combo_entry_clear()
                                                else:
                                                    msg.showerror(title='Error', message='Something Went Wrong !!')
                                            else:
                                                msg.showerror(title='Error', message='Sory !!\nEnter Only Alphebital Word.')
                                except:
                                    pass
                            else:
                                msg.showerror(title='Error', message=f'Invalid Column Name \n{value} not in {table} table !!')
                        except:
                                msg.showerror(title='Error', message='Empty Tables !!')
                    else:
                        pass
                        current_values = list(self.column_values_list_box.get(0, END))
                        if len(current_values) == 0:
                            msg.showerror(title='Error', message='Empty Values !!')
                        else:
                            if int(value) in current_values:
                                val_id = self.column_values_list_box.index(ANCHOR)
                                self.value = PopupWindow(self.root)
                                self.btn_update_column.config(state=DISABLED)
                                self.btn_quite.config(state=DISABLED)
                                self.header_button_close.config(state=DISABLED)
                                self.root.wait_window(self.value.top)
                                self.btn_update_column.config(state=NORMAL)
                                self.btn_quite.config(state=NORMAL)
                                self.header_button_close.config(state=NORMAL)
                                try:
                                    n_val = self.value.new_value
                                    if re.findall('[0-9]', n_val):
                                        self.clear_entry(self.get_column_value)
                                        self.column_values_list_box.delete(val_id)
                                        self.column_value_list.pop(val_id)
                                        try:
                                            val = int(n_val)
                                            self.column_value_list.insert(val_id, int(val))
                                            self.column_values_list_box.insert(val_id, val)
                                        except:
                                            val = float(n_val)
                                            self.column_value_list.insert(val_id, float(val))
                                            self.column_values_list_box.insert(val_id, val)
                                    else:
                                        msg.showerror(title='Error', message='Invalid Input !!')
                                except:
                                    pass
                            else:
                                msg.showerror(title='Error', message='This Value is not in You Entered Value List !!')
                else:
                    pass
            else:
                msg.showerror(title='Error', message='Invalied Input !!')

    def drop_table(self):
        if len(self.dataframe_key_value_dict) == 0:
            msg.showinfo(title='Information', message='Empty Tables !!')
        else:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            result = msg.askyesno(title='Qestion', message=f'Do you want to delete table {table}')
            if result == True:
                try:
                    data_frame = Back.get_data_frame(self, index)
                    result = Back.delete_dataframe(self, data_frame,index)
                    if result == True:
                        del self.dataframe_key_value_dict[f'{table}']
                        self.data_frame_name_list.remove(f'{table}')
                        new_length = len(self.data_frame_name_list)
                        new_id = new_length - 1
                        if new_id < 0:
                            self.set_table_name('No Tables')
                            self.destroye_frame_widgets()
                            self.controll_button_next.config(state=DISABLED)
                            self.controll_button_prev.config(state=DISABLED)
                        else:
                            name = self.data_frame_name_list[new_id]
                            self.set_table_name(name)
                            self.destroye_frame_widgets()
                            new_index = self.get_dataframe_index(name)
                            new_df = Back.get_data_frame(self, new_index)
                            self.disply_table(new_df)
                            name_list = Back.get_column_names(self, new_df)
                            for i in name_list:
                                self.insert_column_names_to_list_box(i)
                            self.update_dropdown(new_df)
                    else:
                        msg.showerror(title='Error', message='Can\'t delete table')
                except:
                    msg.showerror(title='Error', message='Something Went Wrong !!')
            else:
                pass

    def drop_column(self):
        cl_name = self.column_names_list_box.get(ANCHOR)
        val = self.column_names_list_box.curselection()
        if len(val) == 0:
            msg.showerror(title='Error', message='Please Select a row in Column Names')
        else:
            result = msg.askyesno(title='Qestion', message=f'Do You want to delete {cl_name} Column ?')
            if result == True:
                table = self.show_table_name.cget('text')
                index = self.get_dataframe_index(table)
                try:
                    dataframe = Back.get_data_frame(self, index) 
                    ress = Back.drop_dataframe_column(self, dataframe, cl_name)
                    if ress == True:
                        self.column_names_list_box.delete(ANCHOR)
                        self.clear_entry(self.get_column_value)
                        self.destroye_frame_widgets()
                        self.disply_table(dataframe)
                        self.update_dropdown(dataframe)
                        number = Back.get_column_names(self, dataframe)
                        if len(number) == 0:
                            Back.clear_dataframe_index(self, dataframe)
                        else:
                            pass
                    else:
                        msg.showerror(title='Error', message=f'Can\'t delete {cl_name} column')
                except:
                    msg.showerror(title='Error',message='Something Went Wrong !!')
            else:
                pass

    def delete(self):
        try:
            item = self.column_values_list_box.get(ACTIVE)
            val = self.column_values_list_box.curselection()
            if len(val) == 0:
                msg.showerror(title='Error', message='Pleae Select a row in Column Values')
            else:
                result = msg.askyesno(title='Quetion', message=f'Do you sure want to delete {item} ?')
                if result == True:
                    self.column_value_list.pop(val[0])
                    self.column_values_list_box.delete(ANCHOR)
                    self.clear_entry(self.get_column_value)
        except:
            msg.showerror(title='Error', message='Something Went Wrong !!')


    # stystem buttons
    def create_table(self, name, data_frame_list):
        if name == '':
            msg.showerror(title='Error', message='Table Name is Empty !!')
        else:
            if len(data_frame_list) == 0:
                result = Back.create_dataframe(self, name)
                if result == False:
                    msg.showerror('Can\'t Create a Table !!')
                else:
                    data_frame_list.append(name)
                    self.dataframe_key_value_dict[f'{name}'] = data_frame_list.index(f'{name}')
                    self.clear_entry(self.get_table_name)
                    self.set_table_name(name)
                    self.hide_create_table()
                    table = self.show_table_name.cget('text')
                    index = self.get_dataframe_index(table)
                    dataframe = Back.get_data_frame(self, index) 
                    self.update_dropdown(dataframe)
                    self.clear_list_box(self.column_names_list_box)
                    self.destroye_frame_widgets()
                    self.combo_entry_clear()
            else:
                if name in data_frame_list:
                    msg.showerror(title='Error', message='This Table is Already Exist !!')
                else:
                    result = Back.create_dataframe(self, name)
                    if result == False:
                        msg.showerror('Can\'t Create a Table !!')
                    else:
                        data_frame_list.append(name)
                        self.dataframe_key_value_dict[f'{name}'] = data_frame_list.index(f'{name}')
                        self.clear_entry(self.get_table_name)
                        self.set_table_name(name)
                        self.hide_create_table()
                        table = self.show_table_name.cget('text')
                        index = self.get_dataframe_index(table)
                        dataframe = Back.get_data_frame(self, index) 
                        self.update_dropdown(dataframe)
                        self.clear_list_box(self.column_names_list_box)
                        self.destroye_frame_widgets()
                        self.combo_entry_clear()
                        self.controll_button_next.config(state=NORMAL)
                        self.controll_button_prev.config(state=NORMAL)

    def quite(self):
            result = msg.askyesno(title='Quiction', message='Do You Want to Exit ?')
            if result == True:
                root.destroy()
            else:
                pass

    def back(self):
        name = self.show_table_name.cget('text')
        index = self.data_frame_name_list.index(f'{name}')
        value = index - 1
        entry_list = [self.get_column_name, self.get_column_value, self.enty_graph_title, self.entry_show_operation]
        listbox_list = [self.column_values_list_box, self.column_names_list_box]
        if value >= 0 :
            new_name = self.data_frame_name_list[value]
            self.set_table_name(new_name)
            for i in entry_list:
                self.clear_entry(i)
            for i in listbox_list:
                self.clear_list_box(i)
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            self.update_dropdown(data_frame)
            cl_names = Back.get_column_names(self, data_frame)
            for i in cl_names:
                self.insert_column_names_to_list_box(i)
            self.destroye_frame_widgets()
            self.disply_table(data_frame)
            self.update_operation_label('Pending...')
            self.combo_entry_clear()
            self.column_value_list.clear()
        else:
            length = len(self.data_frame_name_list)
            new_name = self.data_frame_name_list[length - 1]
            self.set_table_name(new_name)
            for i in entry_list:
                self.clear_entry(i)
            for i in listbox_list:
                self.clear_list_box(i)
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            self.update_dropdown(data_frame)
            cl_names = Back.get_column_names(self, data_frame)
            for i in cl_names:
                self.insert_column_names_to_list_box(i)
            self.destroye_frame_widgets()
            self.disply_table(data_frame)
            self.update_operation_label('Pending...')
            self.combo_entry_clear()
            self.column_value_list.clear()

    def next(self):
        name = self.show_table_name.cget('text')
        index = self.data_frame_name_list.index(f'{name}')
        length = len(self.data_frame_name_list)
        value = index + 1
        entry_list = [self.get_column_name, self.get_column_value, self.enty_graph_title, self.entry_show_operation]
        listbox_list = [self.column_values_list_box, self.column_names_list_box]
        if value == length:
            new_name = self.data_frame_name_list[0]
            self.set_table_name(new_name)
            for i in entry_list:
                self.clear_entry(i)
            for i in listbox_list:
                self.clear_list_box(i)
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            self.update_dropdown(data_frame)
            cl_names = Back.get_column_names(self, data_frame)
            for i in cl_names:
                self.insert_column_names_to_list_box(i)
            self.destroye_frame_widgets()
            self.disply_table(data_frame)
            self.update_operation_label('Pending...')
            self.combo_entry_clear()
            self.column_value_list.clear()
        else:
            new_name = self.data_frame_name_list[value]
            self.set_table_name(new_name)
            for i in entry_list:
                self.clear_entry(i)
            for i in listbox_list:
                self.clear_list_box(i)
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            data_frame = Back.get_data_frame(self, index)
            self.update_dropdown(data_frame)
            cl_names = Back.get_column_names(self, data_frame)
            for i in cl_names:
                self.insert_column_names_to_list_box(i)
            self.destroye_frame_widgets()
            self.disply_table(data_frame)
            self.update_operation_label('Pending...')
            self.combo_entry_clear()
            self.column_value_list.clear()

    def minimize(self):
        root.overrideredirect(0)
        root.iconify()


    # other methods
    def clear_entry(self, entry):
        entry.delete(0, END)
        entry.insert(0, '')

    def set_table_name(self, name):
        self.text_table_name.config(text=f'{name}')
        self.show_table_name.config(text=f'{name}')

    def hide_create_table(self):
        self.input_table_name.pack_forget()
        self.get_table_name.pack_forget()
        self.btn_create_table.pack_forget()
        self.btn_create_new_table.pack(padx=5, pady=5)

    def show_create_table(self):
        self.input_table_name.pack(side=LEFT, padx=5, pady=5)
        self.get_table_name.pack(side=LEFT, padx=5, pady=5)
        self.btn_create_table.pack(side=LEFT, padx=5, pady=5)
        self.btn_create_new_table.pack_forget()
 
    def insert_column_values_to_list_box(self, value):
        self.column_values_list_box.insert(END, value) 

    def insert_column_names_to_list_box(self, name):
        self.column_names_list_box.insert(END, name)

    def get_dataframe_index(self, name):
        val = self.dataframe_key_value_dict[f'{name}']
        return val

    def clear_list_box(self, list_box):
        list_box.delete(0, END)

    def update_dropdown(self, dataframe):
        cl_names = Back.get_column_names(self, dataframe)
        self.combo_x_axis['values'] = tuple(cl_names) 
        self.combo_y_axis['values'] = tuple(cl_names)
        self.combo_columns['values'] = tuple(cl_names)

    def update_operation_label(self, text):
        self.text_operation.config(text=text)

    def disply_table(self, dataframe):
        cl_names = Back.get_column_names(self, dataframe)
        if len(cl_names) == 0:
            pass
        else:
            for index, name in enumerate(cl_names):
                btn = tk.Button(self.table_frame, text=f'{name}', background='#00022e', relief=FLAT, foreground='cyan2', font='Arial 10 bold')
                btn.grid(row=0, column=index, padx=5, pady=5, sticky='we')
                value_list = Back.get_column_values(self, dataframe, name)
                for val_index, value in enumerate(value_list):
                    lbl = tk.Label(self.table_frame, text=f'{value}', font='Arial 10 normal', foreground='Black')
                    lbl.grid(row=val_index + 2, column=index, padx=5, pady=5, sticky='we')

    def destroye_frame_widgets(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def combo_entry_clear(self):
        self.combo_columns.set('')
        self.combo_x_axis.set('')
        self.combo_y_axis.set('')


    # event handeling methods
    def click_column_values(self, event):
        value = self.column_values_list_box.get(ANCHOR)
        self.get_column_value.delete(0, 'end')
        self.get_column_value.insert(0, value)

    def click_column_name(self, event):
        name = self.column_names_list_box.get(ANCHOR)
        pos = self.get_column_value.index(INSERT)
        self.get_column_value.insert(pos, name)

    def table_button(self):
        print('Button Clicked !!')

    def get_pos(self, event):
        self.x = event.x
        self.y = event.y

    def relese(self, event):
        self.x = None
        self.y = None

    def move_window(self, event):
        delx = event.x - self.x
        dely = event.y - self.y
        xw = root.winfo_x() + delx
        yw = root.winfo_y() + dely
        root.geometry('+{0}+{1}'.format(xw,yw))

    def show_screen(self, event):
        root.deiconify()
        root.overrideredirect(1)
        #root.after(10, lambda: set_appwindow(root))

    def screen_apear(self, event):
        root.overrideredirect(1)

    # Fill Column Using Expression
    def expression(self, expression):
        if len(self.data_frame_name_list) != 0:
            table = self.show_table_name.cget('text')
            index = self.get_dataframe_index(table)
            n_list = re.findall('[a-zA-Z]+', expression)
            try:
                dataframe = Back.get_data_frame(self, index)
                cl_names = Back.get_column_names(self, dataframe)
                if len(cl_names) != 0:
                    if set(n_list).issubset(set(cl_names)):
                        value_dict = self.values_dictionaty(dataframe, n_list)
                        expression_list = self.expressions(value_dict, expression, dataframe)
                        final_values = self.calculate_final_values(expression_list)
                        self.column_value_list = final_values
                        for i in final_values:
                            self.insert_column_values_to_list_box(i)
                        self.clear_entry(self.get_column_value)
                    else:
                        msg.showerror(title='Error', message='Invalied Column Name/s')
                else:
                    msg.showinfo(title='Information', message='Cant do that\nThere are no column in your table')
            except:
                msg.showerror(title='Error', message='Can\'t Calculate Final Values !!')
        else:
            msg.showerror(title='Error', message='Empty tables !!')

    def values_dictionaty(self, dataframe, cl_name_list):
        value_dict = {}
        try:
            for value in cl_name_list:
                val_list = Back.get_column_values(self, dataframe, value)
                value_dict[value] = val_list
            return value_dict
        except:
            msg.showerror(title='Error', message='Something Went Wrong !!')

    def expressions(self, value_dict, exp, dataframe):
        try:
            row_count = Back.get_number_of_rows(self, dataframe)
            explixt = []
            key_list = list(value_dict.keys())
            new = ''
            for i in range(0, row_count):
                test = exp
                for k in key_list:
                    new = test.replace(str(k), str(value_dict[f'{k}'][i]))
                    test = new
                explixt.append(new)
                test = '' 
            return explixt
        except:
            msg.showerror(title='Error', message='Somethin Went Wrong !!')

    def calculate_final_values(self, exp_list):
        try:
            solve_list = []
            for i in exp_list:
                val = eval(i)
                if isinstance(val, int):
                    solve_list.append(val)
                else:
                    val = round(val, 4)
                    solve_list.append(val)
            return solve_list
        except:
            msg.showerror(title='Error', message='Invalid Expression !!')
       

if __name__ == '__main__':
    root = tix.Tk()
    Main(root)
    root.maxsize(width=998, height=546)
    root.geometry('998x536+250+150')
    
    #root.resizable(0,0)
    #root.attributes('-alpha', 0.5) # to transparent background
    
    image = PhotoImage(file='logo.png')
    root.iconphoto(True, image)

    root.overrideredirect(1)

    root.mainloop()
