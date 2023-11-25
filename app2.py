from dash import Dash, html, dcc, dash_table, callback, Output, Input
import plotly.express as px
import pandas as pd

# Cria uma instância do aplicativo Dash.
app = Dash(__name__)
# lendo um dataframe da web
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# pegando apenas os resultados com continet Americas
df2 = df[df['continent'] == 'Americas']

# layout onde adicionamos as coisas do dashboard
app.layout = html.Div(children=[
    html.Div(
        className="my-header",
        children=[
            html.H1(children="Análise sobre países")
        ]
    ),
    html.Hr(),
    html.Div(
        children=[
            # Exibindo o Datatable do dataframe baixado
            dash_table.DataTable(data=df.to_dict('records'), page_size=10),
            # controle da exibição dos histograma + classes do RadioItems
            dcc.RadioItems(options=['pop', 'lifeExp', 'gdpPercap'], value='lifeExp', id="controle-radio",
                           className="radio", labelClassName="radio-item"),
            # histograma
            dcc.Graph(
                id="controle-grafico",
                figure={}
            ),
        ]
    ),
    html.Div(
        children=[
            # controle da exibição do gráfico + classes do RadioItems
            dcc.RadioItems(options=['pop', 'gdpPercap'], value='gdpPercap', id="radio2", className="radio",
                           labelClassName="radio-item"),
            # gráfico de pizza
            dcc.Graph(
                id="graph2",
                figure={}
            ),
        ]
    )
])


# Decorator callback utilizado para deixar gráficos atualizaveis de forma automática
@callback(
    # Output: toda vez que a funçao é terminada ele manda o returna para o component_property do elemento com id igual
    # ao informado no component_id
    Output(component_id="controle-grafico", component_property="figure"),
    # Input toda vez que o componente com id "controle-radio tiver o value alterado a função sera chamada
    Input(component_id="controle-radio", component_property="value"))
# função chamada pelo input inicializada pelo value do componente
def atualizar_grafico(col):
    # histogrma feito de acordo com a coluna selecionada no raiobutton
    fig = px.histogram(data_frame=df, x="continent", y=col, histfunc='avg')
    return fig


# semelhante ao anterior porém o gráfico tem atualizações de formato
@callback(
    Output(component_id="graph2", component_property="figure"),
    Input(component_id="radio2", component_property="value"))
def update_graph(col):
    fig = px.pie(data_frame=df2, values=col, names='country', title=f'{col} of Asia')
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    return fig


if __name__ == '__main__':
    app.run(debug=True)
