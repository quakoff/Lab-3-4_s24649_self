#import data from csv file to google sheets using google sheets api and service account
import gspread
import csv
from oauth2client.service_account import ServiceAccountCredentials
import os
import json

# Load the data
csv_file_path = 'data_student_24649.csv'

# Connect to the Google Sheets API
#google_service_account_info = json.loads(os.getenv('GOOGLE_SERVICE_ACCOUNT_KEY'))

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Open the Google Sheet from the url in github actions secrets
sh = gc.open_by_key(os.environ['GOOGLE_SHEETS_ID'])
worksheet = sh.get_worksheet(0)

# Clear the existing data
worksheet.clear()

# Update the Google Sheet with the new data
with open(csv_file_path, 'r') as file:
    reader = csv.reader(file)
    data = list(reader)
    worksheet.append_rows(data)

print('Data successfully updated in Google Sheets')


