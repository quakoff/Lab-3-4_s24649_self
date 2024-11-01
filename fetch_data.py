import pandas as pd
import requests
import logging

# Konfiguracja loggera
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Link do pliku CSV
csv_url = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv"

try:
    # Pobieranie danych bezpośrednio z URL
    logging.info("Rozpoczęto pobieranie danych z URL.")
    response = requests.get(csv_url)

    # Sprawdzamy, czy pobieranie zakończyło się sukcesem
    if response.status_code == 200:
        # Konwersja do DataFrame
        logging.info("Dane zostały pobrane z URL.")
        data = response.content.decode('utf-8')
        df = pd.read_csv(pd.compat.StringIO(data))

        # Logowanie liczby wierszy
        total_rows = df.shape[0]
        logging.info(f"Wczytano {total_rows} wierszy danych z pliku CSV.")

        # Zapisanie danych do pliku CSV
        df.to_csv('data_from_url.csv', index=False)
        logging.info("Dane zapisano do pliku CSV.")
    else:
        logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
        raise ValueError(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")

except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z URL: {e}")
