# Dokumentacja Projektu

### Opis plików

Poniżej znajduje się opis każdego pliku, który jest częścią projektu. Dzięki temu można lepiej zrozumieć, co dokładnie dzieje się na każdym etapie przetwarzania danych i budowania modelu.

- ~~**fetch_data.py**  
 W tym pliku łączymy się z Google Sheets, aby pobrać dane do lokalnego pliku CSV (`data_from_sheets.csv`). Robi to automatycznie przy użyciu Google API, żebyśmy nie musieli ręcznie zrzucać danych za każdym razem.
 Google API wywalało się przy tak duzej ilośći danych, więc dane będą pobierane bezpośredniu z linku podanego w zadaniu i zapisywane do pliku `data_from_sheets.csv`.~~
 Fetchowanie mi nie szło, więc dane są pobierane z pliku CSV bezpośrednio z folderu.
- **feature_enginee.py**  
  Ten plik służy do przygotowania danych. Przekształca zmienne kategoryczne na zmienne numeryczne (bo modele tego wymagają), a następnie skaluje zmienne liczbowe, żeby były w podobnym zakresie. Na koniec dzieli dane na zbiór treningowy i testowy, zapisując je w osobnych plikach, żeby można było sprawdzić, jak model radzi sobie na nowych danych.

- **model_training.py**  
  
    Plik ten trenuje model na przygotowanych danych. Użyłem modelu **XGBoost**, ponieważ jest to zaawansowany model, który dobrze radzi sobie z danymi mieszanymi (czyli takimi, które mają różne typy cech – kategoryczne i numeryczne) i charakteryzuje się dużą wydajnością oraz elastycznością. XGBoost może skutecznie modelować nieliniowe zależności oraz jest odporny na przetrenowanie, co czyni go idealnym rozwiązaniem dla złożonych zbiorów danych.

    Po treningu plik zapisuje wyniki modelu (MSE i R²) do pliku `logs.txt`, aby można było łatwo zobaczyć, jak model sobie radzi.

- **report.txt**  
  To plik, który generuje `train_model.py`. Zawiera informacje o wynikach modelu i krótkie podsumowanie, dlaczego wybrano taki model. Dzięki temu można szybko sprawdzić, jak dobrze model działa na zbiorze testowym.

### Wyjaśnienie wyboru modelu

Przetestowałem wiele modeli jednocześnie, użyłem tego który ostatecznie dawał moim zdaniem najelepsze wyniki. 
    Oto wyniki dla różnych modeli:

Metryki Modeli na Zbiorze Testowym
- **RandomForest**: MSE = 54.207190116237534, R² = 0.28517082472169053
- **XGBoost**: MSE = 48.182387438851904, R² = 0.36461978195144495
- **LinearRegression**: MSE = 49.111200652362285, R² = 0.352371539938208
- **SVR**: MSE = 49.63096456234643, R² = 0.34551742323677614
