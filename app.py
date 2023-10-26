import logging

from bs4 import BeautifulSoup
from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from flight import Flight

app = FastAPI()
logger = logging.getLogger(__name__)


def get_browser_driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    # options.binary_location = "/snap/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1280,700")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)


def process_html(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('div#vuelos>div>table>tbody')[0].select('tr')
    rows.pop(0)
    flights = []
    for row in rows:
        cols = row.select('td')
        gate = ""
        if len(cols) == 6:
            gate = cols[5].text
        img = cols[0].select('td>img')[0].attrs.get('src', '')
        flights.append(Flight(
            logo=img,
            flight=cols[1].text,
            origin=cols[2].text,
            time=cols[3].text,
            status=cols[4].text,
            gate=gate.strip()
        ))
    return flights


@app.get("/internationals")
async def internationals(option: str):
    browser = get_browser_driver()
    try:

        browser.get(f'https://www.eaai.com.ni/fids/vuelos_dias_fids.php?option={option}')
        # browser.find_element(By.XPATH, '/html/body/form[1]/div/input').click()
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'fids_table'))
        WebDriverWait(browser, 10).until(element_present)
        html = browser.page_source
        flights = process_html(html)
        browser.quit()
        return flights
    except Exception as e:
        browser.quit()
        print(e)


@app.get("/nationals")
async def nationals(option: str):
    browser = get_browser_driver()
    try:
        browser.get(f'https://www.eaai.com.ni/pvnac/vuelos_dias_pvnac.php?option={option}')
        # browser.find_element(By.XPATH, '/html/body/form[1]/div/input').click()
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'pvnac_table'))
        WebDriverWait(browser, 10).until(element_present)
        html = browser.page_source
        flights = process_html(html)
        browser.quit()
        return flights
    except Exception as e:
        browser.quit()
        print(e)
        return f"NO DATA {e}"
