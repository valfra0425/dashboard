import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px

# Contador usado para atualizar a url
count = 1
# Arrays onde vou armazenar valores da raspagem de dados
quotes = []
authors = []
positivity = []
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

        # verifica a quantidade de divs
        # observando a página web eu notei que quando se tem apenas 8 divs a paginação acaba
        no_quotes = soup.find_all('div')
        if len(no_quotes) == 8:
            break

        # divs com quotes
        quotes_div = soup.find_all('div', class_="quote")
        for i in quotes_div:
            # acho todos as quotes com a class text e adiciono no array
            quote = (i.find('span', class_="text")).text
            quotes.append(quote)
            # acho todos os smalls com a class author e adiciono no array
            author = (i.find('small', class_="author")).text
            authors.append(author)
            # análise da quote usando o TextBlob
            analise = TextBlob(quote)
            polaridade = analise.sentiment.polarity
            positivity.append(polaridade)

        count += 1
    # Se deu errado cod != 2000
    else:
        print("Falha, status:{}".format(response.status_code))

# criação de um dataframe com os dados raspados
data = {'quotes': quotes, 'authors': authors, 'positividade': positivity}
df = pd.DataFrame(data)

# conseguindo a media da positividade das frases de cada author
df_group = df.groupby("authors")["positividade"].mean().reset_index()
# conseguindo a contagem de quoutes de cada author
df_group["count"] = (df.groupby("authors")["quotes"].count().reset_index())["quotes"]

# gráfico
fig = px.scatter(df_group, x="positividade", y="authors", color='positividade', hover_data=["count"],
                 hover_name="authors", height=500)
# tirando visibilidade do eixo y
fig.update_layout(yaxis=dict(visible=False))
# atualiza tamanho dos pontos
fig.update_traces(marker=dict(size=10))

# histograma
fig2 = px.histogram(df, x="positividade", range_x=[-1, 1])

# Cria uma instância do aplicativo Dash.
app = Dash(__name__)

# layout onde adicionamos as coisas do dashboard
app.layout = html.Div(className="main_container", children=[
    # H1 html
    html.H1(className="center", children='Dashboard dos resultados da raspagem de dados do site'
                                         ' https://quotes.toscrape.com'),
    # gráfico feito acima
    html.Div(
        children=[
            html.H2(className="center", children="Dataframe criado a partir dos resultados"),
            # Exibindo o Datatable do dataframe baixado
            dash_table.DataTable(data=df_group.to_dict('records'), page_size=10),
        ]
    ),
    html.Div(
        children=[
            html.H2(className="center", children="Gráfico criado a partir dos resultados"),
            # exibindo o gráfico do dataframe
            dcc.Graph(
                id="scatter",
                figure=fig
            )
        ]
    ),
    html.Div(
        children=[
            html.H2(className="center", children="Histograma da positividade das frases"),
            # exibindo o gráfico do dataframe
            dcc.Graph(
                id="histogram",
                figure=fig2
            )
        ]
    )
])

if __name__ == '__main__':
    app.run(debug=True)
