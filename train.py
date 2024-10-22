import os
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())  # Wyświetlanie logów w konsoli

# Pobranie API Key i ID arkusza z zmiennych środowiskowych
api_key = os.getenv('GOOGLE_API_KEY')
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')

# URL API do odczytu danych z Google Sheets
url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Sheet1?key={api_key}"

# Wysłanie żądania do Google Sheets API
response = requests.get(url)

if response.status_code == 200:
    logging.info("Dane zostały pobrane z Google Sheets.")

    data = response.json().get('values')  # Pobranie danych z odpowiedzi JSON

    if data:
        # Tworzenie DataFrame, zakładając, że pierwszy wiersz to nagłówki
        df = pd.DataFrame(data[1:], columns=data[0])
        logging.info(f"Wczytano {len(df)} wierszy danych.")
    else:
        logging.error("Brak danych w odpowiedzi API.")
        df = None  # Jeśli dane są puste, ustawienie df na None
else:
    logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
    df = None

if df is not None:
    # Czyszczenie danych
    logging.info("Rozpoczynam czyszczenie danych.")

    # Zliczanie brakujących wartości
    missing_data_threshold = 0.2  # próg 20% brakujących danych do usunięcia wiersza
    missing_data_count = df.isnull().sum().sum()
    total_rows = df.shape[0]

    # Usuwanie wierszy z brakami powyżej progu
    df_cleaned = df.dropna(thresh=int((1 - missing_data_threshold) * df.shape[1]))

    # Uzupełnianie braków średnią
    df_filled = df_cleaned.fillna(df.mean(numeric_only=True))

    # Standaryzacja danych (średnia 0, odchylenie standardowe 1)
    scaler = StandardScaler()
    df_standardized = pd.DataFrame(scaler.fit_transform(df_filled), columns=df_filled.columns)

    logging.info("Czyszczenie i standaryzacja danych zakończone.")

    # Generowanie raportu
    removed_rows = total_rows - df_cleaned.shape[0]
    filled_values = missing_data_count - df_cleaned.isnull().sum().sum()

    report = f"""
    Procent usuniętych danych: {removed_rows / total_rows * 100:.2f}%
    Procent uzupełnionych danych: {filled_values / missing_data_count * 100:.2f}%
    """

    with open("report.txt", "w") as report_file:
        report_file.write(report)

    logging.info("Raport został wygenerowany.")
else:
    logging.error("Nie udało się przetworzyć danych. Brak danych do przetworzenia.")
