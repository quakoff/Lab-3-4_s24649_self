import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

# Wczytanie modelu i pipeline'u przy starcie aplikacji
model = load_model("model")

st.title("Przewidywanie kategorii wyniku na podstawie cech")

file = st.file_uploader("Wybierz plik CSV z danymi", type=["csv"])
if file is not None:
    data = pd.read_csv(file)
    predictions = predict_model(model, data=data)
    st.write(predictions)


