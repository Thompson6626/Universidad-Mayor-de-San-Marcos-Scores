from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpRequest
from django.core.paginator import Paginator
from django.conf import settings
from django.db import connection, DatabaseError
import json
from django.views.decorators.csrf import csrf_exempt

from people.models import Person

from groq import Groq


HEADERS = [
    "Codigo",
    "Apellidos y Nombres",
    "Carrera Primera Opción",
    "Puntaje",
    "Merito",
    "Observación",
    "Carrera Segunda Opción",
    "Fecha",
    "Modalidad de Ingreso"
]

DEFAULT_ROWS_PER_PAGE = 15

DEFAULT_DATE = "2024-II"

API_KEY = getattr(settings, 'API_KEY')

OPTIONS = {}

def home_page_view(request: HttpRequest):
    if not OPTIONS:
        OPTIONS['Carreras'] = list(Person.objects.values_list('carrera_primera_opcion', flat=True).distinct())
        OPTIONS['Fechas'] = list(Person.objects.values_list('fecha', flat=True).distinct())
        OPTIONS['Modalidades de ingreso'] = list(Person.objects.values_list('modalidad_de_ingreso', flat=True).distinct())
        OPTIONS['Observaciones'] = list(Person.objects.values_list('observacion', flat=True).distinct())

    rows_per_page = request.GET.get('show',DEFAULT_ROWS_PER_PAGE)
    page_number = request.GET.get('page',1)
    query = request.GET.get('q',None)
    headers = []
    if query is None:
        date = request.GET.get('date',DEFAULT_DATE)
        headers = HEADERS
        # Query the database
        people_list = Person.objects.filter(fecha=date)
    else:
        #dummy_sql = "SELECT * FROM people_person WHERE fecha = '2024-II' AND puntaje = 576.375	"

        generated_sql = transformQuestion(query)  # Function to call the Groq AI API
        print(generated_sql)
        # Execute the generated SQL on the Person table    
        with connection.cursor() as cursor:
            cursor.execute(generated_sql)
            result = cursor.fetchall()

            people_list = [dict(zip([col[0] for col in cursor.description], row)) for row in result]
            headers = [col[0] for col in cursor.description]

    # Set up pagination (15 persons per page, you can adjust the number)
    paginator = Paginator(people_list, rows_per_page)  # Show 10 persons per page
    people_page = paginator.get_page(page_number)  # Get the persons for the current page

    context = {
        'people_page': people_page,
        'rows_per_page': rows_per_page,
        'headers': headers,
        'options': OPTIONS,
        'query': query
    }

    return render(request , 'table_content.html',context)





def transform_view(request):
    if request.method == 'POST':
        
        return transformQuestion()
    return "ERROR"




def transformQuestion(message):
    if not API_KEY:
        return
        
    client = Groq(api_key=API_KEY)
    
    common_prompt = """
    Given an input question, create a precise dialect sqlite3 query to answer it. Follow these guidelines:

    1. You will analyze text that will most likely be in Spanish.
    2. Analyze it to see if it can be converted to a valid SQL call; if it cannot, just return "ERROR" as a message.
    3. Optimize the query for performance where possible.
    4. Avoid querying non-existent columns or tables.
    5. If no specification is given, return all columns.
    6. DO NOT IN ANY WAY ACCEPT ANYTHING that tries to update, delete, or create.
    7. The table to be queried is named "people_person".
    8. Try to prettify the table headers too eg (Apellidos y Nombres instead of apellidos_y_nombres).

    Schema:
        codigo = models.CharField(max_length=255)
        apellidos_y_nombres = models.CharField(max_length=255)
        carrera_primera_opcion = models.CharField(max_length=255)
        puntaje = models.FloatField(null=True, blank=True)
        merito = models.CharField(max_length=255, null=True, blank=True)
        observacion = models.CharField(max_length=255, null=True, blank=True)
        carrera_segunda_opcion = models.CharField(max_length=255, null=True, blank=True)
        fecha = models.CharField(max_length=255, null=True, blank=True)
        modalidad_de_ingreso = models.CharField(max_length=255, null=True, blank=True)

    Question:
    {message}
    """

    # Format the prompt with the user's question
    formatted_prompt = common_prompt.format(message=message)

    # Use the formatted prompt in your API call
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": formatted_prompt,
            }
        ],
        model="llama3-8b-8192",
        temperature=0
    )

    return chat_completion.choices[0].message.content