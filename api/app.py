import flask
from flask import request, jsonify
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True

recomendacoes = pd.read_csv('data/ranking_complete.csv', encoding='latin-1')
recomendacoes = recomendacoes[recomendacoes['Pages'] > 2]


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
                                table['vendas_normalizada'] * 90
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
            margem_cima = capital * 1.01
            margem_baixo = capital * 0.90


            table = table[(margem_baixo <=  table['Price']) &  (margem_cima >=  table['Price'])]
                            
    table = table.sort_values('Pontuacao', ascending=False)
    table = table[['Marca', 'Modelo', 'Ano']]
    
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
    
    capital = float(query_parameters.get('capital'))
    atributos = eval(query_parameters.get('atributos'))
  

    
    todas_recomendacoes = calc_score(recomendacoes, capital=capital, atributos=atributos)

    return todas_recomendacoes.to_json(orient='records')

if __name__ == "__main__":
    app.run()