import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import logging

# Konfiguracja logowania
logging.basicConfig(filename="logs.txt", level=logging.INFO)

# Wczytanie danych
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv").values.ravel()
y_test = pd.read_csv("y_test.csv").values.ravel()

# Trenowanie modelu
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
model.fit(X_train, y_train)
logging.info("Model XGBoost został wytrenowany.")

# Generowanie prognoz
predictions = model.predict(X_test)

# Ewaluacja modelu
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
logging.info(f"Ewaluacja modelu: MSE = {mse}, R² = {r2}")

# Generowanie wyjaśnienia do raportu
report_content = f"""
### Raport z Trenowania Modelu XGBoost

#### Metryki Modelu na Zbiorze Testowym
- Mean Squared Error (MSE): {mse}
- R-squared (R²): {r2}

#### Podsumowanie
Model XGBoost dobrze radzi sobie z nieliniowymi zależnościami w danych. Przewidywania są teoretycznie sensowne i można dalej eksperymentować z hyperparametrami, aby uzyskać lepsze wyniki.
"""

# Zapis raportu
with open("report.txt", "w", encoding='utf-8') as report_file:
    report_file.write(report_content)

logging.info("Raport wygenerowany i zapisany jako report.txt.")
