# back end
from tkinter.constants import TOP
from design import button, label, top_level
from error_massage import *
import pandas as pd
import re

class Backend():

    def __init__(self):
        super().__init__()

    def check_input_value(self,value, val_list, show_list):
        if value == '':
            error_msg('Empty Value')
        else:
            try:
                val = int(value)
                val_list.append(val)
                #print(val_list)
                show_list.insert('end', val)
                return True
            except:
                try:
                    val = float(value)
                    val_list.append(val)
                    #print(val_list)
                    show_list.insert('end', val)
                    return True
                except:
                    return False
                    #error_msg('Something Went Wrong !!')

    def add_column(self, name, val_list, data_frame, show_data_list, clm_name_list):
        if name == '':
            error_msg('Name is Empty !!')
        else:
            if name.isalpha():
                clmn_names = data_frame.columns
                if name in clmn_names:
                    error_msg('You Entered Column Aleady exist !!')
                else:
                    #pass
                    if not val_list:
                        error_msg('Empty Column Values !!')
                    else:
                        tot_column = len(data_frame.columns)
                        tot_rows = len(data_frame)
                        count = len(val_list)
                        if tot_column == 0:
                            data_frame[f'{name}'] = val_list
                            print(data_frame)
                            clm_name_list.append(name)
                            self.show_column_names.insert('end', name)
                            #self.show_column(name)
                            show_data_list.delete(0, 'end')
                            name = ''
                            val_list.clear()
                            return True
                        elif tot_column > 0:
                            if tot_rows != count:
                                result = yesno(f'Different value Length !!\nPrevous Cloumn has {tot_rows} values, but you add {count} values\nDo you want to readd values ?')
                                if result == True:
                                    val_list.clear()
                                    show_data_list.delete(0, 'end')
                            else:
                                data_frame[f'{name}'] = val_list
                                print(data_frame)
                                show_data_list.delete(0, 'end')
                                clm_name_list.append(name)
                                self.show_column_names.insert('end', name)
                                name = ''
                                val_list.clear()
                                return True
                        else:
                            error_msg('Something went Wrong !!')
            else:
                error_msg('Input Alphebetics Letters Only !!')

              

    def cancel(self, msg):
        result = yesno(msg)
        return result

    def column_btn(self, name):
        #information_msg(f'This is {name} Column')
        column_name_window = top_level()

    def get_value_from_dataframe(self, name, dataframe):
        try:
            val_list = dataframe[f'{name}'].tolist()
            return val_list
        except:
            return False

    def get_column_names(self, dataframe):
        try:
            name_list = dataframe.columns.tolist()
            return name_list
        except:
            return False

    def Create_new_table(self, dataframe):
        try:
            columns = dataframe.columns.tolist()
            dataframe.drop(dataframe.index, inplace=True)
            print(dataframe)
            information_msg('Detete Sucessfull !!')
        except:
            error_msg('Something Went Wrong !!')