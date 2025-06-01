import logging
import random
import sys
import time

import requests
import json

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create console handler and set level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

# Optionally add file handler to save logs to a file
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def get_captcha_code():
    """
    Wysyła żądanie POST w celu wygenerowania CAPTCHA i zwraca kod z odpowiedzi.
    """
    logger.info("Rozpoczęcie generowania kodu CAPTCHA")
    url = "https://testnr.org/numer/api/generate-captcha"

    headers = {
        "accept": "*/*",
        "accept-language": "pl-PL,pl;q=0.9",
        "content-type": "application/json",
        "sec-ch-ua": "\"Brave\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        # Pamiętaj, aby zaktualizować 'connect.sid' jeśli jest to konieczne
        # lub obsłużyć logowanie/sesję w bardziej dynamiczny sposób.
        "cookie": "connect.sid=s%3ANTd_KxZdUktdrvPNCU2xSrxUzq1tuLqD.w5aoTLN2iNkOd2EJpadnnq%2BL8BZMHrtuIy3jeLpQERg",
        "Referer": "https://testnr.org/numer/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    # Ciało żądania jest puste (null), więc nie przekazujemy parametru 'data' ani 'json'
    # dla metody POST, jeśli serwer oczekuje pustego ciała.
    # Jeśli serwer oczekuje jawnie "null" jako JSON, można użyć json.dumps(None).
    # W tym przypadku, ponieważ content-type to application/json, a body to null,
    # requests.post bez `data` lub `json` powinno wysłać puste ciało.
    # Jeśli serwer wymaga dokładnie `{"body": null}` w JSON, to trzeba by to ustawić.
    # Bazując na oryginalnym `fetch` z `body: null`, puste ciało jest najbardziej prawdopodobne.

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Rzuci wyjątkiem dla kodów błędów HTTP (4xx lub 5xx)

        # Próba sparsowania odpowiedzi jako JSON
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            logger.error("Odpowiedź serwera nie jest poprawnym formatem JSON.")
            logger.error(f"Treść odpowiedzi: {response.text}")
            return None

        # Sprawdzenie, czy pole 'code' istnieje w odpowiedzi
        if "code" in response_data:
            captcha_code = response_data["code"]
            captcha_token = response_data.get("token", None)
            logger.info(f"Pomyślnie wygenerowano kod CAPTCHA: {captcha_code}")
            return captcha_token, captcha_code
        else:
            logger.error("Pole 'code' nie zostało znalezione w odpowiedzi serwera.")
            logger.error(f"Otrzymane dane: {response_data}")
            return None

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Błąd HTTP: {http_err}")
        logger.error(f"Treść odpowiedzi: {response.text if 'response' in locals() else 'Brak odpowiedzi'}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Błąd połączenia: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Przekroczono czas oczekiwania na odpowiedź: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Wystąpił nieoczekiwany błąd żądania: {req_err}")

    return None

def validate_numer(numer_value, phone_value, captcha_token_value, captcha_code_value):
    """
    Wysyła żądanie POST w celu walidacji numeru wraz z danymi CAPTCHA.
    Zwraca odpowiedź serwera w formacie JSON lub None w przypadku błędu.
    """
    logger.info(f"Rozpoczęcie walidacji numeru: {numer_value}, telefon: {phone_value}")
    url = "https://testnr.org/numer/api/validate-numer"

    headers = {
        "Accept": "*/*",
        "Accept-Language": "pl-PL,pl;q=0.9",
        "Connection": "keep-alive", # Dodano z cURL
        "Content-Type": "application/json",
        # Pamiętaj, aby zaktualizować 'connect.sid' jeśli jest to konieczne
        "Cookie": "connect.sid=s%3ANTd_KxZdUktdrvPNCU2xSrxUzq1tuLqD.w5aoTLN2iNkOd2EJpadnnq%2BL8BZMHrtuIy3jeLpQERg", # Przykładowe ciasteczko, upewnij się, że jest takie samo lub zarządzane dynamicznie
        "Origin": "https://testnr.org", # Dodano z cURL
        "Referer": "https://testnr.org/numer/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Sec-GPC": "1", # Dodano z cURL (było GPC, nie gpc)
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36", # Dodano z cURL
        "sec-ch-ua": "\"Brave\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }

    payload = {
        "captchaCode": str(captcha_code_value),
        "captchaToken": str(captcha_token_value),
        "numer": str(numer_value),
        "phone": str(phone_value),
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Rzuci wyjątkiem dla kodów błędów HTTP (4xx lub 5xx)

        try:
            response_json = response.json()  # Zwraca sparsowaną odpowiedź JSON
            logger.info("Pomyślnie zwalidowano numer")
            logger.debug(f"Odpowiedź serwera: {response_json}")
            return response_json
        except json.JSONDecodeError:
            logger.error("Odpowiedź serwera (validate-numer) nie jest poprawnym formatem JSON.")
            logger.error(f"Treść odpowiedzi: {response.text}")
            return {"raw_response": response.text, "error": "Invalid JSON response"}


    except requests.exceptions.HTTPError as http_err:
        logger.error(f"Błąd HTTP (validate-numer): {http_err}")
        logger.error(f"Treść odpowiedzi: {response.text if 'response' in locals() else 'Brak odpowiedzi'}")
    except requests.exceptions.ConnectionError as conn_err:
        logger.error(f"Błąd połączenia (validate-numer): {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logger.error(f"Przekroczono czas oczekiwania na odpowiedź (validate-numer): {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Wystąpił nieoczekiwany błąd żądania (validate-numer): {req_err}")

    return None

if __name__ == "__main__":
    while True:
        logger.info("Rozpoczęcie wykonania programu")
        try:
            numer = random.randint(10**15, (10**16)-1)
            phone = random.randint(100_000_000, 999_999_999)

            logger.debug(f"Wygenerowano losowy numer: {numer}, telefon: {phone}")

            captcha_result = get_captcha_code()
            if captcha_result:
                result = validate_numer(numer, phone, *captcha_result)
                if result:
                    logger.info(f"Wynik walidacji: {result}")
                else:
                    logger.warning("Walidacja nie powiodła się")
            else:
                logger.warning("Nie udało się wygenerować kodu CAPTCHA")
        except Exception as e:
            logger.critical(f"Wystąpił nieoczekiwany błąd: {e}", exc_info=True)
        finally:
            logger.info("Zakończenie wykonania programu")

        time.sleep(1)
