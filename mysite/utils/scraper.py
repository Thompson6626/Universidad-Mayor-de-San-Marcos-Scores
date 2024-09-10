import requests
from bs4 import BeautifulSoup
from people.models import Person

def scrape_and_save(url):
    if Person.objects.filter(source_url = url).exists():
        return Person.objects.filter(source_url = url)
    
    ADDED_LEN = len(".html")
    BASE_URL = url[:-ADDED_LEN]
    START_INDEX = len("./A")

    page = requests.get(url)
    page.encoding = 'utf-8'  # Ensure encoding is set correctly

    soup = BeautifulSoup(page.text, "html.parser")

    all_tds = soup.find_all("td", class_="text-center")

    curso_ref = {}
    
    for row in all_tds:
        a_tags = row.find_all('a')
        for a in a_tags:
            curso_ref[a.get_text()] = a.get('href')

    headers = []

    for _, val in curso_ref.items():
        results_url = f"{BASE_URL}{val[START_INDEX:]}"
        results_page = requests.get(results_url)
        results_page.encoding = 'utf-8'  # Ensure encoding is set correctly
        in_soup = BeautifulSoup(results_page.text, "html.parser")

        if not headers:
            thead = in_soup.find("thead")
            tr = thead.find("tr")
            for th in tr.find_all("th"):
                headers.append(th.text)

        tbody = in_soup.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            td_texts = [td.get_text() for td in tds]

            person = Person.objects.create(
                codigo = td_texts[0],
                apellidos_y_nombres = td_texts[1],
                carrera_primera_opcion = td_texts[2],
                puntaje = td_texts[3],
                merito = td_texts[4],
                observacion = td_texts[5],
                carrera_segunda_opcion = td_texts[6],
                source_url = url
            )

    return Person.objects.filter(source_url=url)
