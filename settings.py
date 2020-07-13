#!/usr/bin/env python3
"""
A list of constants for parcing API-response and scraping.
"""

ENTRY_POINT = 'https://clarity-project.info/api/edr.info/'
BASE_URL = 'https://clarity-project.info/edr/'
INPUT_CSV = 'companies.csv'
OUTPUT_CSV = 'output.csv'
DATETIMEFORMAT = '%Y-%m-%d'
API_KEY = ''

EDRPOU_COLUMN_HEADER = 'Ідентифікаційний код (для фіз. осіб)/Код ЄДРПОУ (для юр. осіб)'
REGISTRATION_COLUMN_HEADER = 'Дата реєстрації компанії'
DIFFERENCE_COLUMN_HEADER = 'Різниця між внеском і реєстрацією'
DONATION_COLUMN_HEADER = 'Дата надходження внеску'
CAPITAL_COLUMN_HEADER = 'Статутний капітал'
BENEFICIARY_COLUMN_HEADER = 'Бенефіціар'
FOUNDER_COLUMN_HEADER = 'Засновник'
VAT_COLUMN_HEADER = 'Платник податків'

EDR_DATA_JSON_KEY = 'edr_data'
REGISTRATION_JSON_KEY = 'registration'
DATE_JSON_KEY = 'Date'
FOUNDERS_JSON_KEY = 'founders'
BENEFICIARIES_JSON_KEY = 'beneficiaries'
NAME_JSON_KEY = 'Name'
SHARE_CAPITAL_JSON_KEY = 'capital'
VAT_JSON_KEY = 'vat'

REGISTRATION_REGEXP = '^\n\d{2}\.\d{2}\.\d{4}\n$'
