# iCarros-hack

Códigos realizados pela equipe ACR no Hackathon realizado nos dias 20 e 21 de outubro de 2018.

A ideia principal da equipe é criar uma espécia de robo-advisor para o setor de carros.

Equipe:
  - **Helder Rezende (Dados)**
  - **Renato Martins (Dev)** https://github.com/renatomvj
  - **Matheus Pinheiro (Negócio)**
  

## Organização dos códigos

Foram feitos as seguintes etapas:

* Crawler do site da iCarros na parte da opinião do dono (https://www.icarros.com.br/opiniao-carros/ranking.jsf).
* Organização do Dataset.
* Sistema de pontuação de produtos.
* Classificação não supervisionada utilizando os comentários positivos dos avaliadores.
* Criação de uma API REST para o consumo da recomendação.
* Implementação de um ChatBot (Microsoft Bot Framework) que utiliza a API de recomendação de carros.
* Site criado para apresentação do projeto (https://www.helderrezende.com/icarros)

## Tecnologias usadas

* Linguages de programação: Python e C#
* Frameworks: Flask(Web), Microsoft Bot Framework e BeautifulSoup

## Exemplo de consumo da API

Filtro realizado por:

* Capital
* Atributos - ordem: [Conforto / Acabamento, Consumo, Custo / Benefício, Design, Dirigibilidade, Manutenção, Performance]

Ou seja, para um cliente que queira gastar 40 mil reais e tem a seguinte preferência:

* 1 - Custo / Benefício
* 2 - Consumo
* 3 - Dirigibilidade


```

https://www.helderrezende.com/api/v1/resources/recommendation?capital=40000&atributos=[0,2,1,0,3,0,0]

```

## Custo:

* Desenvolvimento de uma página.
* Equipe com um cientista de dados e um Dev.
* Desenvolvimento de um ChatBot completo.

Funcionários: 30k e Estrutura: 2k


## Estrutura
![alt text](https://i.imgur.com/1sNvKyU.png)

