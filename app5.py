import requests
from bs4 import BeautifulSoup
import re
import os

# Url onde vamos fazer a raspagem de dados
url = "https://www.adorocinema.com/filmes/melhores/"

# Resposta do request para a url
response = requests.get(url)

# Se funcionou cod 200
if response.status_code == 200:
    # Pego o conteudo da resposta e faço um Soup com ele usando o html.parser
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Pego elementos que quero da página
    titulos = soup.find_all('a', class_="meta-title-link")
    diretocoes = soup.find_all('a', class_="blue-link")
    # Aqui estou pegando a div inteira que tem o generos
    generos = soup.find_all('div', class_="meta-body-info")
    # url das imagens
    img = soup.find_all('img', class_="thumbnail-img")

    # Tratamento
    gen = []
    for i in generos:
        # Acho todos os valores que sejam span e tenham na classe o texto "ACrl"
        # Esse class foi gerado aleatoriamente
        x = i.findAll('span', class_=re.compile("ACrL", re.I))
        # Inicio um array que armazenará os generos da primeira interação
        y = []
        for j in range(len(x)):
            # Adiciono os generos no array y
            y.append(x[j].text)
        # Adiciono o array y no array gen
        # Estou fazendo isso para garantir que a listas de titulos esteja batendo com a lista dos generos
        gen.append(y)

    # Intero os filmes da url comtitulo, diretor e gêneros
    for i in range(len(titulos)):
        # Transformo os itens do array de gênero em uma string para poder concatenar com as outras
        text_gen = ', '.join(map(str, gen[i]))
        print(titulos[i].text + " // " + diretocoes[i].text + " // " + text_gen)
        # Baixando Imagens dos filmes
        # Estou usando o try except porque o link das imagens estão no atributo src ou data-src
        # Adicionei essa linha apenas para o interpretador não dar avisos
        url_img = ""
        try:
            url_img = img[i]['data-src']
        except KeyError:
            url_img = img[i]['src']
        finally:
            # Baixa o conteudo do request e salva no img_data
            img_data = requests.get(url_img).content

            # Extrai o nome do arquivo da URL
            # imgs é o nome do diretório, é necessário que ele já esteja criado
            # os.path.basename(url_img) pega a parte final da url que eu informei
            # Exemplo: "https://example.com/images/picture.jpg", ele tera o valor picture.jpg
            img_name = os.path.join('imgs', os.path.basename(url_img))

            # Salva a imagem no diretório especificado
            # O with garante que recursos sejam devidamente liberados após seu uso
            # Aqui estou abrindo o arquivo img_name no modo de escrita binaria para salva-lo
            with open(img_name, 'wb') as img_file:
                # aqui estou escrevendo os dados na imagem para salva-la
                img_file.write(img_data)

# Se deu errado cod != 200
else:
    print("Falha, status:{}".format(response.status_code))
