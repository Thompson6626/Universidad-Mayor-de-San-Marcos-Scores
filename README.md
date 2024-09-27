
<p align="center">
  <a href="https://docs.djangoproject.com/en/5.1/" target="blank"><img src="https://cdn.hashnode.com/res/hashnode/image/upload/v1636780048014/niLN2J80j.png" width="200" alt="Django Logo" /></a>
</p>

## **Proyecto de Puntajes - Universidad Nacional Mayor de San Marcos**

Este proyecto se encarga de extraer los puntajes del examen de admisión de la Universidad Nacional Mayor de San Marcos.
Además tiene una función que te permite hacerle preguntas a una IA , esta IA intenta convertir tus preguntas en consultas para la base de datos y te devuelve los resultados en forma de tabla.
Perfecto para quienes quieren acceder a la información de manera fácil y rápida.

## **Instalación**

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/Thompson6626/Universidad-Mayor-de-San-Marcos-Scores.git
   cd Universidad-Mayor-de-San-Marcos-Scores
   ```
2. **Crear y activar un entorno virtual**:
    ```bash
    # Linux/macOS
    python3 -m venv env
    source env/bin/activate
    
    # Windows
    python -m venv env
    .\env\Scripts\activate
    ```
3. **Instalar las dependencias:**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Ejecutar los siguientes comandos necesarios para la configuración del proyecto**:
   * vendor_pull: Descarga archivos estáticos (CSS, JS) necesarios de Flowbite:
       ```bash
        python manage.py vendor_pull
        ```
   * collectstatic: Recolecta todos los archivos estáticos para su uso en el servidor:
       ```bash
        python manage.py collectstatic --noinput
        ```
   * fetch_scores: Obtiene los puntajes del examen de admisión:
       ```bash
        python manage.py fetch_scores
        ```
   * import_csv: Importa los datos desde un archivo CSV:
       ```bash
       python manage.py import_csv
        ```
5. **Renombrar y configurar el archivo ```.env```**:

    * Cambia el nombre del archivo ```.env.sample``` a ```.env```.
    * En el archivo ```.env```, asegúrate de agregar:
        * La llave secreta de Django (DJANGO_SECRET_KEY).
        * Tu clave API de Groq para poder usar la funcionalidad de AI (API_KEY).
        * Si no tienes una API Key de Groq, ve a [https://console.groq.com/keys](https://console.groq.com/keys) para crear una.

## **Ejecutar el proyecto**:
  * Ejecutar el siguiente comando en la carpeta  ```src```:
  ```bash
python manage.py runserver
  ```
  * Y luego abes tu navegador y vas a http://127.0.0.1:8000/.



