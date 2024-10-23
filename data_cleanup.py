import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import StandardScaler

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())


def clean_data(df):
    initial_row_count = len(df)
    initial_col_count = len(df.columns)

    # Logowanie początkowej liczby wierszy i kolumn
    logging.info(f"Wczytano dane: {initial_row_count} wierszy, {initial_col_count} kolumn.")

    # Usuwanie całkowicie pustych wierszy
    df_cleaned = df.dropna(how='all')
    removed_rows = initial_row_count - len(df_cleaned)
    logging.info(f"Usunięto {removed_rows} pustych wierszy.")

    # Konwersja kolumn numerycznych z object do właściwego typu
    numeric_cols = df_cleaned.columns[df_cleaned.apply(pd.to_numeric, errors='coerce').notnull().all()]
    df_cleaned[numeric_cols] = df_cleaned[numeric_cols].apply(pd.to_numeric, errors='coerce')
    logging.info(f"Zmieniono typy danych na numeryczne dla kolumn: {', '.join(numeric_cols)}")

    # Uzupełnianie braków w kolumnach numerycznych medianą
    num_cols_before = df_cleaned.select_dtypes(include=[np.number]).isna().sum().sum()
    df_cleaned.fillna(df_cleaned.median(numeric_only=True), inplace=True)
    num_cols_after = df_cleaned.select_dtypes(include=[np.number]).isna().sum().sum()
    filled_numeric = num_cols_before - num_cols_after
    logging.info(f"Uzupełniono {filled_numeric} wartości numerycznych medianą.")

    # Uzupełnianie braków w kolumnach nienumerycznych "BD"
    non_num_cols_before = df_cleaned.select_dtypes(exclude=[np.number]).isna().sum().sum()
    df_cleaned.fillna("BD", inplace=True)
    non_num_cols_after = df_cleaned.select_dtypes(exclude=[np.number]).isna().sum().sum()
    filled_non_numeric = non_num_cols_before - non_num_cols_after
    logging.info(f"Uzupełniono {filled_non_numeric} wartości nienumerycznych ('BD').")

    # Łącznie uzupełnione wartości
    total_filled = filled_numeric + filled_non_numeric
    logging.info(f"Łącznie uzupełniono {total_filled} wartości.")

    # Standaryzacja danych numerycznych (średnia 0, odchylenie standardowe 1)
    numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns
    scaler = StandardScaler()
    df_cleaned[numeric_columns] = scaler.fit_transform(df_cleaned[numeric_columns])
    logging.info(
        f"Przeprowadzono standaryzację danych numerycznych (średnia=0, odchylenie standardowe=1) dla kolumn: {', '.join(numeric_columns)}")

    # Logowanie końcowej liczby wierszy i kolumn
    final_row_count = len(df_cleaned)
    final_col_count = len(df_cleaned.columns)
    logging.info(f"Po czyszczeniu danych: {final_row_count} wierszy, {final_col_count} kolumn.")

    return df_cleaned


# Wczytaj plik CSV
df = pd.read_csv('data_from_sheets.csv')

# Czyszczenie danych
df_cleaned = clean_data(df)

# Zapisz oczyszczony plik
df_cleaned.to_csv('/data_cleaned.csv', index=False)

# Logowanie zapisania pliku
logging.info("Dane zostały zapisane do pliku: data_cleaned.csv")
