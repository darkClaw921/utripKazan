import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger


class Sheet():

    @logger.catch
    def __init__(self, jsonPath: str, sheetName: str, workSheetName, servisName: str = None):

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']  # что то для чего-то нужно Костыль
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            jsonPath, self.scope)  # Секретынй файл json для доступа к API
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(sheetName).worksheet(
            workSheetName)  # Имя таблицы
        # self.sheet = self.client.open(workSheetName)  # Имя таблицы

    def send_cell(self, position: str, value):
        #self.sheet.update_cell(position, value=value)
        self.sheet.update(position, value)

    def update_cell(self, r, c, value):
        self.sheet.update_cell(int(r), int(c), value)
        # sheet.update_cell(1, 1, "I just wrote to a spreadsheet using Python!")0

    def find_cell(self, value):
        cell = self.sheet.find(value)
        return cell

    def get_cell(self, row: str):
        # A1
        cell = self.sheet.acell(row).value
        return cell

