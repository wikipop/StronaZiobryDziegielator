# TestNr.org - Narzędzie do Walidacji Numerów

## Opis
Ten projekt to narzędzie edukacyjne, które demonstruje interakcję z API strony TestNr.org. Skrypt wysyła zapytania do serwera, który generuje kod CAPTCHA i przesyła go do klienta (XDDD), a następnie wykorzystuje ten kod do walidacji losowo wygenerowanych numerów.

![image](https://github.com/user-attachments/assets/a12f54a1-e11f-4ff7-be57-7de691854eb9)

## Czym jest testnr.org?

Strona https://testnr.org/numer/ to narzędzie do weryfikacji numerów zaświadczeń o prawie do głosowania w wyborach w Polsce, stworzone przez Stowarzyszenie Ruch Kontroli Wyborów. Służy do sprawdzania, czy zaświadczenie nie było użyte wielokrotnie. Użytkownik podaje numer zaświadczenia i telefonu; aplikacja pokazuje, czy jest nieużywane (zielony komunikat) czy użyte (czerwony). Nie wymaga PESEL, zgodna z RODO. Nie jest oficjalnym narzędziem państwowym, hosting w Islandii budzi pytania o wiarygodność.

## Funkcjonalność
- Generowanie losowych numerów i numerów telefonów
- Pobieranie kodów CAPTCHA z serwera TestNr.org
- Walidacja numerów z wykorzystaniem otrzymanych kodów CAPTCHA
- Szczegółowe logowanie wszystkich operacji

## Uwaga
Ten projekt został stworzony wyłącznie do celów edukacyjnych i służy do nauki:
- Interakcji z zewnętrznym API
- Obsługi zapytań HTTP w Pythonie
- Przetwarzania odpowiedzi JSON
- Implementacji mechanizmów CAPTCHA
- Obsługi błędów i logowania

## Jak to działa
1. Skrypt wysyła zapytanie do API w celu wygenerowania kodu CAPTCHA
2. Serwer zwraca kod CAPTCHA oraz token
3. Skrypt wykorzystuje otrzymany kod i token do walidacji losowo wygenerowanych numerów
4. Cały proces jest powtarzany w nieskończonej pętli z jednosekundowym opóźnieniem

## Wymagania
- Python 3.x
- Biblioteka requests
- Dostęp do internetu

## Zastrzeżenie
Ten projekt służy wyłącznie do celów edukacyjnych. Autor nie ponosi odpowiedzialności za niewłaściwe wykorzystanie tego narzędzia.
