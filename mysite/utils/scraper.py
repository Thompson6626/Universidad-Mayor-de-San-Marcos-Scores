import requests
from bs4 import BeautifulSoup
from people.models import Person
import time
import random

ADDED_LEN = len(".html")
START_INDEX = len("./A")
HEADERS = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
   }

def scrape_and_save(url):
    if Person.objects.filter(source_url = url).exists():
        return Person.objects.filter(source_url = url)
    
    BASE_URL = url[:-ADDED_LEN]

    soup = ""
    with requests.get(url,headers= HEADERS,timeout=100) as response:
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

    all_tds = soup.find_all("td", class_="text-center")

    curso_ref = {}
    
    for row in all_tds:
        a_tags = row.find_all('a')
        for a in a_tags:
            curso_ref[a.get_text()] = a.get('href')

    data = []

    queue = []
    for val in curso_ref.values():
        results_url = f"{BASE_URL}{val[START_INDEX:]}"

        with requests.get(results_url,headers= HEADERS,timeout=100) as results_page:
            results_page.encoding = 'utf-8'  
            in_soup = BeautifulSoup(results_page.text, "html.parser")

            queue.append(in_soup.select("tbody tr"))

    for trs in queue:
        for tr in trs:
            tds = tr.find_all("td")
            td_texts = [td.get_text() for td in tds]
            td_texts.append(url)
            data.append(td_texts)

    for d in data:
        Person.objects.create(
                codigo = d[0],
                apellidos_y_nombres = d[1],
                carrera_primera_opcion = d[2],
                puntaje = d[3] if d[3] != '\xa0' else None,
                merito = d[4] if d[4] != '\xa0' else None,
                observacion = d[5] if d[5] != '\xa0' else "PRESENTE",
                carrera_segunda_opcion = d[6] if d[6] != '\xa0' else None,
                source_url = d[7]
            )

    return Person.objects.filter(source_url=url)
