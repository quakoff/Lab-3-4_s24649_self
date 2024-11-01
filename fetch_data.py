import os
import pandas as pd
import requests
import logging

# Konfiguracja loggera
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

api_key = os.getenv('GOOGLE_API_KEY')
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
#spreadsheet_id = '1Mjih1A3Lj8mU_GReSrz2WUZXXKmis-9ZXaUeblu5zLw'


# URL do pobrania danych z Google Sheets, zmieniony arkusz na nowy
url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Zad3?key={api_key}"

try:
    # Wysłanie żądania do Google Sheets API
    response = requests.get(url)

    # Sprawdzenie czy odpowiedź jest poprawna
    if response.status_code == 200:
        logging.info("Dane zostały pobrane z Google Sheets")
        data = response.json()

        # Sprawdzenie, czy odpowiedź zawiera dane
        if 'values' in data:
            # Przetwarzanie danych
            df = pd.DataFrame(data['values'][1:], columns=data['values'][0])

            # Sprawdzenie liczby wierszy
            total_rows = df.shape[0]
            logging.info(f"Wczytano {total_rows} wierszy danych z Google Sheets.")

            # Zapisanie danych do pliku CSV
            df.to_csv('data_from_sheets.csv', index=False)
            logging.info("Dane zapisano do pliku CSV.")
        else:
            logging.error("Brak danych w odpowiedzi API.")
            raise ValueError("Brak danych w odpowiedzi API.")

    else:
        logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
        logging.error(f"Treść odpowiedzi: {response.text}")
        raise ValueError(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")

except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z Google Sheets: {e}")
