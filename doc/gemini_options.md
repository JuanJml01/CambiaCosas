# Documentación para la Clase GeminisOptions
## Descripción General
La clase `GeminisOptions` se encuentra en el archivo `src/cambiacosas/googleapi/gemini_options.py` y tiene como objetivo centralizar y configurar las diversas opciones necesarias para interactuar con la API Gemini de Google. Esta clase facilita la configuración de parámetros como la clave de API, el modelo Gemini a utilizar, la construcción de la URL de la API, las cabeceras HTTP necesarias y el cuerpo de las solicitudes que se enviarán a la API.
Su diseño modular permite una gestión clara y organizada de todas las opciones, simplificando la interacción con la API Gemini y promoviendo la reutilización de la configuración en diferentes partes del código.
## Clases de Excepción
### `GeminiOptionsError`
- **Descripción:** Clase base para excepciones específicas de la configuración de las opciones de Gemini. Cualquier error derivado de la configuración de las opciones de la API de Gemini debe ser una instancia de esta clase o una de sus subclases.
### `GeminiAPIKeyError`
- **Descripción:** Subclase de `GeminiOptionsError` utilizada específicamente para señalar errores relacionados con la clave de la API de Gemini. Esta excepción se lanza cuando la clave de la API no está configurada correctamente o no se puede acceder a ella, por ejemplo, si la variable de entorno `GEMINI_API_KEY` no está definida.
## Clase `GeminisOptions`
### Constructor `__init__`
```python
def __init__(self):
```
- **Descripción:** Inicializa una nueva instancia de la clase `GeminisOptions`. Durante la inicialización, se configuran los siguientes atributos:
- `api_key`: La clave de la API se obtiene de la variable de entorno `GEMINI_API_KEY`. Si esta variable no está definida, se lanza una excepción `GeminiAPIKeyError` para indicar una configuración incorrecta.
- `model_id`: El modelo predeterminado se establece en `"gemini-2.0-flash"`.
- `url`: Se construye la URL base para interactuar con la API de Gemini, utilizando el `model_id` y la `api_key` configurados.
- `headers`: Se definen las cabeceras HTTP necesarias para las solicitudes a la API, específicamente `{"Content-Type": "application/json"}` para indicar que los datos se enviarán en formato JSON y se espera que se reciban en este mismo formato.
- `method`: El método HTTP predeterminado para las solicitudes se establece en `"POST"`.
- `body`: Se define la estructura del cuerpo de la solicitud en formato JSON, incluyendo los campos necesarios para interactuar con la API de Gemini. Este cuerpo incluye secciones para:
- `contents`: Define el contenido principal de la solicitud, incluyendo el rol del usuario y la parte de texto que contiene la consulta. Inicialmente, el texto de entrada se establece en `"INSERT_INPUT_HERE"`, que debe ser reemplazado dinámicamente antes de realizar la solicitud.
- `systemInstruction`: Permite incluir instrucciones a nivel de sistema para la API, aunque inicialmente está vacío.
- `generationConfig`: Configura parámetros para la generación de contenido, como el tipo MIME de respuesta esperado (`"application/json"`) y el esquema de respuesta esperado.
- **Excepciones:**
- `GeminiAPIKeyError`: Se lanza si la variable de entorno `GEMINI_API_KEY` no está configurada.
### Método `set_input_text`
```python
def set_input_text(self, input_text):
```
- **Descripción:** Permite modificar el texto de entrada que se enviará a la API de Gemini. Este método es esencial para actualizar la consulta del usuario antes de realizar una solicitud a la API.
- **Parámetros:**
- `input_text` (str): El nuevo texto de entrada que se establecerá para la solicitud.
- **Excepciones:**
- `GeminiOptionsError`: Se lanza si ocurre un error al intentar establecer el texto de entrada.
### Método `set_model`
```python
def set_model(self, model):
```
- **Descripción:** Permite cambiar el modelo Gemini que se utilizará para las solicitudes a la API. Al cambiar el modelo, la URL de la API también se actualiza para reflejar el nuevo modelo seleccionado. Además, este método ajusta la configuración de `responseMimeType` y `responseSchema` basándose en el modelo seleccionado, adaptándose a las características específicas de cada modelo Gemini.
- **Parámetros:**
- `model` (str): El ID del modelo Gemini que se utilizará (p. ej., `"gemini-2.0-flash"`).
- **Excepciones:**
- `GeminiOptionsError`: Se lanza si ocurre un error al intentar establecer el modelo.
### Método `set_response_schema`
```python
def set_response_schema(self, response_schema):
```
- **Descripción:** Permite definir o modificar el esquema de respuesta esperado de la API de Gemini. Este método es útil cuando se espera una respuesta con un formato JSON específico y se desea validar o procesar la respuesta basándose en un esquema predefinido.
- **Parámetros:**
- `response_schema` (dict): Un diccionario que representa el esquema de respuesta esperado en formato JSON Schema.
- **Excepciones:**
- `GeminiOptionsError`: Se lanza si ocurre un error al intentar establecer el esquema de respuesta.
### Método `set_system_instruction`
```python
def set_system_instruction(self, system_instruction):
```
- **Descripción:** Permite establecer instrucciones a nivel de sistema para la API de Gemini. Estas instrucciones pueden influir en el comportamiento de la API y en el tipo de respuestas generadas.
- **Parámetros:**
- `system_instruction` (str): Las instrucciones del sistema en formato de cadena de texto.
- **Excepciones:**
- `GeminiOptionsError`: Se lanza si ocurre un error al intentar establecer las instrucciones del sistema.
---
Esta documentación proporciona una visión completa de la clase `GeminisOptions` y sus métodos, facilitando su uso y comprensión dentro del proyecto.
