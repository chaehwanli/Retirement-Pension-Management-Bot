
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from config import settings, secrets
import json

class GoogleSheetsManager:
    def __init__(self, key_path_or_string):
        """
        Initializes the Google Sheets manager.
        Args:
            key_path_or_string: Path to the JSON key file or the JSON string itself.
        """
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        
        try:
             # If it looks like a JSON string, parse it directly
            creds_dict = json.loads(key_path_or_string)
            self.creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, self.scope)
        except json.JSONDecodeError:
            # Assume it's a file path
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(key_path_or_string, self.scope)
            
        self.client = gspread.authorize(self.creds)

    def get_sheet_data(self, sheet_name):
        """
        Reads data from a specific sheet and returns it as a list of dictionaries.
        """
        try:
            sheet = self.client.open("ISA_관리").worksheet(sheet_name)
            return sheet.get_all_records()
        except gspread.exceptions.WorksheetNotFound:
            print(f"Error: Worksheet '{sheet_name}' not found.")
            return []

    def update_cell(self, sheet_name, row, col, value):
        """
        Updates a specific cell in a sheet.
        """
        try:
            sheet = self.client.open("ISA_관리").worksheet(sheet_name)
            sheet.update_cell(row, col, value)
        except Exception as e:
            print(f"Error updating cell: {e}")

    def update_column(self, sheet_name, col_name, data):
        """
        Updates a specific column with a list of values.
        Finds the column index by name (header).
        """
        try:
            sheet = self.client.open("ISA_관리").worksheet(sheet_name)
            headers = sheet.row_values(1)
            try:
                col_index = headers.index(col_name) + 1
            except ValueError:
                print(f"Error: Column '{col_name}' not found.")
                return

            # Prepare data for batch update (list of lists)
            cell_list = []
            for i, val in enumerate(data):
                cell_list.append([val])
            
            # Update range (start from row 2)
            range_str = f"{gspread.utils.rowcol_to_a1(2, col_index)}:{gspread.utils.rowcol_to_a1(len(data) + 1, col_index)}"
            sheet.update(range_str, cell_list)
            
        except Exception as e:
            print(f"Error updating column: {e}")

    def update_sheet_from_df(self, sheet_name, df):
        """
        Overwrites the sheet with Dataframe content.
        """
        try:
            sheet = self.client.open("ISA_관리").worksheet(sheet_name)
            sheet.clear()
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
        except Exception as e:
            print(f"Error updating sheet from DF: {e}")
