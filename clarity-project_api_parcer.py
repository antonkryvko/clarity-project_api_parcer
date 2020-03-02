#!/bin/env python3

"""Clarity project parcing project.

A parcer to receive information about Ukrainian companies.

"""

import time
from datetime import datetime

import pandas as pd
import requests

ENTRY_POINT = 'https://clarity-project.info/api/edr.info/'
DATASET = 'companies_donations.csv'

EDR_DATA_JSON_KEY = 'edr_data'
REGISTRATION_JSON_KEY = 'registration'
DATE_JSON_KEY = 'Date'
FOUNDERS_JSON_KEY = 'founders'
BENEFICIARIES_JSON_KEY = 'beneficiaries'
NAME_JSON_KEY = 'Name'
SHARE_CAPITAL_JSON_KEY = 'capital'
VAT_JSON_KEY = 'vat'

EDRPOU_COLUMN_HEADER = 'Ідентифікаційний код (для фіз. осіб)/Код ЄДРПОУ (для юр. осіб)'
REGISTRATION_COLUMN_HEADER = 'Дата реєстрації компанії'
DIFFERENCE_COLUMN_HEADER = 'Різниця між внеском і реєстрацією'
DONATION_COLUMN_HEADER = 'Дата надходження внеску'
CAPITAL_COLUMN_HEADER = 'Статутний капітал'
BENEFICIARY_COLUMN_HEADER = 'Бенефіціар'
FOUNDER_COLUMN_HEADER = 'Засновник'
VAT_COLUMN_HEADER = 'Платник податків'

DATETIMEFORMAT = '%Y-%m-%d'
OUTPUT_CSV = 'output.csv'


def upload_dataset_to_dataframe(filename):
    return pd.read_csv(filename, decimal='.', dtype={EDRPOU_COLUMN_HEADER: str})


def get_codes_from_dataframe(df, codes_list=None):
    for code in df[EDRPOU_COLUMN_HEADER]:
        codes_list.append(code)
    return codes_list


def get_clarityproject_data(codes_list, request_data_list=None):
    for code in codes_list:
        request = requests.get(ENTRY_POINT + code)
        request_data = request.json()
        request_data_list.append(request_data)
        time.sleep(0.1)
    return request_data_list


def create_column_with_registration_dates(request_data_list, registration_column=None):
    for request_data in request_data_list:
        try:
            registration_unix_time = request_data[EDR_DATA_JSON_KEY][REGISTRATION_JSON_KEY][DATE_JSON_KEY]
            registration_time_string = datetime.fromtimestamp(float(registration_unix_time)).strftime(DATETIMEFORMAT)
            registration_column.append(registration_time_string)
        except KeyError:
            registration_column.append('невідомо')
    return registration_column


def calc_difference_between_dates(request_data_list, df, difference_column=None):
    for index, request_data in enumerate(request_data_list):
        try:
            registration_unix_time = request_data[EDR_DATA_JSON_KEY][REGISTRATION_JSON_KEY][DATE_JSON_KEY]
            date1 = datetime.fromtimestamp(float(registration_unix_time))
            date2 = datetime.strptime(df[DONATION_COLUMN_HEADER][index], DATETIMEFORMAT)
            diff = date2 - date1
            difference_column.append(diff.days)
        except KeyError:
            difference_column.append('невідомо')
    return difference_column


def get_founders_or_beneficiaries(request_data_list, json_key, founder_or_beneficiar_column=None):
    for request_data in request_data_list:
        names = list()
        persons = list()
        try:
            persons = request_data[EDR_DATA_JSON_KEY][json_key]
        except KeyError:
            names.append('невідомо')
        for person in persons:
            person_name = person[NAME_JSON_KEY]
            names.append(person_name)
        founder_or_beneficiar_column.append(names)
    return founder_or_beneficiar_column


def get_capital(request_data_list, capital_column=None):
    for request_data in request_data_list:
        try:
            capital_column.append(request_data[EDR_DATA_JSON_KEY][SHARE_CAPITAL_JSON_KEY])
        except KeyError:
            capital_column.append('невідомо')
    return capital_column


def check_vat(request_data_list, vat_column=None):
    for request_data in request_data_list:
        try:
            if request_data[VAT_JSON_KEY]:
                vat_column.append('є в реєстрі')
            else:
                vat_column.append('немає в реєстрі')
        except KeyError:
            vat_column.append('немає в реєстрі')
    return vat_column


def add_columns_to_dataframe(df, registration_column, difference_column, founder_column, beneficiary_column,
                             capital_column, vat_column):
    df[REGISTRATION_COLUMN_HEADER] = registration_column
    df[DIFFERENCE_COLUMN_HEADER] = difference_column
    df[FOUNDER_COLUMN_HEADER] = founder_column
    df[BENEFICIARY_COLUMN_HEADER] = beneficiary_column
    df[CAPITAL_COLUMN_HEADER] = capital_column
    df[VAT_COLUMN_HEADER] = vat_column
    df.to_csv(OUTPUT_CSV)


def main():
    print('Розпочинаю роботу')
    df = upload_dataset_to_dataframe(DATASET)
    print('Завантажую датасет')
    codes_list = get_codes_from_dataframe(df)
    print('Отриманий список кодів ЄДРПОУ')
    request_data_list = get_clarityproject_data(codes_list)
    print('Отримані дані Clarity project')
    registration_column = create_column_with_registration_dates(request_data_list)
    difference_column = calc_difference_between_dates(request_data_list, df)
    print('Порахована різниця між внесками і реєстрацією')
    founder_column = get_founders_or_beneficiaries(request_data_list, FOUNDERS_JSON_KEY)
    print('Отриманий список засновників')
    beneficiary_column = get_founders_or_beneficiaries(request_data_list, BENEFICIARIES_JSON_KEY)
    print('Отриманий список бенефіціарів')
    capital_column = get_capital(request_data_list)
    print('Отримані дані про статутні внески')
    vat_column = check_vat(request_data_list)
    print('Перевірено на наявність в реєстрі платників податків')
    add_columns_to_dataframe(df, registration_column, difference_column, beneficiary_column, founder_column,
                             capital_column, vat_column)
    print('Робота закінчена')


if __name__ == '__main__':
    main()
