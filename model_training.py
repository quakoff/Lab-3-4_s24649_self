import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import logging

logging.basicConfig(filename="logs.txt", level=logging.INFO)

# Wczytanie danych
X_train = pd.read_csv("X_train.csv")
X_test = pd.read_csv("X_test.csv")
y_train = pd.read_csv("y_train.csv").values.ravel()
y_test = pd.read_csv("y_test.csv").values.ravel()

# Trenowanie modelu
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
logging.info("Random Forest model trained.")


# Generowanie wyjaśnienia do raportu
report_content = """
### Raport z Trenowania Modelu

#### Wyjaśnienie Wyboru Modelu
Wybrałem model Random Forest Regressor, ponieważ jest prosty w użyciu i dobrze radzi sobie z nieliniowymi zależnościami, co mogłoby pomóc przy różnych zmiennych w danych. Ponadto, lasy losowe są odporne na przetrenowanie, a dane zawierają zarówno zmienne liczbowe, jak i kategoryczne, co ten model dobrze obsługuje.

#### Metryki Modelu na Zbiorze Testowym
Poniżej znajdują się wyniki modelu na zbiorze testowym:
"""

# Ewaluacja modelu
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
r2 = r2_score(y_test, predictions)
logging.info(f"Model evaluation: MSE = {mse}, R2 = {r2}")

report_content += f"""
- Mean Squared Error (MSE): {mse}
- R-squared (R²): {r2}

#### Podsumowanie
Model działa i daje teoretycznie sensowne wyniki. Możliwe, że dałoby się jeszcze poprawić wyniki, ale obecne wyniki są wystarczająco dobre do podstawowej analizy.
"""


with open("report.txt", "w") as report_file:
    report_file.write(report_content)

logging.info("Raport wygenerowany i zapisany jako report.txt")