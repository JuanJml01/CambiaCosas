# Documentación de la clase GeminisOptions

## Descripción General

La clase `GeminisOptions` se encuentra en el archivo `src/cambiacosas/googleapi/gemini_options.py` y tiene como objetivo centralizar y configurar las diversas opciones necesarias para interactuar con la API de Gemini de Google. Esta clase facilita la configuración de parámetros como la clave de API, el modelo de Gemini a utilizar, la construcción de la URL de la API, las cabeceras HTTP necesarias y el cuerpo de las peticiones que se enviarán a la API.

Su diseño modular permite una gestión clara y organizada de todas las opciones, simplificando la interacción con la API de Gemini y promoviendo la reutilización de la configuración en diferentes partes del código.

## Clases de Excepción

### `GeminiOptionsError`
- **Descripción:** Clase base para las excepciones específicas de la configuración de opciones de Gemini. Cualquier error derivado de la configuración de las opciones de la API de Gemini debería ser una instancia de esta clase o de una de sus subclases.

### `GeminiAPIKeyError`
- **Descripción:** Subclase de `GeminiOptionsError` que se utiliza específicamente para señalar errores relacionados con la clave de API de Gemini. Esta excepción se levanta cuando la clave de API no está correctamente configurada o no se puede acceder a ella, por ejemplo, si la variable de entorno `GEMINI_API_KEY` no está definida.

## Clase `GeminisOptions`

### Constructor `__init__`

```python
def __init__(self):
```

- **Descripción:** Inicializa una nueva instancia de la clase `GeminisOptions`. Durante la inicialización, se configuran los siguientes atributos:
    - `api_key`: Se obtiene la clave de API de la variable de entorno `GEMINI_API_KEY`. Si esta variable no está definida, se levanta una excepción `GeminiAPIKeyError` para indicar que la configuración es incorrecta.
    - `model_id`: Se establece el modelo por defecto a `"gemini-2.0-flash"`.
    - `url`: Se construye la URL base para interactuar con la API de Gemini, utilizando el `model_id` y la `api_key` configurados.
    - `headers`: Se definen las cabeceras HTTP necesarias para las peticiones a la API, específicamente `{"Content-Type": "application/json"}` para indicar que se enviará y se espera recibir datos en formato JSON.
    - `method`: Se establece el método HTTP por defecto para las peticiones como `"POST"`.
    - `body`: Se define la estructura del cuerpo de la petición en formato JSON, incluyendo los campos necesarios para interactuar con la API de Gemini. Este cuerpo incluye secciones para:
        - `contents`: Define el contenido principal de la petición, incluyendo el rol del usuario y la parte del texto que contiene la consulta. Inicialmente, el texto de entrada se establece como `"INSERT_INPUT_HERE"`, que debe ser reemplazado dinámicamente antes de realizar la petición.
        - `systemInstruction`: Permite incluir instrucciones a nivel de sistema para la API, aunque inicialmente se encuentra vacío.
        - `generationConfig`: Configura parámetros para la generación de contenido, como el tipo MIME de la respuesta esperado (`"application/json"`) y el esquema de respuesta esperado.

- **Excepciones:**
    - `GeminiAPIKeyError`: Se levanta si la variable de entorno `GEMINI_API_KEY` no está configurada.

### Método `set_input_text`

```python
def set_input_text(self, input_text):
```

- **Descripción:** Permite modificar el texto de entrada que se enviará a la API de Gemini. Este método es fundamental para actualizar la consulta del usuario antes de realizar una petición a la API.
- **Parámetros:**
    - `input_text` (str): El nuevo texto de entrada que se desea establecer para la petición.
- **Excepciones:**
    - `GeminiOptionsError`: Se levanta si ocurre un error al intentar establecer el texto de entrada.

### Método `set_model`

```python
def set_model(self, model):
```

- **Descripción:** Permite cambiar el modelo de Gemini que se utilizará para las peticiones a la API. Al cambiar el modelo, también se actualiza la URL de la API para reflejar el nuevo modelo seleccionado. Además, este método ajusta la configuración de `responseMimeType` y `responseSchema` en función del modelo seleccionado, adaptándose a las particularidades de cada modelo de Gemini.
- **Parámetros:**
    - `model` (str): El ID del modelo de Gemini que se desea utilizar (ej. `"gemini-2.0-flash"`).
- **Excepciones:**
    - `GeminiOptionsError`: Se levanta si ocurre un error al intentar establecer el modelo.

### Método `set_response_schema`

```python
def set_response_schema(self, response_schema):
```

- **Descripción:** Permite definir o modificar el esquema de respuesta esperado de la API de Gemini. Este método es útil cuando se espera una respuesta con un formato JSON específico y se desea validar o procesar la respuesta basándose en un esquema predefinido.
- **Parámetros:**
    - `response_schema` (dict): Un diccionario que representa el esquema de respuesta esperado en formato JSON Schema.
- **Excepciones:**
    - `GeminiOptionsError`: Se levanta si ocurre un error al intentar establecer el esquema de respuesta.

### Método `set_system_instruction`

```python
def set_system_instruction(self, system_instruction):
```

- **Descripción:** Permite establecer instrucciones a nivel de sistema para la API de Gemini. Estas instrucciones pueden influir en el comportamiento de la API y en el tipo de respuestas generadas.
- **Parámetros:**
    - `system_instruction` (str): Las instrucciones del sistema en formato de cadena de texto.
- **Excepciones:**
    - `GeminiOptionsError`: Se levanta si ocurre un error al intentar establecer las instrucciones del sistema.

---
Esta documentación proporciona una visión completa de la clase `GeminisOptions` y sus métodos, facilitando su uso y comprensión dentro del proyecto.