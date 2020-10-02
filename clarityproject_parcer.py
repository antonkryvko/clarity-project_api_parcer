#!/bin/env python3
# -*- coding: utf-8 -*-
"""Clarity-project parcing program.

A parcer to receive information about Ukrainian companies.
You need a valid API-key to use it. In case you have no key, program will try to get data via scrapping.

Before start, change constants in settings.py to appropriate ones.
"""
import pandas as pd

import clarityproject_api_parcer
import clarityproject_markdown_parcer
from settings import *


def upload_dataset_to_dataframe(filename):
    print('Завантажую датасет')
    return pd.read_csv(filename, decimal='.', dtype={EDRPOU_COLUMN_HEADER: str})


def get_codes_from_dataframe(df):
    codes_list = list()
    for code in df[EDRPOU_COLUMN_HEADER]:
        codes_list.append(code)
    print('Отриманий список кодів ЄДРПОУ')
    return codes_list


def add_columns_to_dataframe(df, registration_column=None, founder_column=None, beneficiary_column=None,
                             capital_column=None, vat_column=None, main_kved_column = None, status_column = None, 
                             contacts_column=None, directors_column=None):
    df[REGISTRATION_COLUMN_HEADER] = registration_column
    df[FOUNDER_COLUMN_HEADER] = founder_column
    df[BENEFICIARY_COLUMN_HEADER] = beneficiary_column
    df[CAPITAL_COLUMN_HEADER] = capital_column
    df[VAT_COLUMN_HEADER] = vat_column
    df[MAIN_KVED_COLUMN_HEADER] = main_kved_column
    df[STATUS_COLUMN_HEADER] = status_column
    df[CONTACTS_COLUMN_HEADER] = contacts_column
    df[DIRECTORS_COLUMN_HEADER] = directors_column
    df.to_csv(OUTPUT_CSV, index=False)


if __name__ == '__main__':
    print('Розпочинаю роботу')
    df = upload_dataset_to_dataframe(INPUT_CSV)
    codes_list = get_codes_from_dataframe(df)
    try:
        request_data_list = clarityproject_api_parcer.get_clarityproject_data(codes_list)
        registration_column = clarityproject_api_parcer.get_registration_dates(request_data_list)
        founder_column = clarityproject_api_parcer.get_founders_or_beneficiaries(request_data_list, FOUNDERS_JSON_KEY)
        print('Отриманий список засновників.')
        beneficiary_column = clarityproject_api_parcer.get_founders_or_beneficiaries(request_data_list,
                                                                                     BENEFICIARIES_JSON_KEY)
        print('Отриманий список бенефіціарів.')
        capital_column = clarityproject_api_parcer.get_capital(request_data_list)
        vat_column = clarityproject_api_parcer.check_vat(request_data_list)
    except ValueError:
        print('Немає доступу до API, переходжу у режим скрепінгу.')
        request_data_list = clarityproject_markdown_parcer.get_clarityproject_data(codes_list)
        registration_column = clarityproject_markdown_parcer.get_registration_dates(request_data_list)
        founders_column = clarityproject_markdown_parcer.get_founders(request_data_list)
        capital_column = clarityproject_markdown_parcer.get_capitals(request_data_list)
        kved_column = clarityproject_markdown_parcer.get_main_kved(request_data_list)
        status_column = clarityproject_markdown_parcer.get_status(request_data_list)
        contacts_column = clarityproject_markdown_parcer.get_contacts(request_data_list)
        directors_column = clarityproject_markdown_parcer.get_directors(request_data_list)
    # add_columns_to_dataframe(df, registration_column, beneficiary_column, founder_column,
    #                         capital_column, vat_column)
    add_columns_to_dataframe(df, registration_column, founders_column,None, capital_column,None, kved_column,
                             status_column, contacts_column, directors_column)
    print('Файл з результатами записаний. Робота успішно завершена.')
