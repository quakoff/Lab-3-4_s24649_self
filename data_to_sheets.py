import os
import json
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Wczytywanie zmiennych środowiskowych
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')

# Wczytanie poświadczeń z pliku JSON zapisanego jako zmienna środowiskowa
credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')

if not credentials_json:
    logging.error("Brak poświadczeń Google do arkusza. Zdefiniuj GOOGLE_CREDENTIALS_JSON w sekrecie.")
    exit(1)

# Konwertowanie JSON do słownika
try:
    credentials_info = json.loads(credentials_json)
except json.JSONDecodeError as e:
    logging.error(f"Błąd dekodowania JSON: {e}")
    exit(1)

# Sprawdzanie, czy plik CSV istnieje
csv_file_path = 'data_student_24649.csv'

if not os.path.exists(csv_file_path):
    logging.error(f"Plik {csv_file_path} nie istnieje.")
    exit(1)  # Zakończ program, jeśli plik nie istnieje

# Wczytanie danych z pliku CSV
try:
    df = pd.read_csv(csv_file_path)
    logging.info(f"Wczytano {len(df)} wierszy danych z pliku {csv_file_path}.")
except Exception as e:
    logging.error(f"Nie udało się wczytać danych z pliku CSV: {e}")
    exit(1)  # Zakończ program w przypadku błędu

# Przesyłanie danych do Google Sheets
try:
    # Uwierzytelnienie za pomocą konta serwisowego
    credentials = Credentials.from_service_account_info(credentials_info)
    gc = gspread.authorize(credentials)

    # Otwieranie arkusza
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # Zakładając, że chcesz korzystać z pierwszego arkusza

    # Czyści istniejące dane
    worksheet.clear()
    logging.info("Istniejące dane w arkuszu zostały usunięte.")

    # Wysyłanie nowych danych
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    logging.info("Dane zostały przesłane do Google Sheets.")
except Exception as e:
    logging.error(f"Nie udało się przesłać danych do Google Sheets: {e}")

logging.info("Proces zakończony.")
