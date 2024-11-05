import requests
import logging

# Konfiguracja loggera
logging.basicConfig(filename='logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Link do pliku CSV
csv_url = pd.read_csv("https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv")

try:
    # Pobieranie danych bezpośrednio z URL
    logging.info("Rozpoczęto pobieranie danych z URL.")
    response = requests.get(csv_url)

    # Sprawdzamy, czy pobieranie zakończyło się sukcesem
    if response.status_code == 200:
        # Zapisanie pobranego pliku na lokalny dysk
        with open('data_from_url_BACKUP.csv', 'wb') as f:
            f.write(response.content)
        logging.info("Dane zostały pobrane i zapisane do pliku CSV.")
    else:
        logging.error(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")
        raise ValueError(f"Nie udało się pobrać danych. Kod błędu: {response.status_code}")

except Exception as e:
    logging.error(f"Wystąpił błąd podczas pobierania danych z URL: {e}")
