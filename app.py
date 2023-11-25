from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

# Cria uma instância do aplicativo Dash.
app = Dash(__name__)

# Criação de um dataframe sobre cidades com o pandas
df = pd.DataFrame({
    "Points": ["Praça", "Lanchonete", "Restaurante", "Praça", "Lanchonete", "Restaurante"],
    "frequencia": [500, 1000, 750, 1000, 2000, 1500],
    "Cidades": ["CN", "CN", "CN", "SV", "SV", "SV"]
})

# gráfico de barra da frequencia de cada ponto em cada cidade
fig = px.bar(df, x="Points", y="frequencia", color="Cidades", barmode="group")

# layout onde adicionamos as coisas do dashboard
app.layout = html.Div(children=[
    # H1 html
    html.H1(children='Meu Primeiro Dashboard'),
    # gráfico feito acima
    dcc.Graph(
        id="cidades_graph",
        figure=fig
    )
])

if __name__ == '__main__':
    app.run(debug=True)
