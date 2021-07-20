import requests
from bs4 import BeautifulSoup
import pandas as pd
from functools import lru_cache

list_of_applicants = []


class competition:

    BVI = 'БВИ'
    OK = 'ОК'
    CK = 'ЦК'
    general = 'конкрус'
    contract = 'на контрактной основе'


def parse_table(table):
    res = pd.DataFrame()
    if table['EGE_ID']:
        res = res.append(
            pd.DataFrame([[table['university'],table['curse'], table['admission'], int(table['divorce_numb']), table['FIO'],
                           int(table['EGE_ID']), table['SOGL'], table['state']]],
                         columns=['university','curse', 'admission', 'divorce_numb', 'FIO', 'EGE_ID',
                                  'SOGL', 'state']),
            ignore_index=True)
    else:
        res = res.append(pd.DataFrame([[table['university'],table['curse'], table['admission'], int(table['divorce_numb']), table['FIO'],
                                        '', table['SOGL'], table['state']]],
                                      columns=['university','curse', 'admission', 'divorce_numb', 'FIO', 'EGE_ID',
                                               'SOGL', 'state']),
                         ignore_index=True)
    return (res)


@lru_cache(None)
def get_parser_page(html):
    r = requests.get(html)
    return r.text

def ITMO_PARSER(CURSE_ID='308'):
    global list_of_applicants

    soup = BeautifulSoup(get_parser_page('https://abit.itmo.ru/bachelor/rating_rank/all/' + CURSE_ID + "/"), 'html.parser')

    table = soup.find('table')  # , {'class': 'table-page__wrapper'})

    CURSE_NAME = soup.find('ul', {'class': 'crumbs_block'})
    CURSE = CURSE_NAME.text.split()[6]

    PLACES = soup.find('section', {'class': 'static-page-rule'}).text.split()
    curse_ind = PLACES.index(CURSE)
    free_ind = PLACES.index('бюджетных')
    cont_ind = PLACES.index('контрактных')
    free_pl = ' '.join(PLACES[curse_ind + 1:free_ind]).split('»')
    trs = table.find_all('tr')[2:]
    admission = ''
    for item in trs:
        abit_info = item.find_all()
        a = []
        for index, abit in enumerate(abit_info):
            if index == 0 and ' ' in abit.text:
                if abit.text == 'без вступительных испытаний':
                    admission = competition.BVI
                elif abit.text == 'на бюджетное место в пределах особой квоты':
                    admission = competition.OK
                elif abit.text == 'на бюджетное место в пределах целевой квоты':
                    admission = competition.CK
                elif abit.text == 'по общему конкурсу':
                    admission = competition.general
                elif abit.text == 'на контрактной основе':
                    admission = competition.contract
            else:
                a.append(abit.text)

        applicant = {
            'university': 'ITMO',
            'curse': CURSE,
            'admission': admission,
            'divorce_numb': a[-13],
            'FIO': a[-12],
            'EGE_ID': a[-7],
            'SOGL': a[-4],
            'state': a[-1]
        }

        if (applicant['admission'] != competition.contract and
            (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 257 or
             applicant['admission'] != competition.general)):
            list_of_applicants.append(applicant)



for i in range(308, 312):
    if i == 308:
        ITMO_PARSER(str(i))
    else:
        ITMO_PARSER(str(i))


def V(a):
    if a == competition.BVI:
        return 'background-color: %s' % 'red'
    elif a == competition.OK:
        return 'background-color: %s' % 'yellow'
    elif a == competition.CK:
        return 'background-color: %s' % 'orange'
    else:
        return ''

result=pd.DataFrame()

for i in list_of_applicants:
    res = parse_table(i)
    result = result.append(res, ignore_index=True)

res = result.style.applymap(V)

res.to_excel('CurseIfmo/all.xlsx', engine='openpyxl')
