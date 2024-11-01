import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import logging

# Logging setup
logging.basicConfig(filename='data_processing.log', level=logging.INFO)
logging.info("Rozpoczęcie przetwarzania danych i inżynierii cech.")

# Wczytanie danych
df = pd.read_csv("data_from_url.csv")
logging.info(f"Wczytano dane: {df.shape[0]} wierszy, {df.shape[1]} kolumn.")

# Definicje cech numerycznych i kategorycznych
numeric_features = ["score", "unemp", "wage", "distance", "tuition", "education"]
categorical_features = ["gender", "ethnicity", "fcollege", "mcollege", "home", "urban", "income", "region"]

# Pipeline dla cech numerycznych: imputacja braków, standaryzacja
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# Pipeline dla cech kategorycznych: imputacja braków, OneHotEncoder
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first'))
])

# Połączenie transformacji
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Przygotowanie pełnego przetworzonego zbioru danych
X = df.drop(columns=["score"])  # Zakładamy, że "score" to nasza zmienna docelowa
y = df["score"]

# Transformacja i logowanie statystyk numerycznych
X = preprocessor.fit_transform(X)
logging.info("Dane zostały przetworzone.")
logging.info(f"Standaryzacja i kodowanie cech zakończone: Wymiary zbioru X = {X.shape}")

# Podział na zbiory treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logging.info(f"Podział danych zakończony: X_train={X_train.shape}, X_test={X_test.shape}, y_train={y_train.shape}, y_test={y_test.shape}")

# Zapis wyników do plików
pd.DataFrame(X_train).to_csv("X_train.csv", index=False)
pd.DataFrame(X_test).to_csv("X_test.csv", index=False)
pd.DataFrame(y_train).to_csv("y_train.csv", index=False)
pd.DataFrame(y_test).to_csv("y_test.csv", index=False)
logging.info("Zbiory treningowy i testowy zapisane jako pliki CSV.")
