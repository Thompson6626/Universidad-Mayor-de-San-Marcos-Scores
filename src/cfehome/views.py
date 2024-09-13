from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
from people.models import Person

import polars as pl

HEADERS = [
    "Codigo",
    "Apellidos y Nombres",
    "Carrera Primera Opción",
    "Puntaje",
    "Merito",
    "Observación",
    "Carrera Segunda Opción"
]

DEFAULT_ROWS_PER_PAGE = 15

@csrf_exempt
def home_page_view(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        return redirect(f'fetch?url={url}')

    return HttpResponse(render(request, 'home.html'))


def table_data_view(request):
    url = request.GET.get('url')
    
    if url:
        #people = scrape_and_save(url)  
        
        show = request.GET.get('show',DEFAULT_ROWS_PER_PAGE)
        page_number = request.GET.get('page',1)  

        paginator = Paginator(people, show)  

        page_obj = paginator.get_page(page_number)  

        return render(request,'table.html', {
            'headers': HEADERS,
            'paginator': paginator,
            'people_page':page_obj,
            'url': url,
            'show': show
        })

def fetch_data(request):
    page = request.GET.get('page', 1)
    show = request.GET.get('show', DEFAULT_ROWS_PER_PAGE)

    sort_column = request.GET.get('sort', None)
    sort_order = request.GET.get('order', 'asc')

    people = Person.objects.all()

    if sort_column:
        if sort_order == 'desc':
            sort_column = f'-{sort_column}'  
        people = people.order_by(sort_column)


    paginator = Paginator(people, show)
    people_page = paginator.get_page(page)

    table_html = render_to_string('table_content.html', {'people_page': people_page})
    pagination_html = render_to_string('pagination_content.html', {'people_page': people_page})

    return JsonResponse({
        'table_html': table_html,
        'pagination_html': pagination_html
    })