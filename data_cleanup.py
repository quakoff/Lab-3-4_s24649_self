import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

try:
    # Wczytaj dane z CSV
    df = pd.read_csv('data_from_sheets.csv')
    logging.info("Dane zostały wczytane z pliku CSV.")

    # Informacje o danych
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    logging.info(f"Liczba wierszy przed czyszczeniem: {total_rows}")
    logging.info(f"Liczba kolumn: {total_columns}")

    # Czyszczenie danych - liczenie braków
    missing_data_count = df.isnull().sum().sum()
    logging.info(f"Liczba brakujących danych: {missing_data_count}")

    # Usuwanie wierszy z brakami powyżej progu (np. 20% braków w wierszu)
    missing_data_threshold = 0.2  # próg 20%
    df_cleaned = df.dropna(thresh=int((1 - missing_data_threshold) * df.shape[1]))
    removed_rows = total_rows - df_cleaned.shape[0]
    logging.info(f"Usunięto {removed_rows} wierszy z zbyt wieloma brakującymi danymi.")

    # Uzupełnianie braków średnią (lub inną metodą)
    df_filled = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))
    filled_values = df_cleaned.isnull().sum().sum() - df_filled.isnull().sum().sum()
    logging.info(f"Uzupełniono {filled_values} brakujących wartości.")

    # Standaryzacja danych (średnia 0, odchylenie standardowe 1)
    scaler = StandardScaler()
    numeric_columns = df_filled.select_dtypes(include=[np.number]).columns
    df_filled[numeric_columns] = scaler.fit_transform(df_filled[numeric_columns])
    logging.info("Dane zostały znormalizowane.")

    # Zapisywanie wyczyszczonych danych do pliku
    df_filled.to_csv('cleaned_data.csv', index=False)
    logging.info("Wyczyszczone dane zapisano do pliku 'cleaned_data.csv'.")

    # Generowanie raportu
    report = f"""
    Liczba oryginalnych wierszy: {total_rows}
    Liczba usuniętych wierszy: {removed_rows} ({removed_rows / total_rows * 100:.2f}%)
    Liczba uzupełnionych wartości: {filled_values}
    Procent uzupełnionych danych: {filled_values / missing_data_count * 100:.2f}%
    """
    with open('report.txt', 'w') as report_file:
        report_file.write(report)

    logging.info("Raport wygenerowany i zapisany do pliku 'report.txt'.")

except Exception as e:
    logging.error(f"Wystąpił błąd podczas przetwarzania danych: {e}")
