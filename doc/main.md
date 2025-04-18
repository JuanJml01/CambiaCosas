# Documentación para la función `main` en `__main__.py`
## Función: `main()`
Esta es la función principal de la herramienta `cambiacosas`. Utiliza `argparse` para analizar los argumentos de la línea de comandos, escanea una carpeta especificada y procesa los archivos que contiene utilizando la API de Gemini.

### Parámetros:
La función `main()` utiliza `argparse` para definir los siguientes argumentos de línea de comandos:

-   `folder_name` (str): La ruta a la carpeta que contiene los archivos que se van a procesar. Este argumento es obligatorio.
-   `prompt_file` (str): La ruta al archivo que contiene el prompt de procesamiento que se utilizará con la API de Gemini. Este argumento es obligatorio.
-   `--divide` (bool, opcional): Un indicador opcional que, cuando se proporciona, divide los archivos grandes (con más de 300 líneas) en archivos de fragmentos procesados separados en lugar de fusionarlos en un solo archivo.

### Retorna:
Esta función no devuelve ningún valor directamente. Imprime la salida a la consola y sale con un código de estado.

-   Imprime mensajes informativos sobre el proceso de escaneo de la carpeta, el procesamiento de archivos y cualquier error que ocurra.
-   Sale con un código de estado 1 si ocurre un error, y 0 si la ejecución se completa con éxito.

### Uso:
Ejecute la herramienta desde la línea de comandos con los argumentos requeridos y opcionales:
```bash
python -m cambiacosas <folder_name> <prompt_file> [--divide]
```
Reemplace `<folder_name>` con la ruta a la carpeta que contiene los archivos que se van a procesar.
Reemplace `<prompt_file>` con la ruta al archivo que contiene el prompt de procesamiento.
Opcionalmente, agregue `--divide` para dividir los archivos grandes en fragmentos.

### Ejemplo:
```bash
python -m cambiacosas mi_carpeta prompt.txt --divide
```
En este ejemplo:
-   `mi_carpeta` es la carpeta que se va a escanear.
-   `prompt.txt` es el archivo que contiene el prompt para la API de Gemini.
-   `--divide` indica que los archivos grandes deben dividirse en fragmentos.

**Salida Esperada:**
La salida esperada incluye mensajes informativos sobre el escaneo de la carpeta, el procesamiento de archivos y cualquier error que ocurra durante el proceso. La salida real dependerá de los archivos en la carpeta especificada y del contenido del archivo de prompt.
