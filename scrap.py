

# some important modules to scrape a website.
from bs4 import BeautifulSoup
import requests
import string
import sys
import csv



def scrap_letter(letter):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0"}

    page = requests.get(f'http://www.progarchives.com/bands-alpha.asp?letter={letter}', headers=headers)

    if page.status_code != 200:
        sys.exit('Non 200 status code received')

    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table', attrs={'cellpadding':'6'})

    table_tag = table.find_all('tr')

    artist = []
    for i in range(0, len(table_tag)):
        art = table_tag[i].find_all('a')
        if art:
            art = art[0].get_text()
            if ',' in art:
                art = art[1:-1]
                a = art.split(",")
                art = f"{a[1]} {a[0]}".strip()
            artist.append(art)

    genre = [table_tag[i].find_all('td')[1].find('span').get_text() for i in range(1, len(table_tag))]

    country = [table_tag[i].find_all('td')[2].find('span').get_text() for i in range(1, len(table_tag))]

    # Save the dataset in csv file.
    colums_names = ['artist', 'genre', 'country']
    with open(f'./raw_{letter.upper()}_progarchives.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(colums_names)
        writer.writerows(zip(artist, genre, country))

    f.close()

for letter in  string.ascii_lowercase[:26] + "0":
    scrap_letter(letter)