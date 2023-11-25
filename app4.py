import requests
from bs4 import BeautifulSoup

# Url onde vamos fazer a raspagem de dados
url = "https://quotes.toscrape.com/"

# resposta do request para a url
response = requests.get(url)

# Se funcionou cod 200
if response.status_code == 200:
    # Pego o conteudo da resposta e faço um Soup com ele usando o html.parser
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # acho todas as spans com a class text
    frases = soup.find_all('span', class_="text")
    # acho todos os smalls com a class author
    autores = soup.find_all('small', class_="author")

    # resultados
    for i in range(len(frases)):
        print((autores[i].text, ":", frases[i].text, '\n'))
# Se deu errado cod != 200
else:
    print("Falha, status:{}".format(response.status_code))
