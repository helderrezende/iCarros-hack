import requests
from bs4 import BeautifulSoup
import pandas as pd

link_ranking = 'https://www.icarros.com.br/opiniao-carros/ranking.jsf'
url_icarros = 'https://www.icarros.com.br'

def get_string_page(link, number_page):
    result = requests.post("https://www.icarros.com.br/opiniao-carros/ranking.jsf",
                    data={'j_idt107:j_idt116':'j_idt107:j_idt116','paginaAtual':str(number_page),'categoria':'0'})
    c = result.content
    soup = BeautifulSoup(c)
    
    return soup

def get_string_html(link):
    result = requests.get(link)
    c = result.content
    soup = BeautifulSoup(c)
    
    return soup

def get_links(page):
    links = []

    for sample in page:
        link = url_icarros + sample['href']

        links.append(link)
        
    return links

def get_score(table_score, string_html, link):
    marca = string_html.find("span", {"class": "makeName"}).get_text().replace("\n", "").lstrip(' ')
    modelo = string_html.find("span", {"class": "modelName"}).get_text().replace("\n", "").lstrip(' ')
    ano = string_html.find("span", {"class": "modelYear"}).get_text().replace("\n", "").lstrip(' ')
    price = string_html.find_all("span", {"class": "font-bold"})[0].text
    
    page_tag = string_html.find_all("ul", {"class": "new-pagination__container"})
    try:
        number_pages = len(page_tag[0].find_all('li', {"class": "new-pagination__item"})) - 1
    except:
        number_pages = 0

    positive_text = ""
    
    for i in range(1, number_pages + 1):
        link_temp = link
        link_temp = link_temp.replace('opinioes', '') + 'opiniao-do-dono?order=1&anoReview=3&pag='+ str(i) + '#opinioes'
        print (link_temp)
        
        textos_html = get_string_html(link_temp)
        textos_div = textos_html.find_all("div", {"class": "review-box__text"})

        for texto in textos_div:
            if 'Pontos positivos' in texto.text:
                positive_text = positive_text + texto.text

    score_list = []
    columns = ['Conforto / Acabamento', 'Consumo', 'Custo / Benefício', 'Design', 'Dirigibilidade', 'Manutenção', 'Performance']

    for score in table_score:
        score_list.append(score.text)

    df_score = pd.DataFrame([score_list], columns=columns)
    df_score['Marca'] = marca
    df_score['Modelo'] = modelo
    df_score['Ano'] = ano
    df_score['Pages'] = number_pages
    df_score['Texto Positivo'] = positive_text
    df_score['Price'] = price
    
    return df_score

def get_table_page(links):
    result = pd.DataFrame()

    for link in links:
        print (link)
        string_html = get_string_html(link)
        table_score = string_html.find_all("div", {"class": "font-lg font-bold"})
        df_score = get_score(table_score, string_html, link)

        result = pd.concat([df_score, result])
        
    return result

def get_link_img(string_html):
    imgs = string_html.find_all("img")

    for img in imgs:
        try:
            if 'galeriaimgmodelo' in img['data-src']:
                return img['data-src']
        except:
            pass
        
def get_images_table():
    link_ranking = 'https://www.icarros.com.br/opiniao-carros/ranking.jsf'
    url_icarros = 'https://www.icarros.com.br'

    number_of_pages = 31

    result = pd.DataFrame()

    for i in range(number_of_pages):
        print ('Page:' + str(i))
        r = requests.post("https://www.icarros.com.br/opiniao-carros/ranking.jsf",
                    data={'j_idt107:j_idt116':'j_idt107:j_idt116','paginaAtual':str(i),'categoria':'0'})
        c = r.content
        soup = BeautifulSoup(c)

        samples = soup.find_all("a", {"class": "linkcatalogo"})
        links = get_links(samples)


        for link in links:
            string_html = get_string_html(link)
            table_score = string_html.find_all("div", {"class": "font-lg font-bold"})

            columns = ['Conforto / Acabamento', 'Consumo', 'Custo / Benefício', 'Design', 'Dirigibilidade', 'Manutenção', 'Performance']
            marca = string_html.find("span", {"class": "makeName"}).get_text().replace("\n", "").lstrip(' ')
            modelo = string_html.find("span", {"class": "modelName"}).get_text().replace("\n", "").lstrip(' ')
            link_img = get_link_img(string_html)

            print (link_img)

            df_score = pd.DataFrame([{'Marca': marca, 'Modelo':modelo, 'link': link_img}])

            result = pd.concat([df_score, result])
            
    return result

def main():
    link_ranking = 'https://www.icarros.com.br/opiniao-carros/ranking.jsf'
    url_icarros = 'https://www.icarros.com.br'
    
    number_of_pages = 5
    
    result = pd.DataFrame()
    
    for i in range(number_of_pages):
        print ('Page:' + str(i))
        r = requests.post("https://www.icarros.com.br/opiniao-carros/ranking.jsf",
                    data={'j_idt107:j_idt116':'j_idt107:j_idt116','paginaAtual':str(i),'categoria':'0'})
        c = r.content
        soup = BeautifulSoup(c)

        samples = soup.find_all("a", {"class": "linkcatalogo"})
        links = get_links(samples)
        
        try:
            result_page = get_table_page(links)

            result = pd.concat([result_page, result])
        except:
            pass

    #print (result)
    result['Marca'] = result['Marca'].str.upper()
    result['Modelo'] = result['Modelo'].str.upper()
    result = result[result['Price'].str.contains("R")]
    
    result['Price'] = result['Price'].str.replace('$', '').str.replace('R', '').str.lstrip().str.replace('.', '')
    result['Price'] = result['Price'].astype(float)
    
    columns = ['Conforto / Acabamento', 'Consumo', 'Custo / Benefício', 'Design', 'Dirigibilidade', 'Manutenção', 'Performance']

    for column in columns:
        result[column] = result[column].str.replace(',', '.').convert_objects(convert_numeric=True)
        
    return result