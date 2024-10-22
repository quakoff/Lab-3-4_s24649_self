import os
import pandas as pd
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Wczytywanie zmiennych środowiskowych
spreadsheet_id = os.getenv('GOOGLE_SHEETS_ID')
api_key = os.getenv('GOOGLE_API_KEY')

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

# Czyszczenie danych
logging.info("Rozpoczynam czyszczenie danych.")
missing_data_threshold = 0.2  # próg 20% brakujących danych do usunięcia wiersza
missing_data_count = df.isnull().sum().sum()
total_rows = df.shape[0]

# Usuwanie wierszy z brakami powyżej progu
df_cleaned = df.dropna(thresh=int((1 - missing_data_threshold) * df.shape[1]))

# Uzupełnianie braków średnią (można zmienić na medianę lub inną metodę)
df_filled = df_cleaned.fillna(df.mean(numeric_only=True))

# Standaryzacja danych (średnia 0, odchylenie standardowe 1)
scaler = StandardScaler()
df_standardized = pd.DataFrame(scaler.fit_transform(df_filled), columns=df_filled.columns)

logging.info("Czyszczenie i standaryzacja danych zakończone.")

# Przesyłanie danych do Google Sheets
try:
    # Uwierzytelnienie
    credentials = Credentials.from_service_account_info(api_key)
    gc = gspread.authorize(credentials)

    # Otwieranie arkusza
    spreadsheet = gc.open_by_key(spreadsheet_id)
    worksheet = spreadsheet.sheet1  # Zakładając, że chcesz korzystać z pierwszego arkusza

    # Wysyłanie danych
    worksheet.clear()  # Czyści istniejące dane
    worksheet.update([df_standardized.columns.values.tolist()] + df_standardized.values.tolist())
    logging.info("Dane zostały przesłane do Google Sheets.")
except Exception as e:
    logging.error(f"Nie udało się przesłać danych do Google Sheets: {e}")

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
