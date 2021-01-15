from os import system
from colorama import Fore, Style, init
import requests

def main():

    init()
    system("cls")
    try:
        f = open("output.txt")
        option = input(Fore.YELLOW + "Parece que ya tienes un archivo con proxies, ¿quieres usarlo? (y/n)" + Fore.RESET)
        if(option == "y" or "Y"):
            read_file()
        elif(option == "n" or "N"):
            scrape_proxies()
        else:
            system("cls")
            main()
    except IOError:
        scrape_proxies()

def scrape_proxies():
    try:
        print("[" + Fore.MAGENTA + "*" + Fore.RESET + "]" + Fore.GREEN + " Scraping..." + Fore.RESET)
        system("python lib/proxyScraper.py -p http")
        check_proxies()
    except:
        system("python lib/proxyScraper.py -p http")
        check_proxies()

def check_proxies():  
    try:
        print("[" + Fore.MAGENTA + "*" + Fore.RESET + "]" + Fore.GREEN + " Checking..." + Fore.RESET)
        system("python lib/proxyChecker.py -t 20 -s google.com -l output.txt")
        read_file()
    except:
        system("python lib/proxyChecker.py -t 20 -s google.com -l output.txt")
        read_file()

def read_file():
    try:
        f = open('output.txt')
    except:
        print(Fore.RED + "El Archivo 'output.txt' no existe.")
    proxies = f.read().split("\n")
    proxies.pop()
    f.close()

    make_requests(proxies)

def make_requests(proxies_list):
    for i in range(len(proxies_list)):
        proxy_url = "http://" + proxies_list[i]
        proxies = {
            'http':proxy_url,
            'https':proxy_url
            }

        try:
            r = requests.get("https://stockx.com/retro-jordans/air-jordan-1", headers=headers, proxies=proxies)
            print(r.text)
            print(proxies)
        except:
            print("Ha ocurrido un error al enviar la solicitud")
if __name__ == "__main__":
    main()

    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}