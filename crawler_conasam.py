from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

chromedriver = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=chromedriver, options=options)

news_data = []

page = 8

MAX_PAGES = 30

while page <= 8*MAX_PAGES:

    NEWS_URL = "https://portal.conasems.org.br/noticias?rows=8&start="+str(page)
    driver.get(NEWS_URL)

    print(f'Page: {page}')
    print(NEWS_URL)

    wait = WebDriverWait(driver, 10)

    if page == 0:

        links = driver.find_elements(By.XPATH, '//a[contains(@class, "w-full") and starts-with(@href, "/noticias/")]')
    else:
        container_xpath = '//*[@id="__next"]/section[5]'
        container = wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        links = container.find_elements(By.XPATH, './/a[starts-with(@href, "/noticias/")]')


    news_links = [link.get_attribute("href") for link in links]

    print(f'Links encontrados: {len(news_links)}')

    for link in news_links:

        print(f'Entra no link: {link}')

        driver.get(link)

        titulo = driver.find_element(By.XPATH, '//*[@id="__next"]/section[3]/div/h1').text

        #data = driver.find_element(By.XPATH,'//*[@id="__next"]/section[4]/div/div/p[2]').text

        content = driver.find_element(By.XPATH,'//*[@id="__next"]/section[4]/div/div/section').text

        print(titulo)
        #print(data)
        print(content)

        news_data.append({"title": titulo, "content": content, "url": link})

        print('\n\n\n\n\n\n\n')

    #for news in news_data:
    #    print("\nTítulo:", news["title"])
    #    print("Conteúdo:", news["content"][:500], "...")
    #    print("Link:", news["url"])

    page+=8

driver.quit()

df = pd.DataFrame(news_data)

df.to_csv("conasam.csv", index=False, encoding="utf-8")
