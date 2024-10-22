import os

import gspread
import pandas as pd
import numpy as np
import requests
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

api_key = os.getenv('GOOGLE_API_KEY')
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')

url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/Sheet1?key={api_key}"

# Wysłanie żądania do Google Sheets API
response = requests.get(url)

if response.status_code == 200:
    logging.info("Dane zostały pobrane z Google Sheets")
    data = response.json()['values']
    df = pd.DataFrame(data[1:], columns=data[0])  # Pierwszy wiersz to nagłówki
    logging.info(f"Wczytano {len(df)} wierszy danych")
else:
    logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")

logging.info("Dane wczytane z Google Sheets")

# Czyszczenie danych
missing_data_threshold = 0.2  # próg 20% brakujących danych do usunięcia wiersza
missing_data_count = df.isnull().sum().sum()
total_rows = df.shape[0]

# Usuwanie wierszy z brakami powyżej progu
df_cleaned = df.dropna(thresh=int((1 - missing_data_threshold) * df.shape[1]))

# Uzupełnianie braków średnią (można zmienić na medianę lub inną metodę)
df_filled = df_cleaned.fillna(df.mean())

# Standaryzacja danych (średnia 0, odchylenie standardowe 1)
scaler = StandardScaler()
df_standardized = pd.DataFrame(scaler.fit_transform(df_filled), columns=df_filled.columns)

logging.info("Czyszczenie danych zakończone")

# Generowanie raportu
removed_rows = total_rows - df_cleaned.shape[0]
filled_values = missing_data_count - df_cleaned.isnull().sum().sum()

report = f"""
Procent usuniętych danych: {removed_rows / total_rows * 100:.2f}%
Procent uzupełnionych danych: {filled_values / missing_data_count * 100:.2f}%
"""

with open("report.txt", "w") as report_file:
    report_file.write(report)

logging.info("Raport wygenerowany")
