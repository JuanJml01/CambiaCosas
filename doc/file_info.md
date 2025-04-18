# Documentación para la función `get_file_info`
## Función: `get_file_info(file_path)`
Obtiene información sobre un archivo.
### Parámetros:
-   `file_path` (str): La ruta al archivo.
### Retorna:
Un diccionario que contiene información del archivo, incluyendo:
-   `name` (str): El nombre del archivo sin la ruta.
-   `metadata` (dict): Un diccionario que contiene metadatos del archivo (tamaño, fecha de modificación, tipo de archivo).
-   `full_path` (str): La ruta absoluta al archivo.
-   `content` (str): El contenido del archivo como una cadena de texto.
-   `line_count` (int): El número de líneas en el archivo.
### Errores (Raises):
-   `FileNotFoundError`: Si el archivo no existe.
-   `PermissionError`: Si el archivo no se puede leer debido a permisos.
-   `Exception`: Para otros errores inesperados durante el procesamiento del archivo.
### Ejemplo:
```python
from src.cambiacosas.administracion_archivo.file_info import get_file_info

file_path = "mi_archivo.txt"  # Reemplaza con la ruta real del archivo
try:
    file_info_dict = get_file_info(file_path)
    print(file_info_dict)
except FileNotFoundError:
    print(f"Archivo no encontrado: {file_path}")
except PermissionError:
    print(f"Permiso denegado para leer el archivo: {file_path}")
except Exception as e:
    print(f"Ocurrió un error: {e}")
```
