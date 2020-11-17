# Caso Prático de Web Crawlers e Python

## Preparando o ambiente

Para ambiente que seja capaz de rodar os scripts, fazer os seguintes passo a seguir:

* Clone ou baixe o repositório
* Crie um ambiente viritual usando o comando ``` python3 -m venv .venv ```
* Ative o ambiente virutal com o comando ``` source .venv/bin/activate```
* Instale as depências listadas no requirements.txt utilizando o comando  ```pip install requirements.txt ```
* Execute os crawlers conforme explicado abaixo. 

#### Crawler 1

Objetivo desse crawler é buscar todas as declarações de políticos e autoridades de expressão nacional e se são Verdadeiras, Imprecisas, Exageradas, Contraditórias, Insustentáveis ou Falsas de acordo com método apresentado no site [AosFatos](https://aosfatos.org/nosso-m%C3%A9todo/)

Para exeutar esse Crawler execute o seguinte comando: ``` scrapy runspider aosfatos.py -s HTTPCACHE_ENABLE=1 -o fatos.csv ``` e ```CTRL + Z ``` para interromper-lo

#### Crawler 2

Obetivo desse Crawler é buscar todas as filmes com suas notas, votos e ano de lançamento sobre um intervalo de tempo(em anos) do site do [Imdb](https://www.imdb.com/?ref_=nv_home)

Para executar esse Crawler execute o seguinte comando: ``` python3 imdbmovies.py ``` e ```CTRL + Z ``` para interromper-lo
