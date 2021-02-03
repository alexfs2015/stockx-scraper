from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
from os import system
from colorama import Fore, init
from bs4 import BeautifulSoup
from time import sleep
import sqlite3

def main(url):
    proxy = my_proxy("127.0.0.1", 9050)
    proxy.get(url)
    html = proxy.page_source
    scrape_name_url(html)
    switchIP()

def switchIP():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def my_proxy(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    fp.update_preferences()
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=fp)

def read_file():
    init()
    global urls_list
    path_txt = input(Fore.YELLOW + "Introduce la ruta del archivo de urls: " + Fore.RESET)
    my_file = open(path_txt, "r")
    content = my_file.read()
    urls_list = content.split("\n")
    my_file.close()
    print(urls_list)

def run_tor():
    system("start C:\\Users\\2004a\\AppData\\Roaming\\tor\\Tor\\tor.exe")
    print(Fore.RESET + "[" + Fore.MAGENTA + "*" + Fore.RESET + "] Iniciando tor...")
    sleep(3)

def scrape_name_url(html):
    soup = BeautifulSoup(html, 'lxml')
    model = soup.findAll("div", class_="css-wthos8-TileBody e1b7sao0")
    modelo = []
    for i in model:
        modelo.append(i.find('div').text)
    link = soup.findAll('div', class_="tile css-yrcab6-Tile e1yt6rrx0")
    url = []
    for i in link:
        url.append(i.find('a').get('href'))
    print(modelo)
    print(url)

    for i in range(len(modelo)):
        scrape_image(url[i],modelo[i])

def scrape_image(url, modelo):
    url = "https://stockx.com/" + url
    proxy = my_proxy("127.0.0.1", 9050)
    proxy.get(url)
    html = proxy.page_source

    soup = BeautifulSoup(html, 'lxml')
    if soup.find("div", {"class":"rc-slider-handle"}):
        insert_in_sql_slider(modelo)
        get_url_slider(url, html)
    else:
        insert_in_sql_no_slider(modelo)

def insert_in_sql_no_slider(modelo):
    marca = str(modelo.split(" ")[0])
    modelo = str(modelo)
    entities = (marca, modelo, 0)

    con = sqlite3.connect('database.db')
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO sneakers(Marca, Modelo, Slider) VALUES(?, ?, ?)''', entities)    
    con.commit()

def insert_in_sql_slider(modelo):
    marca = str(modelo.split(" ")[0])
    modelo = str(modelo)
    entities = (marca, modelo, 1)

    con = sqlite3.connect('database.db')
    cursorObj = con.cursor()
    cursorObj.execute('''INSERT INTO sneakers(Marca, Modelo, Slider) VALUES(?, ?, ?)''', entities)    
    con.commit()

def get_url_slider(url, html):
    soup = BeautifulSoup(html, 'lxml')
    image_src = soup.find("img", {"data-testid":"product-detail-image"})['src']
    
    image_src = image_src[:-60]
    for i in range(100):
        image_src = image_src[:-5]
        image_src = image_src + str(i).zfill(2)
        
        proxy = save_image("127.0.0.1", 9050)
        proxy.get(image_src)
        
def save_image(PROXY_HOST,PROXY_PORT):
    fp = webdriver.FirefoxProfile()
    # Direct = 0, Manual = 1, PAC = 2, AUTODETECT = 4, SYSTEM = 5
    fp.set_preference("network.proxy.type", 1)
    fp.set_preference("network.proxy.socks",PROXY_HOST)
    fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))
    fp.update_preferences()
    options = Options()
    options.headless = True
    return webdriver.Firefox(options=options, firefox_profile=fp)

if __name__ == "__main__":
    run_tor()
    read_file()
    with Pool(5) as p:
        print(p.map(main, urls_list))