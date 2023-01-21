from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff

app = Dash(__name__)

#============================================ INÍCIO DO GRÁFICO ============================================#
df = pd.read_csv('primeiro-semestre-2021.csv', encoding = 'utf-8')

lista = df.values.tolist()
casos = []

tipo_violencia = 61
data_ocorrencia = 1
 

for item in lista:
  conjunto = [item[tipo_violencia], item[data_ocorrencia]]
  casos.append(conjunto)

def calcula(nome_crime, lista_de_casos):
    casos_crime = []
    total = 0

    for caso in lista_de_casos:
        tipo_violencia = str(caso[0])
        if tipo_violencia[-len(nome_crime):] == str(nome_crime):
            total += 1
            casos_crime.append(caso)

    datas = []

    for caso in casos_crime:
        datas.append(caso[1])

    jan, fev, mar, abr, mai, jun = 0,0,0,0,0,0
    meses_tot = [jan, fev, mar, abr, mai, jun, total]
    contador = 1
    achou_mes = False

    for data in datas:
        while achou_mes == False:
            if int(data[5:7]) == contador:
                meses_tot[contador - 1] += 1
                contador = 1
                achou_mes = True
            else:
                contador += 1
        achou_mes = False

    nome_crime = nome_crime[0] + nome_crime[1:].lower()
    resultado = [nome_crime, meses_tot[0], meses_tot[1], meses_tot[2], meses_tot[3], meses_tot[4], meses_tot[5], meses_tot[6]]
    return(resultado)

# ==================================================== FIGURA ==========================================#

