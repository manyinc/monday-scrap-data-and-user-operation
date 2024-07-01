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
