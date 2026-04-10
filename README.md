# Centrum Monitoringu Krzysia
Jak uruchomić aplikację
Upewnij się, że masz zainstalowany Docker. W folderze głównym projektu wykonaj:

```
docker-compose up --build
```

Po uruchomieniu kontenerów otwórz w przeglądarce: **http://localhost:8501**.

<img width="901" height="1197" alt="Screenshot_20260329_222525" src="https://github.com/user-attachments/assets/b25846eb-7e5e-40cb-98e6-70f8d1331afc" />

Dane można również przeglądać w formie tabeli
<img width="752" height="400" alt="image" src="https://github.com/user-attachments/assets/f0d9bd66-3faf-4b2e-95ec-4051ceea7dd7" />

Jeśli trzeba, dane można pobrać w formacie CSV
<img width="752" height="468" alt="image" src="https://github.com/user-attachments/assets/762a283d-8e6e-4a12-ba45-4a3db5bbb8d4" />



## Co potrafi system<br>
Przyjmuje, dekoduje i wizualizuje na wykresach telemetrię Krzysia w czasie rzeczywistym (energia, tętno, temperatura, nastrój).

Zapewnia dwustronną łączność poprzez wbudowany czat z symulacją odpowiedzi.

Nieprzerwanie zapisuje historię metryk i wiadomości w bazie danych.

## Wykorzystane technologie
**Streamlit** (Frontend/Backend): Dlaczego Streamlit? Szczerze mówiąc, nie mam żadnego doświadczenia w programowaniu front-endu. Ta biblioteka elegancko rozwiązuje problem, pozwalając na stworzenie reaktywnego interfejsu wyłącznie za pomocą Pythona.

**Protocol Buffers**: (serializacja).

**PostgreSQL**: (broker wiadomości i baza danych).

**Docker i Docker Compose**: (konteneryzacja).

## Architektura projektu
Projekt składa się z 3 izolowanych kontenerów. Dlaczego 3? Uznałem, że to świetna praktyka w zakresie architektury mikroserwisowej. Zamiast złożonych WebSockets w Streamlit, baza danych pełni rolę brokera wiadomości między „kosmosem” (emulatorem) a Ziemią (dashboardem).

### 1. emulator
Imituje komputer pokładowy.

**protobuf_serialization**: Pakuje wygenerowane dane za pomocą Protocol Buffers do formatu binarnego.

**db_write_task**: Łączy się z PostgreSQL i co 2 sekundy wysyła dane binarne do tabeli.

### 2. dashboard
Pełni rolę centrum monitoringu.

**render_telemetry**: Co 2 sekundy pobiera ostatnie pakiety z bazy danych, rozpakowuje je przez Protobuf i aktualizuje wykresy. Aby historia czatu nie migotała podczas odświeżania, użyto dekoratora @st.fragment.

**chat_interface**: Zapisuje wiadomość użytkownika w bazie danych i natychmiast generuje losową odpowiedź w imieniu Krzysia. Historia jest bezpiecznie zapisywana i wczytywana przy ponownym uruchomieniu.


### **Uwaga dotycząca docker-compose.yml**: Tak, mam świadomość, że wpisywanie hasła do bazy danych otwartym tekstem w pliku compose to zła praktyka. Zdecydowałem się jednak nie komplikować rozwiązania – w przeciwnym razie skorzystałbym z Secret Managera lub przeniósł dane uwierzytelniające do pliku .env.
