import pandas as pd
import logging

# Konfiguracja loggera
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Link do pliku CSV
csv_url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv"

try:
    # Pobieranie danych bezpośrednio do DataFrame przy użyciu Pandas
    logging.info("Rozpoczęto pobieranie danych z URL przy użyciu Pandas.")
    data = pd.read_csv(csv_url)
    logging.info("Dane zostały pomyślnie załadowane do DataFrame.")

    # Wyświetlenie kilku pierwszych wierszy jako potwierdzenie
    print(data.head())
except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z URL: {e}")
