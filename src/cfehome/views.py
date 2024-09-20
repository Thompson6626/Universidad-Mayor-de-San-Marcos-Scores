from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.core.paginator import Paginator
from django.db import connection
from django.urls import reverse
import json
from .utils import transformQuestion

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
DEFAULT_QUERY = f"SELECT * FROM people_person WHERE fecha = '{DEFAULT_DATE}'"

def home_page_view(request: HttpRequest):

    rows_per_page = request.GET.get('show',DEFAULT_ROWS_PER_PAGE)
    page_number = request.GET.get('page',1)
    query = request.GET.get('q',None)

    with connection.cursor() as cursor:
        # Use the default query if no query is provided
        cursor.execute(query if query else DEFAULT_QUERY)
        result = cursor.fetchall()  # Fetch all results

    # Create the people list and headers based on the fetched results
    people_list = [dict(zip([col[0] for col in cursor.description], row)) for row in result]
    headers = HEADERS if query is None else [col[0] for col in cursor.description]

    # Set up pagination (15 persons per page, you can adjust the number)
    paginator = Paginator(people_list, rows_per_page)  # Show 10 persons per page
    people_page = paginator.get_page(page_number)  # Get the persons for the current page

    context = {
        'people_page': people_page,
        'rows_per_page': rows_per_page,
        'headers': headers,
        'query': query
    }

    return render(request , 'table_content.html',context)


def transform_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('message')

        query = transformQuestion(question)
        url = reverse('home_page')  # Get the URL of the 'new_page' view

        query_params = f'?q={query}'
        return HttpResponse(f'{url}{query_params}')

    return JsonResponse({'status': 'fail', 'message': 'Invalid request'}, status=400)



