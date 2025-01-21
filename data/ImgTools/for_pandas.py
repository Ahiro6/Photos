import pandas as pd


class GetData:

    def __init__(self, data, type_data, divider=","):
        self.type = type_data
        if self.type == "txt" or self.type == "csv":
            self.name = pd.read_csv(data, divider)
        elif self.type == "json":
            self.name = pd.read_json(data, divider)
        elif self.type == "excel":
            self.name = pd.read_excel(data, divider)

    def get_column(self, column):
        selected_data = list(self.name[column])
        return selected_data

