from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.paginator import Paginator

from utils.scraper import scrape_and_save
from django.views.decorators.csrf import csrf_exempt
from people.models import Person

HEADERS = [
    "Codigo",
    "Apellidos y Nombres",
    "Carrera Primera Opción",
    "Puntaje",
    "Merito",
    "Observación",
    "Carrera Segunda Opción"
]

ROWS_PER_PAGE = 15


@csrf_exempt
def home_page_view(request):
    if request.method == 'POST':
        url = request.POST.get('url', '')
        return redirect(f'fetch?url={url}&page=1&show={ROWS_PER_PAGE}')

    return HttpResponse(render(request, 'home.html'))


def table_data_view(request):
    url = request.GET.get('url')
    
    if url:
        people = scrape_and_save(url)  

        show = request.GET.get('show')
        page_number = request.GET.get('page')  

        paginator = Paginator(people, show)  

        page_obj = paginator.get_page(page_number)  

        return render(request,'table.html', {
            'headers': HEADERS,
            'paginator': paginator,
            'people_page':page_obj,
            'url': url,
            'show': show
        })
