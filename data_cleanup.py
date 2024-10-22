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

# Sprawdzenie, czy dane są poprawnie wczytane
if df.empty:
    logging.error("Plik CSV jest pusty.")
    exit()

# Podstawowe informacje o danych
total_rows, total_columns = df.shape
logging.info(f"Liczba wierszy: {total_rows}, Liczba kolumn: {total_columns}")

# Podział na kolumny numeryczne i nienumeryczne
numeric_cols = df.select_dtypes(include=[np.number]).columns
non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns

missing_values_before = df.isnull().sum().sum()

# Usuwanie wierszy z brakującymi wartościami powyżej progu (np. 20% braków)
df_cleaned = df.dropna(thresh=int(0.8 * total_columns))  # Usuwanie wierszy z ponad 20% brakami

# Uzupełnianie braków w kolumnach numerycznych medianą
df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].median())

# Uzupełnianie braków w kolumnach nienumerycznych napisem "BD"
df_cleaned[non_numeric_cols] = df_cleaned[non_numeric_cols].fillna("BD")

# Logowanie informacji o uzupełnionych danych w kolumnach nienumerycznych
for col in non_numeric_cols:
    num_missing = df[col].isnull().sum()
    if num_missing > 0:
        logging.info(f"Uzupełniono {num_missing} brakujących wartości w kolumnie '{col}' napisem 'BD'.")

# Standaryzacja kolumn numerycznych
scaler = StandardScaler()
if len(numeric_cols) > 0:
    df_cleaned[numeric_cols] = scaler.fit_transform(df_cleaned[numeric_cols])
    logging.info(f"Standaryzowano kolumny numeryczne: {', '.join(numeric_cols)}")

# Informacje o danych po czyszczeniu
removed_rows = total_rows - df_cleaned.shape[0]
percent_removed_rows = (removed_rows / total_rows) * 100

missing_values_after = df_cleaned.isnull().sum().sum()
filled_values = missing_values_before - missing_values_after
changed_columns = len(numeric_cols) + len(non_numeric_cols)

logging.info(f"Liczba usuniętych wierszy: {removed_rows} ({percent_removed_rows:.2f}%)")
logging.info(f"Liczba uzupełnionych wartości: {filled_values}")
logging.info(f"Liczba wierszy po przetwarzaniu: {df_cleaned.shape[0]}")
logging.info(f"Liczba zmienionych kolumn: {changed_columns}")

# Generowanie raportu
report = f"""
Ogólna liczba wierszy: {total_rows}
Ogólna liczba kolumn: {total_columns}
Liczba usuniętych wierszy: {removed_rows} ({percent_removed_rows:.2f}%)
Liczba uzupełnionych wartości: {filled_values}
Liczba zmienionych kolumn: {changed_columns}
"""

with open("report.txt", "w") as report_file:
    report_file.write(report)

logging.info("Raport wygenerowany")
