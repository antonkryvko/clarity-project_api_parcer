#!/bin/env python3
"""Clarity project parcing project.

An API-parcer.
"""

import time
from datetime import datetime

import requests

from settings import *


def get_clarityproject_data(codes_list):
    request_data_list = list()
    for code in codes_list:
        response = requests.get(ENTRY_POINT + code + '?key=' + API_KEY).json()
        request_data_list.append(response)
        time.sleep(0.1)
    print('Отримані дані Clarity-project.')
    return request_data_list


def get_registration_dates(request_data_list):
    registration_column = list()
    for request_data in request_data_list:
        try:
            registration_unix_time = request_data[EDR_DATA_JSON_KEY][REGISTRATION_JSON_KEY][DATE_JSON_KEY]
            registration_time_string = datetime.fromtimestamp(float(registration_unix_time)).strftime(DATETIMEFORMAT)
            registration_column.append(registration_time_string)
        except KeyError:
            registration_column.append('невідомо')
    print('Отримані дати реєстрації компаній.')
    return registration_column


def get_founders_or_beneficiaries(request_data_list, json_key):
    founder_or_beneficiar_column = list()
    for request_data in request_data_list:
        names = list()
        persons = list()
        try:
            persons = request_data[EDR_DATA_JSON_KEY][json_key]
        except KeyError:
            names.append('невідомо')
        for person in persons:
            names.append(person[NAME_JSON_KEY])
        founder_or_beneficiar_column.append(names)
    return founder_or_beneficiar_column


def get_capital(request_data_list):
    capital_column = list()
    for request_data in request_data_list:
        try:
            capital_column.append(request_data[EDR_DATA_JSON_KEY][SHARE_CAPITAL_JSON_KEY])
        except KeyError:
            capital_column.append('невідомо')
    print('Отримані дані про статутні внески.')
    return capital_column


def check_vat(request_data_list):
    vat_column = list()
    for request_data in request_data_list:
        try:
            if request_data[VAT_JSON_KEY]:
                vat_column.append('є в реєстрі')
            else:
                vat_column.append('немає в реєстрі')
        except KeyError:
            vat_column.append('немає в реєстрі')
    print('Перевірено на наявність в реєстрі платників податків.')
    return vat_column
