import os
import requests
import pandas as pd
import logging

from train import spreadsheet_id

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Pobranie zmiennych środowiskowych z GitHub Secrets
api_key = os.getenv('GOOGLE_API_KEY')
# spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
spreadsheet_id = "1Mjih1A3Lj8mU_GReSrz2WUZXXKmis-9ZXaUeblu5zLw"

# URL do pobrania danych z Google Sheets
url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Dane?key={api_key}"

# Wysłanie żądania do Google Sheets API
response = requests.get(url)

# Sprawdzenie czy odpowiedź jest poprawna
if response.status_code == 200:
    logging.info("Dane zostały pobrane z Google Sheets")

    # Sprawdzenie czy odpowiedź jest w formacie JSON
    try:
        data = response.json()

        # Sprawdzenie, czy w odpowiedzi znajdują się dane
        if 'values' in data:
            df = pd.DataFrame(data['values'][1:], columns=data['values'][0])  # Nagłówki z pierwszego wiersza
            df.to_csv('data_from_sheets.csv', index=False)
            logging.info(f"Wczytano {len(df)} wierszy danych z Google Sheets i zapisano do pliku CSV.")
        else:
            logging.error("Brak danych w odpowiedzi API.")
            raise ValueError("Odpowiedź nie zawiera klucza 'values'.")

    except ValueError as e:
        logging.error(f"Wystąpił błąd podczas przetwarzania odpowiedzi z Google Sheets: {e}")

else:
    logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
    raise Exception(f"Nieprawidłowy kod odpowiedzi: {response.status_code}")
