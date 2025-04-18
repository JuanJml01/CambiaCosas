# Documentación para la función `modify_file_lines`
## Función: `modify_file_lines(file_path, line_range, new_content)`
Modifica un archivo de texto, reemplazando un rango de líneas especificado con nuevo contenido. Si no se proporciona `line_range`, se modificará el archivo completo.
### Parámetros:
-   `file_path` (str): La ruta al archivo que se va a modificar.
-   `line_range` (tupla o slice, opcional): Una tupla `(start_line, end_line)` o un objeto slice que define el rango de líneas (basado en 1) para reemplazar (inclusivo). Si no se proporciona, se utiliza el rango completo del archivo.
-   `new_content` (str o list de str): El contenido para reemplazar las líneas especificadas.
-   Si es una cadena, se trata como un solo bloque de texto.
-   Si es una lista de cadenas, cada cadena es una línea de nuevo contenido.
### Retorna:
Esta función modifica el archivo en el lugar y no retorna ningún valor.
### Errores (Raises):
-   `FileNotFoundError`: Si el `file_path` especificado no existe.
-   `ValueError`:
-   Si `start_line` > `end_line`.
-   Si los números de línea no son enteros positivos.
-   Si el rango de líneas no es válido para el contenido del archivo.
-   `TypeError`: Si los parámetros son de tipos incorrectos.
### Ejemplo:
```python
from src.cambiacosas.administracion_archivo.edit_file import modify_file_lines

# Ejemplo 1: Reemplazar las líneas 2 a 4 con una sola cadena
modify_file_lines("my_file.txt", (2, 4), "Esta es la nueva línea 2.\nEsta es la nueva línea 3.\nEsta es la nueva línea 4.")

# Ejemplo 2: Reemplazar las líneas 2 a 4 con una lista de cadenas
modify_file_lines("my_file.txt", slice(2, 5), ["Nueva línea 2", "Nueva línea 3", "Nueva línea 4"])

# Ejemplo 3: Reemplazar todo el contenido del archivo
modify_file_lines("my_file.txt", None, "Esto reemplaza todo el contenido del archivo")
```
