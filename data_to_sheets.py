import os
import json
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Wczytywanie zmiennych środowiskowych
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')

if not credentials_json:
    logging.error("Brak poświadczeń Google do arkusza. Zdefiniuj GOOGLE_CREDENTIALS_JSON w sekrecie.")
    exit(1)

# Zakresy autoryzacji
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Wczytanie poświadczeń z JSON
try:
    credentials_info = json.loads(credentials_json)
    credentials = Credentials.from_service_account_info(credentials_info, scopes=SCOPES)
except json.JSONDecodeError as e:
    logging.error(f"Błąd dekodowania JSON: {e}")
    exit(1)

# Inicjalizacja klienta gspread
try:
    gc = gspread.authorize(credentials)
except Exception as e:
    logging.error(f"Błąd autoryzacji gspread: {e}")
    exit(1)

# Otwieranie arkusza
try:
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # Pierwszy arkusz
except gspread.SpreadsheetNotFound:
    logging.error("Nie znaleziono arkusza. Sprawdź ID arkusza Google.")
except gspread.APIError as e:
    logging.error(f"Błąd API Google: {e}")
except Exception as e:
    logging.error(f"Inny błąd podczas otwierania arkusza: {e}")


# Usuwanie istniejących danych i wstawianie nowych
try:
    worksheet.clear()  # Usuwanie danych
    df = pd.read_csv('data_student_24649.csv')  # Wczytanie pliku CSV
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())  # Aktualizacja arkusza
    logging.info("Dane zostały przesłane do Google Sheets.")
except Exception as e:
    logging.error(f"Nie udało się przesłać danych do Google Sheets: {e}")