dados_tabela = [['Tipo de Violência', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Total'],
                calcula('ESTUPRO', casos),
                calcula('ASSÉDIO SEXUAL', casos),
                calcula('LESÃO CORPORAL', casos)]


fig = ff.create_table(dados_tabela, height_constant=60)

categorias = ['Janeiro', 'Fevereiro', 'Março',
         'Abril', 'Maio', 'Junho', 'Total']
estupro = calcula('ESTUPRO', casos)[1:]
assedio = calcula('ASSÉDIO SEXUAL', casos)[1:]
lesao = calcula('LESÃO CORPORAL', casos)[1:]

barra1 = go.Bar(x=categorias, y=estupro, xaxis='x2', yaxis='y2',
                marker=dict(color='#0099ff'),
                name='Denúncias de<br>estupro')
barra2 = go.Bar(x=categorias, y=assedio, xaxis='x2', yaxis='y2',
                marker=dict(color='#404040'),
                name='Denúncias de<br>assédio sexual')
barra3 = go.Bar(x=categorias, y=lesao, xaxis='x2', yaxis='y2',
                marker=dict(color='#00FF7F'),
                name='Denúncias de<br>lesão corporal')

fig.add_traces([barra1, barra2, barra3])

fig['layout']['xaxis2'] = {}
fig['layout']['yaxis2'] = {}

fig.layout.yaxis.update({'domain': [0, .45]})
fig.layout.yaxis2.update({'domain': [.6, 1]})

fig.layout.yaxis2.update({'anchor': 'x2'})
fig.layout.xaxis2.update({'anchor': 'y2'})
fig.layout.yaxis2.update({'title': 'Número de Incidentes'})

fig.layout.margin.update({'t':75, 'l':50})
fig.layout.update({'title': 'Violência contra a Mulher - Denúncias'})

fig.layout.update({'height':800})

#============================================ FIM DO GRÁFICO ============================================#
opcoes = categorias
opcoes.append('Todos os meses')

app.layout = html.Div(children=[
    html.H1(children='Violência contra a mulher no Brasil'),

    html.Div(children='''
        Denúncias de casos de estupro, assédio sexual e lesão corporal.
    '''),

    dcc.Dropdown(opcoes, value='Todos os meses', id='lista_de_meses'),

    dcc.Graph(
        id='grafico_violencia',
        figure=fig
    )
])

@app.callback(
    Output('grafico_violencia', 'figure'),
    Input('lista_de_meses', 'value')
)
def update_output(value):
    if value == 'Todos os meses':
        dados_tabela = [['Tipo de Violência', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Total'],
                calcula('ESTUPRO', casos),
                calcula('ASSÉDIO SEXUAL', casos),
                calcula('LESÃO CORPORAL', casos)]


        fig = ff.create_table(dados_tabela, height_constant=60)

        categorias = ['Janeiro', 'Fevereiro', 'Março',
                'Abril', 'Maio', 'Junho', 'Total']
        estupro = calcula('ESTUPRO', casos)[1:]
        assedio = calcula('ASSÉDIO SEXUAL', casos)[1:]
        lesao = calcula('LESÃO CORPORAL', casos)[1:]

        barra1 = go.Bar(x=categorias, y=estupro, xaxis='x2', yaxis='y2',
                        marker=dict(color='#0099ff'),
                        name='Denúncias de<br>estupro')
        barra2 = go.Bar(x=categorias, y=assedio, xaxis='x2', yaxis='y2',
                        marker=dict(color='#404040'),
                        name='Denúncias de<br>assédio sexual')
        barra3 = go.Bar(x=categorias, y=lesao, xaxis='x2', yaxis='y2',
                        marker=dict(color='#00FF7F'),
                        name='Denúncias de<br>lesão corporal')

        fig.add_traces([barra1, barra2, barra3])

        fig['layout']['xaxis2'] = {}
        fig['layout']['yaxis2'] = {}

        fig.layout.yaxis.update({'domain': [0, .45]})
        fig.layout.yaxis2.update({'domain': [.6, 1]})

        fig.layout.yaxis2.update({'anchor': 'x2'})
        fig.layout.xaxis2.update({'anchor': 'y2'})
        fig.layout.yaxis2.update({'title': 'Número de Incidentes'})

        fig.layout.margin.update({'t':75, 'l':50})
        fig.layout.update({'title': 'Violência contra a Mulher - Denúncias'})

        fig.layout.update({'height':800})

    else:
        dados_tabela = [['Tipo de Violência', 'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Total'],
                calcula('ESTUPRO', casos),
                calcula('ASSÉDIO SEXUAL', casos),
                calcula('LESÃO CORPORAL', casos)]

        lista_indices = dados_tabela[0]


        fig = ff.create_table(dados_tabela, height_constant=60)

# Aqui os dados do gráfico serão colocados, categorias recebe o mês selecionado
# a função calcula('ESTUPRO', casos) recebe uma lista com o número de casos de janeiro à junho, mês a mês.
# por isso usamos [lista_indices.index(value)] para pegar apenas o numero de casos no mês selecionado.
# Essa estratégia funciona para as variáveis assedio e lesao da mesma forma.
        categorias = [value]
        estupro = [calcula('ESTUPRO', casos)[lista_indices.index(value)]]
        assedio = [calcula('ASSÉDIO SEXUAL', casos)[lista_indices.index(value)]]
        lesao = [calcula('LESÃO CORPORAL', casos)[lista_indices.index(value)]]

        barra1 = go.Bar(x=categorias, y=estupro, xaxis='x2', yaxis='y2',
                        marker=dict(color='#0099ff'),
                        name='Denúncias de<br>estupro')
        barra2 = go.Bar(x=categorias, y=assedio, xaxis='x2', yaxis='y2',
                        marker=dict(color='#404040'),
                        name='Denúncias de<br>assédio sexual')
        barra3 = go.Bar(x=categorias, y=lesao, xaxis='x2', yaxis='y2',
                        marker=dict(color='#00FF7F'),
                        name='Denúncias de<br>lesão corporal')

        fig.add_traces([barra1, barra2, barra3])

        fig['layout']['xaxis2'] = {}
        fig['layout']['yaxis2'] = {}

        fig.layout.yaxis.update({'domain': [0, .45]})
        fig.layout.yaxis2.update({'domain': [.6, 1]})

        fig.layout.yaxis2.update({'anchor': 'x2'})
        fig.layout.xaxis2.update({'anchor': 'y2'})
        fig.layout.yaxis2.update({'title': 'Número de Incidentes'})

        fig.layout.margin.update({'t':75, 'l':50})
        fig.layout.update({'title': 'Violência contra a Mulher - Denúncias'})

        fig.layout.update({'height':800})

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)