import os
import gspread
import pandas as pd
import logging
from google.oauth2.service_account import Credentials

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Uwierzytelnienie i połączenie z Google Sheets
logging.info("Rozpoczynam proces uwierzytelniania i pobierania danych z Google Sheets.")

spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
api_key = os.getenv('GOOGLE_API_KEY')

try:
    # Konfiguracja połączenia
    credentials = Credentials.from_service_account_info(api_key)
    gc = gspread.authorize(credentials)

    # Otwórz arkusz
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # Pierwszy arkusz

    # Pobierz dane
    data = worksheet.get_all_values()
    logging.info("Dane zostały pobrane z Google Sheets.")

    # Przekształć dane w DataFrame
    df = pd.DataFrame(data[1:], columns=data[0])  # Pierwszy wiersz to nagłówki
    df.to_csv("data_from_sheets.csv", index=False)  # Zapisz dane do pliku CSV
    logging.info("Dane zostały zapisane do pliku data_from_sheets.csv.")

except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z Google Sheets: {e}")
