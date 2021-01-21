from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from multiprocessing import Pool
from os import system
from colorama import Fore, init
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from time import sleep

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
    split_for_db(modelo, url)
    
        

def connect_db():
    try:
        global con
        con = sqlite3.connect('database.db')
        print(Fore.RESET + "[" + Fore.MAGENTA + "*" + Fore.RESET + "] Conectando a la base de datos...")
        table_db()
    except Error:
        print(Error)

def table_db():
    global cursorObj
    cursorObj = con.cursor()
    try:
        cursorObj.execute("CREATE TABLE sneakers(id integer PRIMARY KEY, marca text, modelo text, url text)")
        con.commit()
        print(Fore.RESET + "[" + Fore.MAGENTA + "*" + Fore.RESET + "] Creando base de datos...")
    except Error:
        print(Fore.RESET + "[" + Fore.MAGENTA + "*" + Fore.RESET + "] Base de datos OK...")

def insert_db(marca, modelo, url):
    argumentos = ("NULL", marca, modelo, url)
    cursorObj.execute('''INSERT INTO sneakers(id, marca, modelo, url) VALUES(?, ?, ?, ?)''', argumentos)
    con.commit()

def split_for_db(modelo, url):
    for i in range(len(modelo)):
        marca = str(modelo[i].split(" ")[0])
        insert_db(marca, modelo, url)
    print(marca)
    print(modelo)
    print(url)
    


if __name__ == "__main__":
    connect_db()
    run_tor()
    read_file()
    with Pool(5) as p:
        print(p.map(main, urls_list))