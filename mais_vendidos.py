import pandas as pd


def get_mais_vendidos():
    #source 'https://www.noticiasautomotivas.com.br/os-carros-mais-vendidos-do-primeiro-semestre-de-2018/'
    mais_vendidos = pd.read_csv('data/mais_vendidos_raw.txt', names=['Posicao', 'Nome', 'Value'], sep=',')
    mais_vendidos['Value'] = mais_vendidos['Value'].astype(float)
    mais_vendidos = mais_vendidos.reset_index()
    mais_vendidos['index'] += 1
    mais_vendidos = mais_vendidos.rename(columns={'index': 'ranking'})
    mais_vendidos['Marca'], mais_vendidos['Modelo'] = mais_vendidos['Nome'].str.split('/', 1).str
    
    mais_vendidos['Marca'] = mais_vendidos['Marca'].replace('VW', 'VOLKSWAGEN')
    mais_vendidos['Marca'] = mais_vendidos['Marca'].replace('GM', 'CHEVROLET')
    mais_vendidos['Marca'] = mais_vendidos['Marca'].replace('CITROEN', 'CITROËN')
    mais_vendidos['Marca'] = mais_vendidos['Marca'].replace('LR', 'LAND ROVER')
    mais_vendidos['Modelo'] = mais_vendidos['Modelo'].replace('HILUX SW4', 'SW4')
    mais_vendidos['Modelo'] = mais_vendidos['Modelo'].replace('UP!', 'UP')


    mais_vendidos = mais_vendidos.drop(['Posicao', 'Nome'], 1)
    
    return mais_vendidos
