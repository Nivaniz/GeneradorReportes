# GeneradorReportes

Este programa es una aplicación de monitorización de temperaturas que utiliza la biblioteca PySide6 para la interfaz gráfica y PyqtGraph para la visualización de datos en un gráfico en tiempo real. Genera reportes de los datos insertador o autogenerados en pdf o html.


## Características destacadas

- Gráficos en Tiempo Real: Utiliza la biblioteca PyqtGraph para mostrar gráficos en tiempo real de las temperaturas monitoreadas. Cada valor tiene su propia línea de gráfico con colores y símbolos distintivos.
- Tabla de Datos: Muestra una tabla que se actualiza dinámicamente con las temperaturas ingresadas. La tabla tiene una estructura de columnas basada en el número de temperaturas registradas para el valor seleccionado.
- Generación de Informes HTML: Permite generar informes en formato HTML que incluyen tablas con los datos de temperaturas. Se utiliza la biblioteca pandas para manipular datos y Jinja2 para la generación dinámica del informe.
- Exportación a PDF: Facilita la exportación del informe generado en formato PDF. Utiliza la biblioteca pdfkit para convertir el informe HTML a PDF.

## Ventanas

Ventana Principal:
<p align="center">
  <img src="https://github.com/Nivaniz/TableroKanban/blob/main/img/main.png" alt="Main Window" style="width: 50%; max-width: 200px;">
</p>

Archivo que genera de ejemplo:
[Informe PDF](https://github.com/tu-usuario/tu-repositorio/blob/main/ruta-al-archivo/reporte.pdf)

## Ejecución 

Es necesario tener instalado los requerimientos necesarios para ejecutarlo correctamente desde el archivo programa.py

### Instalación

Para poder utilizar el proyecto o modificarlo puedes:

1.- **Clonar el repositorio en tu máquina local:**

2.- **Crea un entorno virtual e instala las dependencias necesarias.**

3.- **Ejecutarlo desde el archivo programa.py o desde el ejecutable adjunto**

4.- Es necesario pre-instalar las dependencias, para la librería import pdfkit es necesario hacer un pip y posteriormente usar:
### Linux: sudo apt-get install wkhtmltopdf
### Windows: https://wkhtmltopdf.org/downloads.html#stable (Descargar y guardar en variables del sistema agregando \bin)
### Reiniciar VSCODE

## Autoría

¡Tus contribuciones son bienvenidas! Si encuentras errores o mejoras para el proyecto, no dudes en enviar tus pull requests. Si tienes alguna pregunta o comentario, puedes encontrarme y visitar mi sitio web https://codingwithnirvana.pythonanywhere.com.

Espero que esta versión del README sea útil.
Creado por **Nirvana Belen González López** 