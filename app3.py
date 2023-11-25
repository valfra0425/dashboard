from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import plotly.graph_objs as go
import numpy as np
import datetime
from collections import deque

# Cria uma instância do aplicativo Dash.
app = Dash(__name__)

# layout onde adicionamos as coisas do dashboard
app.layout = html.Div(
    children=[

        # Gráfico que receberá valores aleatorios de forma uniforme
        dcc.Graph(id='live-update-graph-uniforme', figure={}),
        # Interval do gráfico
        dcc.Interval(
            id="interval-component-line-uniforme",
            interval=500,
            n_intervals=0
        ),

        # Histograma que receberá valores aleatorios de forma uniforme
        dcc.Graph(id='live-update-hist-uniforme', figure={}),
        # Interval do histograma
        dcc.Interval(
            id="interval-component-hist-uniforme",
            interval=500,
            n_intervals=0
        ),

        # Gráfico que receberá valores aleatorios de forma normal
        dcc.Graph(id='live-update-graph-normal', figure={}),
        # Interval do gráfico
        dcc.Interval(
            id="interval-component-line-normal",
            interval=500,
            n_intervals=0
        ),

        # Histograma que receberá valores aleatorios de forma normal
        dcc.Graph(id='live-update-hist-normal', figure={}),
        # Interval do histograma
        dcc.Interval(
            id="interval-component-hist-normal",
            interval=500,
            n_intervals=0
        ),

        html.Div(
            children=[
                html.H3(children="Diferença entre distribuição normal e uniforme"),
                html.P(children="A disbruição uniforme distribui valores igualmente entre os valores de um determinado "
                                "intervalo de valores e a normal distribui  de forma que existe um acumulo de valores "
                                "presentes em um pico que vai diminuindo para os extremos.")
            ]
        )
    ]
)

# vars do gráfico de linha e histograma uniforme
# usamos o deque porque toda vez que um elemento novo é adicionado após o maxlen o primeiro valor do deque é removido
X = deque(maxlen=20)
Y = deque(maxlen=20)
hist = []

# vars do gráfico de linha e histograma normal
A = deque(maxlen=20)
B = deque(maxlen=20)
hist_norm = []


def gerar_dado_aleatorio():
    # Eixo x vai ser o momento onde o valor foi gerado
    X.append(datetime.datetime.now())
    # valor aleatorio uniforme de 0 a 1
    y = (np.random.uniform(0, 1))
    # Adiciona no histograma
    hist.append(y)
    # Adiciona no deck
    Y.append(y)
    # retorno na forma de gráfico de linha
    return go.Scatter(x=list(X), y=list(Y), mode='lines+markers', name='Valores Aleatórios Uniformes')


def gerar_dado_aleatorio_normal():
    # Eixo x vai ser o momento onde o valor foi gerado
    A.append(datetime.datetime.now())
    # valor aleatorio normal de 0 a 1
    b = (np.random.normal(0.5, 0.1))
    # Adiciona no histograma
    hist_norm.append(b)
    # Adiciona no deck
    B.append(b)
    # retorno na forma de gráfico de linha
    return go.Scatter(x=list(A), y=list(B), mode='lines+markers', name='Valores Aleatórios normal')


# uniform
@callback(
    Output(component_id="live-update-graph-uniforme", component_property="figure"),
    Input(component_id="interval-component-line-uniforme", component_property="n_intervals"))
# esse n representa o número de interaçãoes do input porém não está sendo usado, mas se necessario pode ser utilizado
def atualizar_grafico_uniforme(n):
    # gráfico gerado na função gerar_dado_aleatorio
    fig = gerar_dado_aleatorio()
    # detalhes do layout
    layout = go.Layout(title="valores uniformes por tempo",
                       xaxis=dict(title="Tempo"),
                       yaxis=dict(title="Valor", range=[0, 1]))
    return {'data': [fig], 'layout': layout}


# normal
@callback(
    Output(component_id="live-update-hist-uniforme", component_property="figure"),
    Input(component_id="interval-component-hist-uniforme", component_property="n_intervals"))
def atualizar_histograma_uniforme(n):
    fig = px.histogram(x=hist, nbins=50, range_x=[0, 1], title="histogram of values uniforme")
    return fig


# normal
@callback(
    Output(component_id="live-update-graph-normal", component_property="figure"),
    Input(component_id="interval-component-line-normal", component_property="n_intervals"))
def atualizar_grafico_normal(n):
    # gráfico gerado na função gerar_dado_aleatorio_normal
    fig = gerar_dado_aleatorio_normal()
    # detalhes do layout
    layout = go.Layout(title="valores normais por tempo",
                       xaxis=dict(title="Tempo"),
                       yaxis=dict(title="Valor", range=[0, 1]))
    return {'data': [fig], 'layout': layout}


@callback(
    Output(component_id="live-update-hist-normal", component_property="figure"),
    Input(component_id="interval-component-hist-normal", component_property="n_intervals"))
def atualizar_histograma_normal(n):
    fig = px.histogram(x=hist_norm, nbins=50, range_x=[0, 1], title="histogram of values normal")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
