import pandas as pd
import mais_vendidos
import crawler
from sklearn import preprocessing

def main():
    #crawler.main()
    
    mais_vendidos_df = mais_vendidos.get_mais_vendidos()
    ranking = pd.read_csv('data/ranking.csv', encoding='latin-1')
    
    ranking = ranking.merge(mais_vendidos_df, on=['Marca', 'Modelo'], how='left')
    ranking['Value'] = ranking['Value'].fillna(0)
    
    min_max_scaler = preprocessing.MinMaxScaler()
    ranking['vendas_normalizada'] = min_max_scaler.fit_transform(ranking['Value'])
    
    ranking.to_csv('data/ranking_complete.csv', index=False)
    
    return ranking

if __name__ == "__main__":
    main()