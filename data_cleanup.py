import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Odczyt danych z pliku data_from_sheets.csv
file_path = 'data_from_sheets.csv'

try:
    df = pd.read_csv(file_path)
    logging.info(f"Pomyślnie wczytano dane z pliku: {file_path}")
except Exception as e:
    logging.error(f"Nie udało się wczytać danych: {e}")
    exit()

# Podstawowe informacje o danych
total_rows, total_columns = df.shape
logging.info(f"Liczba wierszy: {total_rows}, Liczba kolumn: {total_columns}")

# Uzupełnianie braków - można uzupełnić medianą lub średnią w kolumnach numerycznych
numeric_cols = df.select_dtypes(include=[np.number]).columns
missing_values_before = df.isnull().sum().sum()

# Usuwanie wierszy z brakującymi wartościami (jeśli brakuje zbyt wielu danych)
df_cleaned = df.dropna(thresh=int(0.8 * total_columns))  # Zachowujemy wiersze, które mają min. 80% danych

# Uzupełnianie braków w pozostałych wierszach średnią (lub medianą, można dostosować)
df_cleaned.fillna(df_cleaned.median(), inplace=True)

missing_values_after = df_cleaned.isnull().sum().sum()
filled_values = missing_values_before - missing_values_after

# Standaryzacja wybranych kolumn numerycznych
scaler = StandardScaler()
if len(numeric_cols) > 0:
    df_cleaned[numeric_cols] = scaler.fit_transform(df_cleaned[numeric_cols])
    logging.info(f"Standaryzowano kolumny numeryczne: {', '.join(numeric_cols)}")

# Informacje o danych po czyszczeniu
removed_rows = total_rows - df_cleaned.shape[0]
percent_removed_rows = (removed_rows / total_rows) * 100

logging.info(f"Liczba usuniętych wierszy: {removed_rows} ({percent_removed_rows:.2f}%)")
logging.info(f"Liczba uzupełnionych wartości: {filled_values}")
logging.info(f"Liczba wierszy po przetwarzaniu: {df_cleaned.shape[0]}")

# Generowanie raportu
report = f"""
Ogólna liczba wierszy: {total_rows}
Ogólna liczba kolumn: {total_columns}
Liczba usuniętych wierszy: {removed_rows} ({percent_removed_rows:.2f}%)
Liczba uzupełnionych wartości: {filled_values}
Procent uzupełnionych wartości: {filled_values / (total_rows * total_columns) * 100:.2f}%
"""

with open("report.txt", "w") as report_file:
    report_file.write(report)

logging.info("Raport wygenerowany")
