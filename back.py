# Backend
import pandas as pd

class Back():

    def __init__(self):
        super().__init__()

    def create_dataframe(self, name):
        try:
            name = pd.DataFrame()
            self.dataframes_object_list.append(name) 
            return True
        except:
            return False

    def get_data_frame(self, index):
        try:
            d_frame = self.dataframes_object_list[index]
            return d_frame
        except:
            return False

    def get_column_names(self, d_frame):
        try:
            name_list = d_frame.columns.tolist()
            return name_list
        except:
            return False

    def get_number_of_rows(self, dataframe):
        try:
            number = len(dataframe)
            return number
        except:
            return False

    def add_column_data(self, dataframe, cl_name, value_list):
        try:
            dataframe[f'{cl_name}'] = value_list
            print(dataframe)
            return True
        except:
            return False        

    def get_column_values(self, dataframe, cl_name):
        try:
            value_list = dataframe[f'{cl_name}'].tolist()
            return value_list
        except:
            return False

    def delete_dataframe(self, dataframe, index):
        try:
            self.dataframes_object_list.pop(index)
            del dataframe
            return True
        except:
            return False

    def drop_dataframe_column(self, dataframe, cl_name):
        try:
            del dataframe[cl_name]
            return True
        except:
            return False

    def clear_dataframe_index(self, dataframe):
        try:
            dataframe.drop(dataframe.index, inplace=True)
            return True
        except:
            return False

    def rename_column(self, dataframe, new_column_names):
        try:
            dataframe.columns = new_column_names
            return True
        except:
            return False
