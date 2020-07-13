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
            registration_column.append(re.sub('\n', '', soup.find(string=re.compile(REGISTRATION_REGEXP))))
        except (KeyError, TypeError):
            registration_column.append('невідомо')
    print(registration_column)
    print('Отримані дати реєстрації компаній.')
    return registration_column

# codes_list = ['21656874', '26112280', '40269229']
# request_data_list = get_clarityproject_data(codes_list)
# get_registration_dates(request_data_list)
