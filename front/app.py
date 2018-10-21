import flask
from flask import Flask, render_template, request, redirect
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

recomendacoes = pd.read_csv('static/ranking_complete_group_img.csv', encoding='latin-1')
recomendacoes = recomendacoes[recomendacoes['Pages'] > 2]

position_atributos = {'Conforto / Acabamento':0, 'Consumo':1, 'Custo / Benefício':2, 'Design':3,
                      'Dirigibilidade':4, 'Manutenção':5, 'Performance':6}

def calc_score(table, capital, atributos=[1, 2, 3, 0, 0, 0, 0]):
    if atributos != None:
        atributos = [int(x) for x in atributos]
        atributos = [3/x if x > 0 else 0 for x in atributos]

        table['Pontuacao'] = table['Conforto / Acabamento'] * (atributos[0] + 1) + \
                                table['Consumo'] * (atributos[1] + 1) + \
                                table['Custo / Benefício'] * (atributos[2] + 1) +  \
                                table['Design'] * (atributos[3] + 1) +  \
                                table['Dirigibilidade'] * (atributos[4] + 1) + \
                                table['Manutenção'] * (atributos[5] + 1) + \
                                table['Performance'] * (atributos[6] + 1) + \
                                table['vendas_normalizada'] * 50
    else:
        table['Pontuacao'] = 1

    if capital != None:
        print (capital)
        if capital > 200000:
            table = table[(200000 <=  table['Price'])]
            print (table)

        elif capital < 10000:
            table = table[(table['Price'] <= 10000)]


        else:
            margem_cima = capital * 1.10
            margem_baixo = capital * 0.85


            table = table[(margem_baixo <=  table['Price']) &  (margem_cima >=  table['Price'])]

    table = table.sort_values('Pontuacao', ascending=False)
    table = table[['Marca', 'Modelo', 'Ano', 'Grupo', 'link']]
    table['link'] = table['link'].fillna('https://image.slidesharecdn.com/midiakit2016-icarros-160406125244/95/icarros-midia-kit-2016-1-638.jpg?cb=1459947506')

    table = table.reset_index(drop=True).reset_index()
    table = table.rename(columns={'index':'Posicao'})

    return table

@app.route('/api/v1/resources/recommendation/all', methods=['GET'])
def api_all():
    todas_recomendacoes = calc_score(recomendacoes, capital=None, atributos=None)

    return todas_recomendacoes.to_json(orient='records')

@app.route('/api/v1/resources/recommendation', methods=['GET'])
def api_filter():
    query_parameters = request.args

    try:
        capital = float(query_parameters.get('capital'))
    except:
        capital = None

    try:
        atributos = eval(query_parameters.get('atributos'))
    except:
        atributos = None



    todas_recomendacoes = calc_score(recomendacoes, capital=capital, atributos=atributos)

    return todas_recomendacoes.to_json(orient='records')

@app.route('/icarros', methods=['GET', 'POST'])
def icarros():  
    result = [{'Nome': 'CHEVROLET ONIX', 'Ano': '2019', 'link':'https://img1.icarros.com/dbimg/galeriaimgmodelo/1/130529_1.png'},
             {'Nome': 'HYUNDAI HB20', 'Ano': '2019', 'link': 'https://img1.icarros.com/dbimg/galeriaimgmodelo/1/126411_1.png'},
             {'Nome': 'VOLKSWAGEN POLO', 'Ano': '2019', 'link': 'https://img2.icarros.com/dbimg/galeriaimgmodelo/1/130702_1.png'}]

    if request.method == 'POST':
        atributos = [0, 0, 0, 0, 0, 0, 0]

        opcao_1 = request.form.get("opcao_1")
        opcao_2 = request.form.get("opcao_2")
        opcao_3 = request.form.get("opcao_3")

        if opcao_1 in position_atributos.keys():
            atributos[position_atributos[opcao_1]] = 1

        if opcao_2 in position_atributos.keys():
            atributos[position_atributos[opcao_2]] = 2

        if opcao_3 in position_atributos.keys():
            atributos[position_atributos[opcao_3]] = 3

        money = request.form.get("money")

        try:
            money = float(money)
        except: 
            money = 30000

        #opcao_1 = request.form["opcao_1"]
        print (opcao_1)
        print (opcao_2)
        print (opcao_3)

        print (money)

        result_df = calc_score(recomendacoes, money, atributos=atributos)
        result_df = result_df.head(5)

        print(result_df)

        result_df['Nome'] = result_df['Marca'] + ' ' + result_df['Modelo']

        result_df = result_df[['Nome', 'Ano', 'link']]

        result_df['Ano'] = result_df['Ano'].apply(lambda x: str(x))
        result_json = result_df.to_json(orient='records')
        result_json = eval(result_json)

        print (result_json)


        return render_template('index_1.html', result=result_json)




    return render_template('index_1.html', result=result)


if __name__ == "__main__":
    app.run()