import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Ustawienie logowania
logging.basicConfig(filename='logs.log', level=logging.INFO)
logging.info("Rozpoczęcie przetwarzania i modelowania.")

# Wczytanie danych
df = pd.read_csv("data_from_url.csv")
logging.info(f"Wczytano dane: {df.shape[0]} wierszy, {df.shape[1]} kolumn.")

# Przekształcenie `score` na klasy
df['score_class'] = pd.qcut(df['score'], q=3, labels=['low', 'medium', 'high'])

# Definicja cech
X = df.drop(columns=["score", "score_class"])
y = df["score_class"]

# Wybór cech numerycznych i kategorycznych
numeric_features = ["unemp", "wage", "distance", "tuition", "education"]
categorical_features = ["gender", "ethnicity", "fcollege", "mcollege", "home", "urban", "income", "region"]

# Preprocessing dla danych numerycznych i kategorycznych
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(drop='first'))
])

# Złączenie przekształceń
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Pipeline łączący preprocesor i model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Podział na zbiór treningowy i testowy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logging.info(f"Podział danych: X_train={X_train.shape}, X_test={X_test.shape}")

# Trenowanie modelu
model.fit(X_train, y_train)
logging.info("Model Random Forest został wytrenowany.")

# Ewaluacja modelu
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
logging.info(f"Dokładność modelu: {accuracy}")
logging.info(f"Macierz pomyłek: \n{conf_matrix}")

# Wyświetlenie macierzy pomyłek
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['low', 'medium', 'high'], yticklabels=['low', 'medium', 'high'])
plt.xlabel("Przewidywana klasa")
plt.ylabel("Rzeczywista klasa")
plt.title("Macierz pomyłek")
plt.savefig("confusion_matrix.png")

# Obliczanie AUC dla klasyfikacji wieloklasowej (metoda 'ovr' - one-vs-rest)
y_pred_proba = model.predict_proba(X_test)
auc_score = roc_auc_score(pd.get_dummies(y_test), y_pred_proba, multi_class='ovr')
logging.info(f"AUC modelu: {auc_score}")

# Analiza znaczenia cech
feature_importances = model.named_steps['classifier'].feature_importances_
feature_names = numeric_features + list(model.named_steps['preprocessor'].transformers_[1][1].named_steps['onehot'].get_feature_names_out(categorical_features))
feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': feature_importances}).sort_values(by='importance', ascending=False)

# Wyświetlenie wykresu znaczenia cech
plt.figure(figsize=(10, 8))
sns.barplot(x='importance', y='feature', data=feature_importance_df)
plt.title("Znaczenie cech w modelu Random Forest")
plt.xlabel("Waga cechy")
plt.ylabel("Cechy")
plt.savefig("feature_importance.png")

# Zapis wyników do pliku
with open("report_rf.txt", "w") as report_file:
    report_content = f"""
### Raport z Trenowania Modelu

#### Cel
Celem było przewidywanie przedziału wyniku (`score`) na podstawie różnych cech.

#### Wyniki Modelu
- Dokładność (accuracy): {accuracy:.4f}
- AUC: {auc_score:.4f}

#### Analiza Znaczenia Cech
Poniżej przedstawiono najważniejsze cechy wpływające na przewidywania modelu:
{feature_importance_df.to_string(index=False)}

#### Wnioski
Model Random Forest osiągnął dokładność {accuracy:.2%} oraz AUC {auc_score:.2f}. Najbardziej znaczące cechy to:
{feature_importance_df['feature'].iloc[:5].tolist()}.

Dalsza optymalizacja i dostrajanie modelu mogłyby poprawić wyniki.
"""
    report_file.write(report_content)

logging.info("Raport wygenerowany i zapisany jako report_rf.txt")
