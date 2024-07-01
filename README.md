# Aplikacja do Zarządzania Kontami Użytkowników w Monday.com

## Opis Aplikacji

Aplikacja służy do automatycznego pobierania danych z platformy Monday.com oraz do zarządzania kontami użytkowników, ich konfiguracją e-mail oraz generowaniem stopki e-mail. Główne funkcjonalności aplikacji obejmują:

- Pobieranie danych użytkowników z Monday.com za pomocą API.
- Przetwarzanie danych i przechowywanie ich w lokalnej zmiennej.
- Transformacja danych osobowych (np. formatowanie numerów telefonów).
- Generowanie stopki e-mail na podstawie szablonu HTML.
- Automatyczne konfigurowanie kont e-mail użytkowników, w tym ustawienia preferencji i podpisu.
- Wysyłanie powiadomień SMS do użytkowników.
- Generowanie plików VCF z kontaktami użytkowników.

## Wymagania

Aby uruchomić aplikację, potrzebujesz:

- Python 3.x
- Zainstalowane biblioteki Python: `requests`, `selenium`, `phonenumbers`, `smsapi-client`
- Przeglądarka Google Chrome oraz zainstalowany ChromeDriver
- Klucz API do Monday.com
- Konto SMSAPI oraz odpowiedni token dostępu
- Szablon stopki w formacie HTML zapisany w folderze `template/`

## Instalacja

1. Zainstaluj wymagane biblioteki Python:
   ```bash
   pip install requests selenium phonenumbers smsapi-client
   ```
2. Pobierz i zainstaluj ChromeDriver odpowiedni dla Twojej wersji przeglądarki Google Chrome.

3. Upewnij się, że plik szablonu stopki HTML znajduje się w folderze template/ oraz że folder footer/ istnieje.

## Uruchomienie Aplikacji

Skonfiguruj klucz API i ID tablicy w Monday.com oraz do SMSAPI:

```python
apiKey = "secret api key here"
IDS = "1234567890"
SMS_API_KEY = "sms api key here"
```

Uruchom program:
```bath
python main.py
```

Aplikacja automatycznie pobierze dane z Monday.com, przetworzy je i wygeneruje stopki e-mail oraz skonfiguruje konta e-mail użytkowników w zależności od wybranej opcji.

##Opis Działania

Pobieranie Danych z Monday.com
Aplikacja wykorzystuje API Monday.com do pobierania danych użytkowników. Pobierane są wartości z kolumn określonej tablicy i przetwarzane w celu dalszej obróbki.

Przetwarzanie Danych
Dane są filtrowane i przetwarzane, aby usunąć niepotrzebne znaki oraz zamienić puste wartości na "NULL". Numery telefonów są formatowane zgodnie z międzynarodowymi standardami.

Generowanie Stopki E-mail
Na podstawie przetworzonych danych aplikacja generuje stopkę e-mail, którą zapisuje w formacie HTML. Szablon stopki znajduje się w folderze template/, a gotowe stopki są zapisywane w folderze footer/.

Konfiguracja Kont E-mail
Aplikacja automatycznie loguje się na konta e-mail użytkowników, konfiguruje ustawienia preferencji, dodaje podpis oraz ustawia nazwę konta. Proces ten jest realizowany za pomocą Selenium.

Wysyłanie Powiadomień SMS
Aplikacja umożliwia wysyłanie powiadomień SMS do użytkowników z wykorzystaniem API SMSAPI.

Generowanie Plików VCF
Aplikacja tworzy plik VCF zawierający kontakty wszystkich użytkowników, co ułatwia importowanie ich do książki adresowej.

