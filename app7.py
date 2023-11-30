import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px

count = 1
quotes = []
authors = []
felling = []
while True:

    # Url onde vamos fazer a raspagem de dados
    url = "https://quotes.toscrape.com/page/" + str(count) + "/"

    # resposta do request para a url
    response = requests.get(url)

    # Se funcionou cod 200
    if response.status_code == 200:
        # Pego o conteudo da resposta e faço um Soup com ele usando o html.parser
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # verifica a quantidade de
        no_quotes = soup.find_all('div')
        if len(no_quotes) == 8:
            break

        quotes_div = soup.find_all('div', class_="quote")
        for i in quotes_div:
            # # acho todos as quotes com a class text
            quote = (i.find('span', class_="text")).text
            quotes.append(quote)
            # acho todos os smalls com a class author
            author = (i.find('small', class_="author")).text
            authors.append(author)
            # análise da quote
            analise = TextBlob(quote)
            polaridade = analise.sentiment.polarity
            felling.append(polaridade)

        count += 1
    # Se deu errado cod != 2000
    else:
        print("Falha, status:{}".format(response.status_code))

data = {'quotes': quotes, 'authors': authors, 'positividade': felling}
df = pd.DataFrame(data)

# Cria uma instância do aplicativo Dash.
app = Dash(__name__)

# layout onde adicionamos as coisas do dashboard
app.layout = html.Div(children=[
    # H1 html
    html.H1(children='Dataframe de frases'),
    # gráfico feito acima
    html.Div(
        children=[
            # Exibindo o Datatable do dataframe baixado
            dash_table.DataTable(data=df.to_dict('records'), page_size=10),

        ]
    ),
    html.Div(
        children=[
            # exibindo o gráfico do dataframe
            dcc.Graph(
                id="scatter",
                figure={}
            )
        ]
    )
])

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color='petal_length')
fig.show()

if __name__ == '__main__':
    app.run(debug=True)
