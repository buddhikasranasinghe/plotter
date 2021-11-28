# front end
import re
import tkinter as tk
from tkinter.constants import ACTIVE, ALL, ANCHOR, BOTH, BOTTOM, COMMAND, END, HORIZONTAL, INSERT, LEFT, N, NW, RIGHT, TOP, VERTICAL, W, X, Y, YES
from tkinter.ttk import Combobox
import numpy as np
from numpy.core.einsumfunc import _update_other_results
from numpy.core.overrides import set_module

from numpy.lib.function_base import delete, select
from numpy.lib.scimath import power
from design import *
from error_massage import *
from backend import *
import pandas as pd
import matplotlib.pyplot as plt
import statistics

class Plot_Graph():
    
    def __init__(self, root):

        self.root = root
        self.df = pd.DataFrame()

        self.column_name = tk.StringVar()
        self.column_value = tk.StringVar()
        self.column_value_list = []
        self.column_name_list = []

        self.main_frame = frame(self.root)
        self.main_frame.pack()

        self.pane_one = pane(self.main_frame)
        self.pane_one.grid(row=0, column=0)

        main_lbl = label(self.pane_one, 'PLOT YOUR OWN GRAPH')
        main_lbl.grid(row=0, column=0, padx=5, pady=5)

        #======================= COLUMN DETAILS WINDOW ========================
        self.pane_two = pane(self.main_frame)
        self.pane_two.grid(row=1, column=0)

        self.frame_column_details = lblframe(self.pane_two, 'Column Details')
        self.frame_column_details.pack(side='left', padx=5, pady=5, expand=True, fill=BOTH)
        
        pane_column_details = pane(self.frame_column_details)
        pane_column_details.grid(row=1, column=0)

        lbl_clumn_name = label(pane_column_details, 'Column Name')
        lbl_clumn_name.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.column_name_entry = entry(pane_column_details, self.column_name)
        self.column_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

        lbl_column_values = label(pane_column_details, 'Column Values')
        lbl_column_values.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.column_value_entry = entry(pane_column_details, self.column_value)
        self.column_value_entry.grid(row=1, column=1, padx=5, pady=5, sticky=W)

        btn_add = button(self.frame_column_details, 'ADD', btn_cmnd= lambda :self.add_value(self.column_value.get(), self.column_value_list))
        btn_add.grid(row=4, column=0, padx=5, pady=5)

            #-------------- column value buttons list ------------------
        self.btn_column_val_pane = pane(self.frame_column_details)
        self.btn_column_val_pane.grid(row=5, column=0)

        pane_one = pane(self.btn_column_val_pane)
        pane_one.grid(row=1, column=0)

        pane_two = pane(self.btn_column_val_pane)
        pane_two.grid(row=1, column=1)

        label_text = label(self.btn_column_val_pane, lbl_text='Column Values ')
        label_text.grid(row=0, column=0, padx=5, pady=5)

        label_column_names = label(self.btn_column_val_pane, lbl_text='Column Names ')
        label_column_names.grid(row=0, column=1, padx=5, pady=5)

        self.btn_list = list_box(pane_one)
        self.btn_list.bind('<<ListboxSelect>>',self.select_value)
        self.btn_list.pack(side=LEFT)

        val_scroll = scroll_bar(pane_one)
        val_scroll.pack(side=RIGHT, fill=BOTH)
        self.btn_list.config(yscrollcommand=val_scroll.set)
        val_scroll.config(command=self.btn_list.yview)

        self.show_column_names = list_box(pane_two)
        self.show_column_names.bind('<<ListboxSelect>>',self.select_column)
        self.show_column_names.pack(side=LEFT)

        name_scroll = scroll_bar(pane_two)
        name_scroll.pack(side=RIGHT, fill=BOTH)
        self.show_column_names.config(yscrollcommand=name_scroll.set)
        name_scroll.config(command=self.show_column_names.yview)

            #-------------- button panel ---------------------- 
        self.pane_three = pane(self.frame_column_details)
        self.pane_three.grid(row=6, column=0)

        btn_cancel = button(self.pane_three, btn_text='Cancel', btn_cmnd=self.cancel)
        btn_cancel.grid(row=0, column=0, padx=5, pady=5, sticky='we')

        btn_add_column = button(self.pane_three, btn_text='Add Column', btn_cmnd= lambda: self.add_column(self.column_name.get(), self.column_value_list, self.df, self.btn_list, self.column_name_list))
        btn_add_column.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        btn_drop = button(self.pane_three, btn_text='New Table', btn_cmnd=lambda : self.create_new_data_frame(self.df))
        btn_drop.grid(row=0, column=2, padx=5, pady=5, sticky='we')

        btn_update = button(self.pane_three, btn_text='Update', btn_cmnd=lambda:self.update(self.column_value_entry.get()))
        btn_update.grid(row=1, column=0, padx=5, pady=5, sticky='we')

        btn_delete = button(self.pane_three, btn_text='Delete', btn_cmnd= lambda:self.delete(self.btn_list, self.column_value_list))
        btn_delete.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        btn_save = button(self.pane_three, btn_text='Save Table', btn_cmnd=self.new_button)
        btn_save.grid(row=1, column=2, padx=5, pady=5, sticky='we')

        #================================ FOOTER WINDOW ===========================
        self.pane_footer = pane(self.main_frame)
        self.pane_footer.grid(row=2, column=0, sticky='e')

        btn_quite = button(self.pane_footer, btn_text='QUITE', btn_cmnd=self.quite)
        btn_quite.pack(side=LEFT, fill=X, padx=5, pady=5)

        #============================= Show Table =========================
        self.frame_show_table = lblframe(self.pane_two, 'Table Details')
        self.frame_show_table.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

        self.pane_table_name = pane(self.frame_show_table)
        self.pane_table_name.pack(side=TOP)

        text_lbl = label(self.pane_table_name, '')
        text_lbl.grid(row=0, column=0)

        self.table_pane = pane(self.frame_show_table)
        self.table_pane.pack(side=TOP)

        self.pane_scroll = lblframe(self.table_pane, '')
        self.pane_scroll.pack(fill=BOTH, expand=YES)

        self.canvas = tk.Canvas(self.pane_scroll)
        self.canvas.pack(side=LEFT, fill=BOTH)

        self.h_scroll = ttk.Scrollbar(self.pane_scroll, orient=VERTICAL, command=self.canvas.yview)
        self.h_scroll.pack(side=RIGHT, fill=Y)

        self.pane_table = ttk.Frame(self.canvas)
        self.canvas.configure(yscrollcommand=self.h_scroll.set)
        self.pane_table.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.create_window((0,0), window=self.pane_table, anchor='nw')
        
        pane_x_sroll = pane(self.frame_show_table)
        pane_x_sroll.pack(fill=X)

        v_scroll = ttk.Scrollbar(pane_x_sroll, orient=HORIZONTAL, command=self.canvas.xview)
        v_scroll.pack(side=TOP, fill=X)
        self.canvas.configure(xscrollcommand=v_scroll.set)
        self.pane_table.bind('<Configure>', lambda e:self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.btn_go_to_plot = button(self.frame_show_table, btn_text='Go to plot', btn_cmnd=self.go_to_plot)
        self.btn_go_to_plot.pack(side=BOTTOM, padx=5, pady=5)

        self.btn_reloard = button(self.frame_show_table, btn_text='Reload', btn_cmnd=self.reload)

    def add_value(self, value, val_list):
        result = Backend.check_input_value(self, value, val_list, self.btn_list)
        if result == True:
            self.column_value_entry.delete(0, 'end')
            self.column_value_entry.insert(0, '')
        elif result == False:
            self.calculation(self.column_value_entry.get())
        else:
            pass

    def cancel(self):
        msg = 'Do you want to cancel ?'
        result = Backend.cancel(self,msg)
        if result == True:
            self.column_name_entry.delete(0, 'end')
            self.column_name_entry.insert(0, '')
            self.column_value_entry.delete(0, 'end')
            self.column_value_entry.insert(0, '')
            self.btn_list.delete(0,'end')

    def add_column(self, name, val_list, data_frame, show_list, clm_name_list):
        result = Backend.add_column(self, name, val_list, data_frame, show_list, clm_name_list)
        if result == True:
            self.show_column(name)
            self.column_name_entry.delete(0, 'end')
            self.column_name_entry.insert(0, '')
            self.column_value_entry.delete(0, 'end')

    def show_column(self, name):
        total_column = len(self.df.columns)
        total_rows = len(self.df)
        btn = button(self.pane_table, btn_text=name, btn_cmnd=lambda:self.column_btn(name))
        btn.grid(row=1, column=(total_column+1), padx=5, pady=5, sticky='we')
        values_list = self.df[f'{name}'].to_list() # get column values of given column in data frame
        for  index, value in enumerate(values_list):
            value_label = label(self.pane_table, lbl_text=f'{value}')
            value_label.grid(row=(index+2), column=(total_column+1), padx=5, pady=5, sticky='we')

    def update(self, item):
        if item == '':
            error_msg('Select a value')
        else:
            popup = tk.Toplevel()
            new_value = tk.StringVar()
            text_lbl = label(popup, lbl_text='Enter New Value')
            text_lbl.grid(row=0, column=0)
            new_value_entry = entry(popup, text_var=new_value)
            new_value_entry.grid(row=0, column=1)
            btn_ok = tk.Button(popup, text='Ok')
            btn_ok.grid(row=2, column=0)
            btn_ok = tk.Button(popup, text='Cansel')
            btn_ok.grid(row=2, column=1)

    def quite(self):
        result = yesno('Doy you want to Quite !!')
        if result == True:
            root.destroy()

    def delete(self, show_list, val_list):
        try:
            item = show_list.get(ACTIVE)
            val = show_list.curselection()
            if len(val) == 0:
                information_msg('Pleae Select a row')
            else:
                result = yesno(f'Are you sure want to delete {item} ?')
                if result == True:
                    val_list.pop(val[0])
                    show_list.delete(ANCHOR)
                    self.column_value_entry.delete(0, 'end')
        except:
            information_msg('Something Went Wrong !!')

    def go_to_plot(self):
        column_name = self.df.columns.tolist()
        if not column_name:
            error_msg('Empty Columns')
        else:
            self.show_frame()

    def show_frame(self):
        self.btn_go_to_plot.destroy()
        self.btn_reloard.pack(side=BOTTOM, padx=5, pady=5)

        self.frame_plot_graph = lblframe(self.pane_two,'Graph Details')
        self.frame_plot_graph.pack(side=RIGHT, fill=BOTH, padx=5, pady=5)

        self.pane_graph_details = pane(self.frame_plot_graph)
        self.pane_graph_details.pack()

        lbl_select_x_axis = label(self.pane_graph_details, 'Select X-Axis :')
        lbl_select_x_axis.grid(row=0, column=0, padx=5, pady=5)

        var_x = tk.StringVar()
        var_y = tk.StringVar()
        self.data_list_one = self.df.columns.tolist()
        self.data_list_two = self.df.columns.tolist()
        column_name_list_x = drop_down(self.pane_graph_details, var_x, self.data_list_one)
        column_name_list_x.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        lbl_select_y_axis = label(self.pane_graph_details, 'Select Y-Axis :')
        lbl_select_y_axis.grid(row=1, column=0, padx=5, pady=5)

        column_name_list_y = drop_down(self.pane_graph_details, var_y, self.data_list_two)
        column_name_list_y.grid(row=1, column=1, padx=5, pady=5, sticky='we')

        lbl_select_x_axis_name = label(self.pane_graph_details, 'X-Axis Name :')
        lbl_select_x_axis_name.grid(row=2, column=0, padx=5, pady=5)

        self.var_name_x = tk.StringVar()
        self.var_name_y = tk.StringVar()
        self.graph_name = tk.StringVar()
        entry_x_name = entry(self.pane_graph_details, self.var_name_x)
        entry_x_name.grid(row=2, column=1, padx=5, pady=5)

        lbl_select_y_axis_name = label(self.pane_graph_details, 'Y-Axis Name :')
        lbl_select_y_axis_name.grid(row=3, column=0, padx=5, pady=5)

        entry_y_name = entry(self.pane_graph_details, self.var_name_y)
        entry_y_name.grid(row=3, column=1, padx=5, pady=5)

        lbl_graph_name = label(self.pane_graph_details, 'Graph title ')
        lbl_graph_name.grid(row=4, column=0, padx=5, pady=5)

        entry_graph_name = entry(self.pane_graph_details, self.graph_name)
        entry_graph_name.grid(row=4, column=1, padx=5, pady=5)

        btn_plot = button(self.pane_graph_details, btn_text='Plot', btn_cmnd=lambda:self.plot(self.var_name_x.get(), self.var_name_y.get(), var_x.get(), var_y.get(), self.graph_name.get()))
        btn_plot.grid(row=5, column=0, padx=5, pady=5)

        self.pane_column_operations = pane(self.frame_plot_graph)
        self.pane_column_operations.pack(fill=BOTH)

        self.lbl_column_operations = lblframe(self.pane_column_operations, frame_text='')
        self.lbl_column_operations.pack(fill=BOTH)

        self.pane_select_column = pane(self.lbl_column_operations)
        self.pane_select_column.pack(fill=BOTH, expand=True)
        select_column_label = label(self.pane_select_column, lbl_text='Select a Column')
        select_column_label.grid(row=0, column=0)

        var_names = tk.StringVar()
        data = self.get_column_names(self.df)
        column_name_dd = drop_down(self.pane_select_column, var_names, data)
        column_name_dd.grid(row=0, column=1, sticky='we')

        self.operation_label = tk.Label(self.pane_select_column, text='Not Yet ', width=20)
        self.operation_label.grid(row=1, column=0)

        self.show_val = tk.StringVar()
        self.entry_show = tk.Entry(self.pane_select_column, textvariable=self.show_val, width=10)
        self.entry_show.grid(row=1, column=1, sticky='we')

        self.column_operation_buttons = pane(self.lbl_column_operations)
        self.column_operation_buttons.pack()

        btn_sum = button(self.column_operation_buttons, btn_text='Summation', btn_cmnd= lambda: self.column_operations(var_names.get(), number=1, dataframe=self.df))
        btn_sum.grid(row=0, column=0, padx=5, pady=5, sticky='we')

        btn_max = button(self.column_operation_buttons, btn_text='Max', btn_cmnd= lambda: self.column_operations(var_names.get(), number=2, dataframe=self.df))
        btn_max.grid(row=0, column=1, padx=5, pady=5, sticky='we')

        btn_min = button(self.column_operation_buttons, btn_text='Min', btn_cmnd= lambda: self.column_operations(var_names.get(), number=3, dataframe=self.df))
        btn_min.grid(row=1, column=0, padx=5, pady=5, sticky='we')

        btn_mean = button(self.column_operation_buttons, btn_text='Mean', btn_cmnd= lambda: self.column_operations(var_names.get(), number=4, dataframe=self.df))
        btn_mean.grid(row=1, column=1, padx=5, pady=5, sticky='we')
        
    def plot(self, name_x, name_y, val_x, val_y, g_name):
        if name_x == '' or name_y == '':
            error_msg('Name is Empty ')
        else:
            if val_x == '' or val_y == '':
                error_msg('Select Axis')
            else:
                val_list_x = self.df[f'{val_x}'].tolist()
                val_list_y = self.df[f'{val_y}'].tolist()
                plt.plot(val_list_x, val_list_y)
                plt.xlabel(f'{name_x}') 
                plt.ylabel(f'{name_y}')  
                plt.title(g_name)  
                plt.show()

    def calculation(self, expression):
        clmn_names = self.df.columns.tolist()
        n_list = re.findall('[a-zA-Z]+', expression)
        if set(n_list).issubset(set(clmn_names)):
            val_dict = self.get_column_values(n_list)
            exp_list = self.explist(val_dict, expression)
            final_values = self.cal_final_values(exp_list)
            self.column_value_list = final_values
            try:
                for i in final_values:        
                    self.btn_list.insert('end', i)
            except:
                pass
        else:
            error_msg('Invalied Expression !! ')
    
    def get_column_values(self, cl_name_list):
        val_dict = {}
        for value in cl_name_list:
            val_list = self.df[f'{value}'].tolist()
            val_dict[value] = val_list
        return val_dict

    def explist(self, dict, exp):
        index = self.df.index
        number = len(index)
        explixt = []
        key_list = list(dict.keys())
        new = ''
        for i in range(0, number):
            test = exp
            for k in key_list:
                new = test.replace(str(k), str(dict[f'{k}'][i]))
                test = new
            explixt.append(new)
            test = '' 
        return explixt       

    def cal_final_values(self, exp_list):
        try:
            new_list = []
            for i in exp_list:
                val = eval(i)
                if isinstance(val, int):
                    new_list.append(val)
                else:
                    val = round(val, 4)
                    new_list.append(val)
            return new_list
        except:
            error_msg('Invalid Input !!')

    def select_value(self, event):
        value = self.btn_list.get(ANCHOR)
        self.column_value_entry.delete(0, 'end')
        self.column_value_entry.insert(0, value)

    def select_column(self, event):
        name = self.show_column_names.get(ANCHOR)
        pos = self.column_value_entry.index(INSERT)
        self.column_value_entry.insert(pos,f'{name}')

    def reload(self):
        self.frame_plot_graph.pack_forget()
        self.show_frame()

    def new_button(self):
        print('We are new cammers ')

    def column_operations(self, name, number, dataframe):
        if name == '':
            error_msg('Please Select a Column')
        else:
            val_list = Backend.get_value_from_dataframe(self, name=name, dataframe=dataframe)
            if val_list == False:
                error_msg('Invallied Column Name')
            else:
                if number == 1:
                    summation = sum(val_list)
                    self.entry_show.delete(0, 'end')
                    self.entry_show.insert(0, summation)
                    self.operation_label.config(text=f'Summation of \n{name} ')
                elif number == 2:
                    max_val = max(val_list)
                    self.entry_show.delete(0, 'end')
                    self.entry_show.insert(0, max_val)
                    self.operation_label.config(text=f'Max value of \n{name} ')
                elif number == 3:
                    min_val = min(val_list)
                    self.entry_show.delete(0, 'end')
                    self.entry_show.insert(0, min_val)
                    self.operation_label.config(text=f'Min value of \n{name} ')
                elif number == 4:
                    ave = statistics.mean(val_list)
                    self.entry_show.delete(0, 'end')
                    self.entry_show.insert(0, round(ave, 4))
                    self.operation_label.config(text=f'Mean value of \n{name} ')
                else:
                    error_msg('Something Went Wrong !!')
    
    def get_column_names(self, dataframe):
        name_list = Backend.get_column_names(self, dataframe)
        if name_list == False:
            error_msg('Something Went Wrong ' )
        else:
            return name_list

    def column_btn(self, name):
        result = yesno(f'Do You Want to Delete \'{name}\' Column ?')
        if result == True:
            print('Deleting.........')
        else:
            pass

    def create_new_data_frame(self, dataframe):
        result = yesno('Do You Want to Create a New Table !!')
        if result == True:
            Backend.Create_new_table(self, dataframe=dataframe)
        else:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    Plot_Graph(root)
    root.title('Ploter')
    root.maxsize(width=970, height=475)
    root.geometry('970x475')
    root.minsize(width=970, height=475)
    root.mainloop()