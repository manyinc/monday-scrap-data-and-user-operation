**Monday Task Manager**

**Task Manager** to aplikacja webowa służąca do zarządzania zadaniami, stworzona w ramach kursu web development. Aplikacja umożliwia użytkownikom tworzenie, edytowanie, usuwanie oraz oznaczanie zadań jako ukończone.

## Funkcjonalności

- **Rejestracja i logowanie użytkowników**: Użytkownicy mogą tworzyć konta i logować się, aby uzyskać dostęp do swoich zadań.
- **Dodawanie zadań**: Użytkownicy mogą dodawać nowe zadania, podając tytuł, opis oraz datę wykonania.
- **Edytowanie zadań**: Możliwość edytowania istniejących zadań.
- **Usuwanie zadań**: Użytkownicy mogą usuwać zadania, które są już niepotrzebne.
- **Oznaczanie zadań jako ukończone**: Zadania mogą być oznaczane jako ukończone, co ułatwia śledzenie postępów.

## Technologie

Aplikacja została stworzona z wykorzystaniem następujących technologii:

- **Frontend**: HTML, CSS, JavaScript, React
- **Backend**: Node.js, Express
- **Baza danych**: MongoDB

## Instalacja

Aby uruchomić aplikację lokalnie, wykonaj poniższe kroki:

1. **Sklonuj repozytorium**:

    ```bash
    git clone https://github.com/TwojUzytkownik/task-manager.git
    ```

2. **Przejdź do katalogu projektu**:

    ```bash
    cd task-manager
    ```

3. **Zainstaluj zależności**:

    ```bash
    npm install
    ```

4. **Skonfiguruj plik `.env`**:

    Utwórz plik `.env` w głównym katalogu projektu i dodaj następujące zmienne środowiskowe:

    ```env
    MONGODB_URI=<TwojMongoDBURI>
    JWT_SECRET=<TwojeTajneHasloJWT>
    PORT=<PortNaKtorymMaDzialacAplikacja>
    ```

5. **Uruchom aplikację**:

    ```bash
    npm start
    ```

Aplikacja będzie dostępna pod adresem `http://localhost:<PORT>`.

## Testowanie

Aby uruchomić testy jednostkowe, wykonaj poniższe polecenie:

```bash
npm test
