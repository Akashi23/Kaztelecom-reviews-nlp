from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import re

def parse_spr(doc: str) -> dict:
    soup = BeautifulSoup(doc, 'html.parser')
    review = soup.find_all('div', 'review')
    json_data = {}
    json_list = []
    for i in review:
        text = i.find('p', 'reviewText')
        str_to_replace = text.find(attrs={"class": "linkFullText"})
        
        if str_to_replace in text:
            txt = text.text.replace(str_to_replace.text, '').strip()
        else:
            txt = text.text

        review_json = {
            'title' : i.find('div', 'reviewTitleText').text.strip(),
            'text' : txt,
            'rating' : 'null',
            'reaction' : i['class'][1].replace('review', ''),
            'who' : i.find('span', 'reviewAuthor').text.strip(),
            'date' : i.find('span', 'reviewDate').text,
            'website' : 'spr.kz'

        }
        json_list.append(review_json)

    json_data['spr.kz'] = json_list
    return json_data

#######################################################################################
def parse_huzhe(doc: str) -> dict:
    soup = BeautifulSoup(doc, 'html.parser')
    review = soup.find_all('div', 'item', id=True)
    json_data = {}
    json_list = []
    for i in review:
        date_and_author = i.find(attrs={'class' : 'date'}).text.strip()
        date = "".join(re.findall('[0-9.]+\n', date_and_author)).replace('\n', '')
        author = date_and_author.replace(date, "").strip()
        review_json = {
            'title' : i.find(attrs={'class' : 'title'}).text.strip(),
            'text' : i.find('p').text.strip(),
            'rating' : 'null',
            'reaction' : 'Negative',
            'who' : author,
            'date' : date,
            'website' : 'huzhe.net'

        }
        json_list.append(review_json)

    json_data['huzhe.net'] = json_list
    return json_data


def huzhe_loop():
    path_list = os.listdir('otzyv')
    list_full_path = []
    
    for i in path_list:
        f = 'Казахтелеком Контакты, Отзывы, Пожаловаться - Хуже.нет'
        if f in i and '.html' in i:
            list_full_path.append(f'otzyv/{i}')

    data = []
    for i in list_full_path:
        with open(i) as f:
            doc = f.read()
            data.append(pd.DataFrame(parse_huzhe(doc)['huzhe.net']))

    concat_data = data[0]
    for i, dt in enumerate(data):
        if i == 0:
            continue
        concat_data = concat_data.append(dt, ignore_index=True)
    
    concat_data.to_csv("dataset_full/before_merge/huzhe_net.csv", index=False)

########################################################################

########################################################################

def parse_valrating(doc: str) -> dict:
    soup = BeautifulSoup(doc, 'html.parser')
    review = soup.find_all('div', 'review')
    # print(review)
    json_data = {}
    json_list = []
    for i in review:
        rating = int(i.find(attrs={'itemprop':'ratingValue'}).text)
        date = i.find(attrs={'itemprop':'datePublished'})['datetime'].replace('-', '.')
        date = f"{date[8:10]}.{date[5:7]}.{date[0:4]}"
        reaction: str
        if rating > 3:
            reaction = 'Positive'
        else:
            reaction = 'Negative'

        review_json = {
            'title' : i.find_all(attrs={'itemprop':'name'})[1].text,
            'text' : i.find(attrs={'itemprop':'reviewBody'}).text,
            'rating' : i.find(attrs={'itemprop':'ratingValue'}).text,
            'reaction' : reaction,
            'who' : i.find_all(attrs={'itemprop':'name'})[0].text.strip(),
            'date' : date,
            'website' : 'valrating.com'

        }
        json_list.append(review_json)

    json_data['valrating.com'] = json_list
    return json_data


