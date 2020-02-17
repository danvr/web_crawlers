import json
import requests
import re
from time import sleep
from random import randint
from bs4 import BeautifulSoup
import pandas as pd

base_url = 'http://www.imdb.com/search/title'

params = dict(
    params='num_votes,desc',
    start=1,
    title_type='feature',
    year='2018,2020'
)

imdb_movies_dict = {    
    'movie': [],
    'year': [],
    'imdb': [],
    'metascore': [],
    'votes':[]   
}


def make_soup(base_url,params):
    page = requests.get(base_url, params=params)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def get_request_number(soup):
    movies_count = get_movie_count(soup)
    request_number = round(movies_count/50)
    return request_number


def get_movie_count(soup):
    pagination_number = soup.find_all(class_ = 'desc')[0].span.text
    regex = re.compile(r'([0-9]+\S[0-9]+)\stitles')
    movies_count = int(regex.findall(pagination_number)[0].replace(",",""))
    return movies_count


def get_movie_info(soup,dict_):
    
    movies = soup.find_all(
    'div',
     class_ = 'lister-item mode-advanced'
     )
    
    for movie in movies:

        if movie.find('div', class_ = 'ratings-metascore') is not None:

            name = movie.h3.a.text
            dict_['movie'].append(name)

            year = movie.h3.find('span', class_ = 'lister-item-year').text
            dict_['year'].append(year)

            imdb = float(movie.strong.text)
            dict_['imdb'].append(imdb)

            m_score = int(movie.find('span', class_ = 'metascore').text)
            dict_['metascore'].append(m_score)

            vote = int(movie.find('span', attrs = {'name':'nv'})['data-value'])
            dict_['votes'].append(vote)



soup = make_soup(base_url,params)
number_of_requests = get_request_number(soup)

for request_count in range(0,number_of_requests):
    params["start"] =+ 50*request_count +1
    soup_html = make_soup(base_url,params)
    get_movie_info(soup_html,imdb_movies_dict)
    print("Scraping movies on page {}".format(request_count +1))
    print("To stop the process press crl + c")
    print(str(len(imdb_movies_dict["movie"])) + " scraped movies until now")
    sleep(randint(1,4))
    
pd.DataFrame(imdb_movies_dict).to_csv("imdb.csv", index = False)


