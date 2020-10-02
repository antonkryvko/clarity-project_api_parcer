#!/bin/env python3
"""Clarity project parcing project.

A markdown-parcer.
"""

import time
import re

import requests
from bs4 import BeautifulSoup

from settings import *


def get_clarityproject_data(codes_list):
    request_data_list = list()
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/62.0.3202.9 Safari/537.36'}
    for code in codes_list:
        response = requests.get(BASE_URL + code, headers=headers)
        print('Завантажена інформація про компанію з кодом ЄДРПОУ {}.'.format(code))
        request_data_list.append(response.content)
        time.sleep(0.1)
    print('Отримані дані Clarity-project.')
    return request_data_list


def get_registration_dates(request_data_list):
    registration_column = list()
    for request_data in request_data_list:
        try:
            soup = BeautifulSoup(request_data, 'lxml')
            registration_column.append(re.sub('\n', '',soup.find(string=re.compile(REGISTRATION_REGEXP))))
        except (KeyError, TypeError):
            registration_column.append('невідомо')
    print('Отримані дати реєстрації компаній.')
    return registration_column

def get_founders(request_data_list):
    founders_column = list()
    for request_data in request_data_list:
        try:
            soup = BeautifulSoup(request_data, "html.parser")
            founders_list=list()
            for founder in soup.select(FOUNDERS_CSS_SELECTOR):
                founder_trimmed = founder.get_text().strip()
                if (founder_trimmed not in founders_list) & (founder_trimmed is not None):
            	     founders_list.append(founder_trimmed)
            founders_column.append(founders_list)
        except (KeyError, TypeError):
            founders_column.append('невідомо')
    print('Отримані засновники компаній.')
    return founders_column

def get_capitals(request_data_list):
    capital_column = list()
    for request_data in request_data_list:
        decoded_data  = request_data.decode(encoding='UTF-8')
        try:
            regex_boundaries = re.search(CAPITAL_REGEXP, decoded_data).span()
            #знаходимо повне співпадіння з регулярним виразом
            full_match = decoded_data[regex_boundaries[0]:regex_boundaries[1]] 
	    #знаходимо індекс початку числового значення всередині повного співпадіння
            first_digit_index= re.search("\d",full_match).span()[0] 
            capital = full_match[first_digit_index:]
            capital_trimmed = capital.replace(" ","")
            capital_column.append(capital_trimmed)  
            
        except (KeyError, TypeError):
            capital_column.append('невідомо')

    print('Отримані статутні капітали компаній.')
    return capital_column


def get_main_kved(request_data_list):
    kved_column = list()
    for request_data in request_data_list:
        try:
            soup = BeautifulSoup(request_data, "html.parser")
            
            for i,td in enumerate(soup.find_all('td')):
                td_text = td.get_text()
                
                if KVED_TD in td_text:
                    all_kveds = soup.find_all('td')[i+1].find_all('div')
                    main_kved = all_kveds[0].get_text().strip()
            
            kved_column.append(main_kved)  
            
        except (KeyError, TypeError):
            kved_column.append('невідомо')
    print('Отримані основні кведи компаній.')
    return kved_column


def get_directors(request_data_list):
    directors_column = list()
    for request_data in request_data_list:
        try:
            soup = BeautifulSoup(request_data, "html.parser")           
            for i,td in enumerate(soup.find_all('td')):
                td_text = td.get_text()                
                if DIRECTORS_TD in td_text:
                    all_directors = soup.find_all('td')[i+1].find_all('div')
                    directors_list = list()
                    for director in all_directors:
                       raw_director_data = director.get_text().replace("(Згідно з Статутом)","")
                       raw_director_data = raw_director_data.strip().split("\n-\n\n")
                       if (len(raw_director_data)>=2):
                           
                           formatted_director = raw_director_data[0]+" ("+raw_director_data[1]+")"
                       
                       directors_list.append(formatted_director)
            directors_column.append(directors_list)     
        except (KeyError, TypeError):
            directors_column.append('невідомо')
    print(directors_column)
    print('Отримані директори компаній.')
    return directors_column

def get_status(request_data_list):
    status_column = list()
    for request_data in request_data_list:
        try:
            soup = BeautifulSoup(request_data, "html.parser")     
            status = soup.select(STATUS_CSS_SELECTOR)
            status_trimmed = status[0].get_text().strip().replace("\n"," ")
            status_column.append(status_trimmed)
        except (KeyError, TypeError):
            status_column.append('невідомо')
    print('Отримані стани компаній.')
    return status_column


def get_contacts(request_data_list):
    contacts_column = list()
    
    for request_data in request_data_list:
        decoded_data  = request_data.decode(encoding='UTF-8')
        contacts_list = list()
        try:
            while (re.search(CONTACTS_REGEXP,decoded_data)):
                contact_boundries = re.search(CONTACTS_REGEXP,decoded_data).span()
                contact = decoded_data[contact_boundries[0]:contact_boundries[1]]  
                contacts_list.append(contact[4:])
                contact_end_index = contact_boundries[1]
                #видаляємо частину сторінки, в якій знайшли перший контакт
                decoded_data = decoded_data[contact_end_index:] 

            contacts_column.append(contacts_list)
        except (KeyError, TypeError):
            contacts_column.append('невідомо')
    print('Отримані контакти компаній.')
    return contacts_column


# codes_list = ['21656874', '26112280', '40269229']
# request_data_list = get_clarityproject_data(codes_list)
# get_registration_dates(request_data_list)
