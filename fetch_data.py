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
    data.to_csv("data_from_url.csv", index=False)
    logging.info("Dane zostały pomyślnie zapisane do pliku data_from_url.csv.")

    dff = pd.read_csv("data_from_url.csv")
    # Wyświetlenie kilku pierwszych wierszy jako potwierdzenie
    print(dff.head())
except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z URL: {e}")
