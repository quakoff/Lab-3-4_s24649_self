import pandas as pd
from sklearn.preprocessing import StandardScaler
import logging

# Konfiguracja loggera
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

logging.info("Rozpoczynam proces czyszczenia i standaryzacji danych.")

# Wczytaj dane z pliku CSV
try:
    df = pd.read_csv('data_from_sheets.csv')
    logging.info(f"Wczytano {len(df)} wierszy danych.")
except Exception as e:
    logging.error(f"Nie udało się wczytać danych: {e}")
    exit(1)

# Usuwanie brakujących danych
missing_data_threshold = 0.2  # próg 20% brakujących danych do usunięcia wiersza
total_rows = df.shape[0]

df_cleaned = df.dropna(thresh=int((1 - missing_data_threshold) * df.shape[1]))  # Usunięcie wierszy z dużą ilością braków
removed_rows = total_rows - df_cleaned.shape[0]
logging.info(f"Usunięto {removed_rows} wierszy z brakującymi danymi.")

# Uzupełnianie brakujących danych (średnią)
df_filled = df_cleaned.fillna(df_cleaned.mean(numeric_only=True))  # Uzupełnienie braków w kolumnach numerycznych średnią
filled_values = df_cleaned.isnull().sum().sum() - df_filled.isnull().sum().sum()
logging.info(f"Uzupełniono {filled_values} brakujących wartości.")

# Standaryzacja danych (tylko dla kolumn numerycznych)
numeric_cols = df_filled.select_dtypes(include=['float64', 'int64']).columns  # Wybór kolumn numerycznych

scaler = StandardScaler()
df_standardized = df_filled.copy()

df_standardized[numeric_cols] = scaler.fit_transform(df_filled[numeric_cols])  # Standaryzacja kolumn numerycznych
logging.info("Standaryzacja danych została zakończona.")

# Zapisanie przetworzonych danych
df_standardized.to_csv("cleaned_data.csv", index=False)
logging.info("Przetworzone dane zapisano w pliku cleaned_data.csv.")

# Generowanie raportu
report = f"""
Procent usuniętych danych: {removed_rows / total_rows * 100:.2f}%
Procent uzupełnionych danych: {filled_values} wartości zostało uzupełnionych.
"""

with open("report.txt", "w") as report_file:
    report_file.write(report)

logging.info("Raport został wygenerowany i zapisany do pliku report.txt.")