def valrating_loop():
    path_list = os.listdir('otzyv')
    list_full_path = []

    for i in path_list:
        f = 'Отзывов АО «Казахтелеком»'
        if f in i and '.html' in i:
            list_full_path.append(f'otzyv/{i}')

    data = []
    for i in list_full_path:
        with open(i) as f:
            doc = f.read()
            data.append(pd.DataFrame(parse_valrating(doc)['valrating.com']))

    concat_data = data[0]
    for i, dt in enumerate(data):
        if i == 0:
            continue
        concat_data = concat_data.append(dt, ignore_index=True)
    
    concat_data.to_csv("dataset_full/before_merge/valrating_com.csv", index=False)

########################################################################

def parse_2ip(doc: str) -> dict:
    soup = BeautifulSoup(doc, 'html.parser')
    review = soup.find_all('div', 'reviewItem')
    # print(review)
    json_data = {}
    json_list = []
    for i in review:
        date = i.find(attrs={'class':'reviewItem__date'}).text.strip()
        title = i.find(attrs={'class':'reviewItem__title'}).text.strip()
        text = i.find(attrs={'class':'reviewItem__txt'}).text.strip()
        user = i.find(attrs={'class':'reviewItem__user reviewItem__link'}).text.strip()
        month_list = {'февраля': '2', 'января':'1'}
        month = date.split(' ')[1]
        if month in month_list.keys():
            date = f"{date.split()[0]}.0{month_list[month]}.2021"
        else:
            date = date.split(' ')[0]
        
        rating_list = i.find(attrs={'class':'rating reviewItem__rating-mobile'}).find_all(attrs={'class':'rating__item'})
        rating = 0
        for i in rating_list:
            if 'full' in i['src']:
                rating += 1

        reaction: str
        if rating > 3:
            reaction = 'Positive'
        else:
            reaction = 'Negative'
        
        review_json = {
            'title' : title,
            'text' : text,
            'rating' : rating,
            'reaction' : reaction,
            'who' : user,
            'date' : date,
            'website' : '2ip.ru'
        }
        json_list.append(review_json)

    json_data['2ip.ru'] = json_list
    return json_data


def ip_loop():
    path_list = os.listdir('otzyv')
    list_full_path = []

    for i in path_list:
        f = 'Отзывы об интернет провайдере Казахтелеком'
        if f in i and '.html' in i:
            list_full_path.append(f'otzyv/{i}')

    data = []
    for i in list_full_path:
        with open(i) as f:
            doc = f.read()
            data.append(pd.DataFrame(parse_2ip(doc)['2ip.ru']))

    concat_data = data[0]
    for i, dt in enumerate(data):
        if i == 0:
            continue
        concat_data = concat_data.append(dt, ignore_index=True)
    # print(concat_data)
    concat_data.to_csv("dataset_full/before_merge/2ip_ru.csv", index=False)

############################################################################
def all_data_merge():
    path_list = os.listdir('dataset_full/before_merge')
    data = []
    for i in path_list:
        data.append(pd.read_csv(f'dataset_full/before_merge/{i}'))

    concat_data = data[0]
    for i, dt in enumerate(data):
        if i == 0:
            continue
        concat_data = concat_data.append(dt, ignore_index=True)
    # print(concat_data)
    concat_data.to_csv("dataset_full/kazakhtel_review.csv", index=False)
    
#################################################################################
def data_for_nlp():
    path = 'dataset_full/kazakhtel_review.csv'
    data = pd.read_csv(path)
    data_for_nlp = data.drop(columns=['title', 'rating', 'who', 'date', 'website'])
    data_for_nlp['reaction'] = data_for_nlp['reaction'].map({'Positive' : '1', 'Negative': '0'})
    data_for_nlp.to_csv('dataset_nlp/kazakhtel_review_reaction.csv', index=False)

#### SPR.KZ ###########
# with open("otzyv/724-otzyv.html", encoding='windows-1251') as f:
#     doc = f.read()
#     data = pd.DataFrame(parse_spr(doc)['spr.kz'])
#     data.to_csv("dataset_full/before_merge/spr_kz.csv", index=False)