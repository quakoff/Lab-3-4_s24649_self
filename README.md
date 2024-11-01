# Dokumentacja Projektu

### Opis plików

Poniżej znajduje się opis każdego pliku, który jest częścią projektu. Dzięki temu można lepiej zrozumieć, co dokładnie dzieje się na każdym etapie przetwarzania danych i budowania modelu.

- **fetch_data.py**  
 ~~W tym pliku łączymy się z Google Sheets, aby pobrać dane do lokalnego pliku CSV (`data_from_sheets.csv`). Robi to automatycznie przy użyciu Google API, żebyśmy nie musieli ręcznie zrzucać danych za każdym razem.~~ 
 Google API wywalało się przy tak duzej ilośći danych, więc dane będą pobierane bezpośredniu z linku podanego w zadaniu i zapisywane do pliku `data_from_sheets.csv`.

- **feature_enginee.py**  
  Ten plik służy do przygotowania danych. Przekształca zmienne kategoryczne na zmienne numeryczne (bo modele tego wymagają), a następnie skaluje zmienne liczbowe, żeby były w podobnym zakresie. Na koniec dzieli dane na zbiór treningowy i testowy, zapisując je w osobnych plikach, żeby można było sprawdzić, jak model radzi sobie na nowych danych.

- **model_training.py**  
  Plik ten trenuje model na przygotowanych danych. Użyłem modelu **Random Forest Regressor**, ponieważ jest to prosty model, który dobrze radzi sobie z danymi mieszanymi (czyli takimi, które mają różne typy cech – kategoryczne i numeryczne) i nie wymaga skomplikowanego przygotowania danych. Random Forest jest też odporny na przetrenowanie, więc przy takich danych daje dobre rezultaty bez ryzyka przeuczenia.

  Po treningu plik zapisuje wyniki modelu (MSE i R²) do pliku `report.txt`, żeby można było łatwo zobaczyć, jak model sobie radzi.

- **report.txt**  
  To plik, który generuje `train_model.py`. Zawiera informacje o wynikach modelu i krótkie podsumowanie, dlaczego wybrano taki model. Dzięki temu można szybko sprawdzić, jak dobrze model działa na zbiorze testowym.

### Wyjaśnienie wyboru modelu

Wybrałem **Random Forest Regressor**, dobrze radzi sobie z danymi, które mogą mieć nieliniowe zależności, i obsługuje różne typy cech (numeryczne i kategoryczne). To dobry wybór, ponieważ dane w tym projekcie są mieszane, więc użycie prostego modelu, jak regresja liniowa, mogłoby nie dać tak dobrych wyników.

Random Forest jest też odporny na przetrenowanie, więc mimo stosunkowo prostego pipeline’u, wyniki powinny być stabilne i powtarzalne.
