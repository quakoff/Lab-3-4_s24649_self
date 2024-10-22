import os

import gspread
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Autoryzacja z użyciem API Key
api_key = os.getenv('GOOGLE_API_KEY')
spreadsheet_id = os.getenv('GOOGLE_SHEET_ID')

# Połączenie z Google Sheets z użyciem API Key
gc = gspread.Client(auth=api_key)
sheet = gc.open_by_key(spreadsheet_id).sheet1

# Pobieranie danych z Google Sheets
data = sheet.get_all_records()
df = pd.DataFrame(data)

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
