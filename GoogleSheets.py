from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime

import AppConfig

class GoogleSheets():
    def __init__(self, 
                scopes=['https://www.googleapis.com/auth/spreadsheets']):
        self.scopes = scopes
        self.sheet = self._initSheet()
        self.config = AppConfig.config

    def _initSheet(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', self.scopes)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        return sheet

    # def readRange(self,
    #                 spreadsheetID='1XbFflGI5sn_w4Bxt-rRg-mb-AYFrDfGWS7-qMSJZomY',
    #                 rangeName='Sheet1!A2:E'):
    #     result = self.sheet.values().get(spreadsheetId=spreadsheetID,
    #                             range=rangeName).execute()
    #     values = result.get('values', [])

    #     if not values:
    #         print('No data found.')
    #     else:
    #         print('Name, Major:')
    #         for row in values:
    #             # Print columns A and E, which correspond to indices 0 and 4.
    #             print('%s, %s' % (row[0], row[4]))

    def readRange(self, spreadsheetID='', rangeName=''):
        if not spreadsheetID:
            spreadsheetID = self.config["spreadsheetID"]
        if not rangeName:
            rangeName = self.config["spreadsheetRange"]
        print(rangeName)
        # How values should be represented in the output.
        # The default render option is ValueRenderOption.FORMATTED_VALUE.
        # value_render_option = 'FORMATTED_VALUE'  # TODO: Update placeholder value.
        
        # How dates, times, and durations should be represented in the output.
        # This is ignored if value_render_option is
        # FORMATTED_VALUE.
        # The default dateTime render option is [DateTimeRenderOption.SERIAL_NUMBER].
        # date_time_render_option = 'FORMATTED_STRING'  # TODO: Update placeholder value.
        result = self.sheet.values().get(spreadsheetId=spreadsheetID,
                                range=rangeName).execute()
        # print(result)
        values = result.get('values', [])
        
        if not values:
            print('No data found.')
        else:
            print('Name, Major:')
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                # print('%s, %s' % (row[0], row[4]))
                print(row)
                
        return values
        
    def writeStockInfo(self, stockInfo, startRow, spreadsheetID=''):
        if not spreadsheetID:
            spreadsheetID = self.config["spreadsheetID"]
        # if not rangeName:
        #     rangeName = self.config["spreadsheetRange"]
        # Send data to be written
        body = {
            'values': stockInfo
        }
        
        # rangeName = f"B{rowNumber}"
        rangeName = f"Sheet1!B{startRow}:Z"

        value_input_option = "RAW" # ["RAW","USER_ENTERED"]
        print(f"About to writ data: {stockInfo}")
        result = self.sheet.values().update(
            spreadsheetId=spreadsheetID, range=rangeName,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

    # This function will write inputted transaction into Google Sheets
    '''
    Example row data for Google Sheets
        values = [
            ['row1','aa','ascc','as'],
            ['row2','sad','s','xa'],
            ['row3','asds','sad','eas']
        ]
    '''
    def writeTransactions(self, 
                            transactionsList, 
                            spreadsheetID='',
                            rangeName=''):
        print("Writing transactions to sheets")

        if not spreadsheetID:
            spreadsheetID = self.config["spreadsheetID"]
        if not rangeName:
            rangeName = self.config["spreadsheetRange"]

        colParser = TransactionColumnParser()

        # Initialise column names for first row
        sheetData = [
            colParser.getColumnHeaders()
        ]

        for t in transactionsList:
            transactionRow = colParser.parse(t)
            sheetData.append(transactionRow)

        # Send data to be written
        body = {
            'values': sheetData
        }

        value_input_option = "USER_ENTERED" # ["RAW","USER_ENTERED"]
        result = self.sheet.values().update(
            spreadsheetId=spreadsheetID, range=rangeName,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))