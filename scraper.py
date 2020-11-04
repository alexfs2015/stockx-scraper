import requests
from bs4 import BeautifulSoup
from bing_image_downloader import downloader

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}

url = "https://stockx.com/retro-jordans/air-jordan-1?page=1"

models = []
for i in range(0, 26):
  url_search = url[:-1]
  url_search = url_search + str(i)
  r = requests.get(url_search, headers=headers)
  soup = BeautifulSoup(r.text, 'html.parser')

  for h in soup.find_all(class_="css-1iephdx e1inh05x0"):
    a = h.text
    models.append(a)
    downloader.download(a, limit=100,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60)

print(len(models))
