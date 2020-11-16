import pandas as pd
import numpy as np
import json
import datetime
import re

import requests
from requests import get
from bs4 import BeautifulSoup

from time import sleep
from random import randint

OSCAR_TITLES = ['Wings', 'The Broadway Melody', 'All Quiet on the Western Front',
                'Cimarron', 'Grand Hotel', 'Cavalcade', 'It Happened One Night',
                'Mutiny on the Bounty', 'The Great Ziegfeld', 'The Life of Emile Zola',
                "You Can't Take It with You", 'Gone with the Wind', 'Rebecca',
                'How Green Was My Valley', 'Mrs. Miniver', 'Casablanca', 'Going My Way',
                'The Lost Weekend', 'The Best Years of Our Lives', "Gentleman's Agreement",
                'Hamlet', "All the King's Men", 'All About Eve', 'An American in Paris',
                'The Greatest Show on Earth', 'From Here to Eternity', 'On the Waterfront',
                'Marty', 'Around the World in 80 Days', 'The Bridge on the River Kwai',
                'Gigi', 'Ben-Hur', 'The Apartment', 'West Side Story', 'Lawrence of Arabia',
                'Tom Jones', 'My Fair Lady', 'The Sound of Music', 'A Man for All Seasons',
                'In the Heat of the Night', 'Oliver!', 'Midnight Cowboy', 'Patton',
                'The French Connection', 'The Godfather', 'The Sting', 'The Godfather Part II',
                "One Flew Over the Cuckoo's Nest", 'Rocky', 'Annie Hall', 'The Deer Hunter',
                'Kramer vs. Kramer', 'Ordinary People', 'Chariots of Fire', 'Gandhi',
                'Terms of Endearment', 'Amadeus', 'Out of Africa', 'Platoon',
                'The Last Emperor', 'Rain Man', 'Driving Miss Daisy', 'Dances with Wolves',
                'The Silence of the Lambs', 'Unforgiven', "Schindler's List", 'Forrest Gump',
                'Braveheart', 'The English Patient', 'Titanic', 'Shakespeare in Love',
                'American Beauty', 'Gladiator', 'A Beautiful Mind', 'Chicago',
                'The Lord of the Rings: The Return of the King', 'Million Dollar Baby',
                'Crash', 'The Departed', 'No Country for Old Men', 'Slumdog Millionaire',
                'The Hurt Locker', "The King's Speech", 'The Artist', 'Argo',
                '12 Years a Slave', 'Birdman or (The Unexpected Virtue of Ignorance)',
                'Spotlight', 'Moonlight', 'The Shape of Water', 'Green Book',
                'Parasite']

OSCAR_TITLES = [x.lower() for x in OSCAR_TITLES]

# Creating the lists we want to write into
titles = []
years = []
date_released = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []
budget = []

genre_list = []
certificate_list = []

link_list = []
original_language = []
oscar_list = []


# Getting English translated titles from the movies
headers = {'Accept-Language': 'en-US, en;q=0.5'}

pages = np.arange(1, 6)

# pages = [1]

# Storing each of the urls of 50 movies
for page in pages:
    # Getting the contents from the each url
    page = requests.get('https://www.imdb.com/list/ls057163321/?sort=release_date,desc&st_dt=&mode=detail&page=' + str(page))
    soup = BeautifulSoup(page.text, 'html.parser')

    # Aiming the part of the html we want to get the information from
    movie_div = soup.find_all('div', class_='lister-item mode-detail')

    # Controling the loop’s rate by pausing the execution of the loop for a specified amount of time
    # Waiting time between requests for a number between 2-10 seconds
    sleep(randint(2,10))

    for container in movie_div:
        # Scraping the movie's name
        name = container.h3.a.text
        titles.append(name)

        # Scraping the movie's year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # Scraping the movie's length
        runtime = container.find('span', class_='runtime').text if container.p.find('span', class_='runtime') else '-'
        time.append(runtime)

        # Scraping the movies' link
        temp_link_list = []
        for link in container.find_all('a'):
            temp_link_list.append(link.get('href'))
        link_list.append(temp_link_list[0])

        # Scraping genre
        genre = container.find('span', class_='genre').text if container.p.find('span', class_='genre') else '-'
        genre_list.append(genre)

        # Scraping certificate
        certificate = container.find('span', class_='certificate').text if container.p.find('span', class_='certificate') else '-'
        certificate_list.append(certificate)

        # Scraping the rating
        imdb = float(container.find('span', class_='ipl-rating-star__rating').text if container.find('span', class_='ipl-rating-star__rating') else 'nan')
        imdb_ratings.append(imdb)

        # Scraping the metascore
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)

        # Scraping votes and gross earnings
        # Scraping votes and gross earnings
        try:
            nv = container.find_all('span', attrs={'name':'nv'})
            vote = nv[0].text
        except:
            print("No vote for: " + str(name))
            vote = "0"
        votes.append(vote)

#Cleaning up ID from scraping the links
link_list = [i.replace('/title/','') for i in link_list]
link_list = [i.replace('/','') for i in link_list]

key = "1b2ecde3434e3ac104c5b73656277e9a"
for id in link_list:
    print(id)
    x = requests.get('https://api.themoviedb.org/3/movie/' + str(id) + '?api_key=' + key + '&language=en-US')
    jsonOutput = json.loads(x.text)
    try:
        us_gross.append(int(jsonOutput['revenue']))
    except:
        print("No us_gross for: " + str(id))
        us_gross.append(0)

    try:
        date_released.append(datetime.datetime.strptime((jsonOutput['release_date']), '%Y-%m-%d'))
    except:
        print("No release_date for: " + str(id))
        date_released.append('NaN')

    try:
        budget.append(int(jsonOutput['budget']))
    except:
        print("No budget for: " + str(id))
        budget.append(0)

    try:
        original_language.append(jsonOutput['original_language'])
    except:
        print("No original_language for: " + str(id))
        original_language.append('NaN')


for title in titles:
    if title.lower() in OSCAR_TITLES:
        oscar_list.append(1)
    else:
        oscar_list.append(0)


movies = pd.DataFrame({'id': link_list,
                       'movie':titles,
                       'year':years,
                       'date_released': date_released,
                       'time_minute':time,
                       'budget': budget,
                       'imdb_rating':imdb_ratings,
                       'metascore':metascores,
                       'vote':votes,
                       'gross_earning':us_gross,
                       'genre': genre_list,
                       'original_language': original_language,
                       'certificate': certificate_list,
                       'Oscar': oscar_list})


# Cleaning 'year' column
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)

# Cleaning 'time_minute' column
movies['time_minute'] = movies['time_minute'].str.extract('(\d+)').astype(int, errors='ignore')

# Cleaning 'genre' column
movies['genre'] = movies['genre'].str.replace('\n', '')
# Getting rid of extra spaces at the end
movies['genre'] = movies['genre'].str.replace('            ', '')


# Cleaning 'metascore' column
movies['metascore'] = movies['metascore'].str.extract('(\d+)')
# convert it to float and if there are dashes turn it into NaN
movies['metascore'] = pd.to_numeric(movies['metascore'], errors='coerce')

# Cleaning 'vote' column
movies['vote'] = movies['vote'].str.replace(',', '').astype(int)

movies.to_csv('IMDb_OscarNom_TMDb.csv')
