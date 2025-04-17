# src/cambiacosas/googleapi/api_client.py  (ES)
import requests
from src.cambiacosas.googleapi.gemini_options import GeminisOptions, GeminiOptionsError, GeminiAPIKeyError

def call_gemini_api(gemini_config):
    """
    Llama a la API de Google Gemini utilizando la configuración proporcionada.

    Args:
        gemini_config: Un objeto GeminisOptions que contiene la configuración de la API de Gemini.

    Returns:
        Un diccionario que representa los datos de respuesta de la API en caso de éxito.

    Raises:
        GeminiOptionsError: Si hay un error en la configuración de Gemini.
        requests.exceptions.RequestException: Si hay un error durante la solicitud a la API.
    """
    try:
        if not isinstance(gemini_config, GeminisOptions):
            raise GeminiOptionsError("Invalid gemini_config type. Must be a GeminisOptions object.")

        url = gemini_config.url
        headers = gemini_config.headers
        method = gemini_config.method
        body = gemini_config.body

        response = requests.request(method, url, headers=headers, json=body)
        response.raise_for_status() # Lanza HTTPError para respuestas incorrectas (4xx o 5xx)
        return response.json() # O procesa la respuesta según sea necesario

    except GeminiOptionsError as e:
        raise GeminiOptionsError(f"Gemini configuration error: {e}") from e
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"API request failed: {e}") from e
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {e}") from e

def parse_gemini_response(json_response):
   """
   Analiza la respuesta JSON de la API de Gemini para extraer y reconstruir el contenido JSON.

   Args:
       json_response: La respuesta JSON fragmentada de la API de Gemini.

   Returns:
       Una cadena que contiene la respuesta JSON completa con el contenido 'response', o None en caso de error.
   """
   full_response_content = ""
   extracted_json = ""
   try:
       for item in json_response:
           if 'candidates' in item and item['candidates']:
               candidate = item['candidates'][0]
               if 'content' in candidate and candidate['content'] and 'parts' in candidate['content']:
                   for part in candidate['content']['parts']:
                       if 'text' in part:
                           full_response_content += part['text']

       # Intenta extraer JSON si la respuesta es una cadena JSON
       try:
           import json
           start_index = full_response_content.find('{')
           if start_index != -1:
               json_fragment = full_response_content[start_index:]
               extracted_json = json.loads(json_fragment)
               return extracted_json
           else:
               return full_response_content # Devuelve como cadena si no se encuentra JSON
       except json.JSONDecodeError:
           return full_response_content # Devuelve como cadena si falla la decodificación de JSON

   except (TypeError, ValueError, KeyError) as e:
       print(f"Error parsing Gemini response: {e}")
       return None

if __name__ == '__main__':
    # Ejemplo de uso
    fragmented_json_response = [
        {'candidates': [{'content': {'parts': [{'text': '{'}], 'role': 'model'}}], 'usageMetadata': {'promptTokenCount': 10, 'totalTokenCount': 10, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 10}]}, 'modelVersion': 'gemini-2.0-flash'},
        {'candidates': [{'content': {'parts': [{'text': '\n  "'}], 'role': 'model'}}], 'usageMetadata': {'promptTokenCount': 10, 'totalTokenCount': 10, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 10}]}, 'modelVersion': 'gemini-2.0-flash'},
        {'candidates': [{'content': {'parts': [{'text': 'response": "Pale orb in velvet skies,\\nA silent watch with watchful eyes.\\n'}], 'role': 'model'}}], 'usageMetadata': {'promptTokenCount': 10, 'totalTokenCount': 10, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 10}]}, 'modelVersion': 'gemini-2.0-flash'},
        {'candidates': [{'content': {'parts': [{'text': 'Silver beams on sleeping land,\\nA gentle touch, a helping hand."\n}'}], 'role': 'model'}, 'finishReason': 'STOP'}], 'usageMetadata': {'promptTokenCount': 12, 'candidatesTokenCount': 37, 'totalTokenCount': 49, 'promptTokensDetails': [{'modality': 'TEXT', 'tokenCount': 12}], 'candidatesTokensDetails': [{'modality': 'TEXT', 'tokenCount': 37}]}, 'modelVersion': 'gemini-2.0-flash'}
    ]

    parsed_response = parse_gemini_response(fragmented_json_response)
    print("Parsed Response:", parsed_response)
    # Example usage (for testing)
    try:
        gemini_options = GeminisOptions() # Carga las opciones por defecto, y la clave API del entorno
        gemini_options.set_input_text("Escribe un poema corto sobre la luna.")

        api_response = call_gemini_api(gemini_options)
        sd = parse_gemini_response(api_response)
        print(sd)
        print(type(sd))

    except GeminiOptionsError as e:
        print(f"Gemini Options Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"API Request Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")