import requests
from bs4 import BeautifulSoup
import polars as pl
import aiohttp
import asyncio
from urllib.parse import urljoin
import os

SCHEMA = {
    "Codigo": pl.Int64,
    "Apellidos y Nombres": pl.Utf8,
    "Carrera Primera Opción": pl.Utf8,
    "Puntaje": pl.Float64,
    "Merito": pl.Utf8,
    "Observación": pl.Utf8,
    "Carrera Segunda Opción": pl.Utf8,
    "Fecha": pl.Utf8,
    "Modalidad de ingreso":pl.Utf8
}

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

FILE_PATH = 'unmsm_results.csv'    

def str_is_float(text:str)->bool:
    return text.replace('.','',1).isdigit()


# Function to fetch HTML content asynchronously
async def fetch_html(session, url):
    try:
        async with session.get(url, headers=REQUEST_HEADERS) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


async def main_scrape(date,url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, url)
        if html is None:
            return  # Returnif there was an error

        soup = BeautifulSoup(html, "html.parser")

        tbody = soup.find("tbody")
        a_tags = tbody.find_all('a')

        for a in a_tags:
            href = a.get('href')
            mod = a.get_text(strip=True)
            full_url = urljoin(url, href)
            await scrape_and_save(session, full_url, date, mod)
            
# Main scraping function
async def scrape_and_save(session,url,date,mod):
    # Fetch the HTML of the initial URL
    html = await fetch_html(session, url)
    if html is None:
        return   # Return if there was an error
    soup = BeautifulSoup(html, "html.parser")

    # Find all <td> elements with the class "text-center" and extract the href attributes from <a> tags
    all_tds = soup.find_all("td", class_="text-center")
    curso_ref = [a.get('href') for td in all_tds for a in td.find_all('a')]

    # Create tasks to fetch HTML content from the referenced URLs
    tasks = [fetch_html(session, urljoin(url, ref)) for ref in curso_ref]
    # Gather all the HTML content from the tasks
    pages = await asyncio.gather(*tasks)

    data = []

    # Process each page's HTML content
    for page in pages:
        if page is None:
            continue  # Skip pages that could not be fetched
        in_soup = BeautifulSoup(page, "html.parser")
        # Get all the tr inside the tbody
        trs = in_soup.select("tbody tr")
        # Extract and clean data from each row
        for tr in trs:
            tds = tr.find_all("td")
            cleaned_texts = []
            # Clean and append text to the cleaned_texts list
            for td in tds:
                text = td.get_text()
                if text == '\xa0' or text == '&nbsp;':
                    cleaned_texts.append(None)
                else:
                    cleaned_texts.append(text.strip())

            # Create a dictionary for each row with headers and URL
            row_data = dict(zip(SCHEMA.keys() , cleaned_texts + [date,mod]))

            if row_data["Puntaje"] is not None and not str_is_float(row_data["Puntaje"]):
                continue  
            data.append(row_data)

    df = pl.DataFrame(data,schema=SCHEMA)
    
    if not df.is_empty():
        df = df.filter(~pl.all_horizontal(pl.all().is_null()))

        df = df.with_columns(
            pl.when(df["Observación"] == "ALCANZO VACANTE")
            .then(pl.lit("ALCANZO VACANTE PRIMERA OPCIÓN"))
            .otherwise(df["Observación"])
            .alias("Observación")
        )

        mode = 'a' if os.path.exists(FILE_PATH) else 'w'
        include = False if os.path.exists(FILE_PATH) else True
        with open(FILE_PATH, mode) as f:
            df.write_csv(f,include_header=include)
    

UNMSM_URL_RESULTS = {
    "2024-I": "https://admision.unmsm.edu.pe/Website20241/",
    "2024-II": "https://admision.unmsm.edu.pe/Website20242/index.html",
}

async def main():
    tasks = [main_scrape(date, url) for date, url in UNMSM_URL_RESULTS.items()]
    await asyncio.gather(*tasks)

asyncio.run(main())