# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import StandardScaler
# import logging
#
# # Konfiguracja loggera
# logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
# logging.getLogger().addHandler(logging.StreamHandler())
#
# # Wczytaj dane z CSV
# try:
#     df = pd.read_csv('data_from_sheets.csv')
#     logging.info("Dane zostały wczytane z pliku CSV.")
#
#     # Informacje o danych
#     total_rows = df.shape[0]
#     total_columns = df.shape[1]
#     logging.info(f"Liczba wierszy przed czyszczeniem: {total_rows}")
#     logging.info(f"Liczba kolumn: {total_columns}")
#
#     # Czyszczenie danych - liczenie braków
#     missing_data_count = df.isnull().sum().sum()
#     logging.info(f"Liczba brakujących danych: {missing_data_count}")
#
#     # Ustalamy, które wiersze usunąć na podstawie liczby braków w każdej kolumnie
#     threshold = 1  # Możemy zmienić na inną wartość, aby określić próg usunięcia
#     rows_to_drop = df[df.isnull().sum(axis=1) > threshold]  # Usuwamy wiersze z brakami
#     df_cleaned = df.drop(rows_to_drop.index)
#
#     # Liczymy usunięte wiersze
#     removed_rows = total_rows - df_cleaned.shape[0]
#     logging.info(f"Usunięto {removed_rows} wierszy z zbyt wieloma brakującymi danymi.")
#
#     # Uzupełnianie braków - wybór metody uzupełnienia
#     fill_methods = {
#         'średnia': lambda x: x.fillna(x.mean()),
#         'mediana': lambda x: x.fillna(x.median()),
#         'domyślna': lambda x: x.fillna(0),
#         'tryb': lambda x: x.fillna(x.mode()[0])  # Uzupełnianie trybem
#     }
#
#     # Liczba zmienionych wartości przed uzupełnieniem
#     initial_missing_counts = df_cleaned.isnull().sum()
#
#     # Uzupełniamy dla wszystkich kolumn, w tym nienumerycznych
#     columns_changed = 0
#     for column in df_cleaned.columns:
#         if df_cleaned[column].isnull().any():
#             fill_method = 'tryb' if df_cleaned[column].dtype == 'object' else 'średnia'
#             df_cleaned[column] = fill_methods[fill_method](df_cleaned[column])
#             columns_changed += 1  # Zwiększamy licznik zmienionych kolumn
#
#     # Liczba zmienionych wartości po uzupełnieniu
#     final_missing_counts = df_cleaned.isnull().sum()
#     filled_values_per_column = initial_missing_counts - final_missing_counts
#     total_filled_values = filled_values_per_column.sum()  # Liczba wszystkich uzupełnionych wartości
#
#     logging.info(f"Uzupełniono {total_filled_values} brakujących wartości w kolumnach.")
#
#     # Standaryzacja danych (średnia 0, odchylenie standardowe 1)
#     scaler = StandardScaler()
#     numeric_columns = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
#
#     if numeric_columns:
#         df_cleaned[numeric_columns] = scaler.fit_transform(df_cleaned[numeric_columns])
#         logging.info("Dane zostały znormalizowane.")
#     else:
#         logging.warning("Brak kolumn numerycznych do standaryzacji.")
#
#     # Zapisywanie wyczyszczonych danych do pliku
#     df_cleaned.to_csv('cleaned_data.csv', index=False)
#     logging.info("Wyczyszczone dane zapisano do pliku 'cleaned_data.csv'.")
#
#     # Generowanie raportu
#     report = f"""
#     Liczba oryginalnych wierszy: {total_rows}
#     Liczba usuniętych wierszy: {removed_rows} ({removed_rows / total_rows * 100:.2f}%)
#     Liczba uzupełnionych wartości: {total_filled_values}
#     Procent uzupełnionych danych: {total_filled_values / missing_data_count * 100:.2f}%
#     Liczba zmienionych kolumn: {columns_changed}
#     Liczba pozostałych brakujących wartości: {df_cleaned.isnull().sum().sum()}
#     """
#     with open('report.txt', 'w') as report_file:
#         report_file.write(report)
#
#     logging.info("Raport wygenerowany i zapisany do pliku 'report.txt'.")
#
# except Exception as e:
#     logging.error(f"Wystąpił błąd podczas przetwarzania danych: {e}")
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Wczytaj dane z CSV
try:
    df = pd.read_csv('data_from_sheets.csv')
    logging.info("Dane zostały wczytane z pliku CSV.")

    # Informacje o danych
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    total_cells = total_rows * total_columns  # Całkowita liczba komórek w danych
    logging.info(f"Liczba wierszy: {total_rows}, liczba kolumn: {total_columns}, liczba komórek: {total_cells}")

    # Czyszczenie danych - liczenie braków
    initial_missing_data_count = df.isnull().sum().sum()  # Łączna liczba brakujących komórek
    logging.info(f"Liczba brakujących danych przed uzupełnieniem: {initial_missing_data_count}")

    # Usuwanie wierszy z zbyt wieloma brakującymi wartościami
    threshold = 2  # Usuwamy wiersze, gdzie brakuje więcej niż threshold kolumn
    df_cleaned = df.dropna(thresh=df.shape[1] - threshold)

    # Liczba usuniętych wierszy
    removed_rows = total_rows - df_cleaned.shape[0]
    logging.info(f"Usunięto {removed_rows} wierszy z zbyt wieloma brakującymi danymi.")

    # Uzupełnianie braków - wybór metody uzupełnienia
    fill_methods = {
        'średnia': lambda x: x.fillna(x.mean()),
        'mediana': lambda x: x.fillna(x.median()),
        'domyślna': lambda x: x.fillna(0),
        'tryb': lambda x: x.fillna(x.mode()[0])  # Uzupełnianie trybem dla nienumerycznych
    }

    # Przed uzupełnieniem liczymy brakujące dane
    before_fill_missing_count = df_cleaned.isnull().sum().sum()

    # Uzupełniamy brakujące wartości
    total_filled_values = 0
    columns_changed = 0  # Liczba kolumn, w których uzupełniono dane

    for column in df_cleaned.columns:
        if df_cleaned[column].isnull().any():
            fill_method = 'tryb' if df_cleaned[column].dtype == 'object' else 'średnia'
            filled_column = fill_methods[fill_method](df_cleaned[column])
            filled_count = df_cleaned[column].isnull().sum() - filled_column.isnull().sum()  # Ile wartości uzupełniono
            total_filled_values += filled_count
            if filled_count > 0:
                columns_changed += 1
            df_cleaned[column] = filled_column

    # Po
