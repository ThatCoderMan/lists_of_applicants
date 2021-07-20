import requests
from bs4 import BeautifulSoup
import pandas as pd
from parsers import parser
from global_parametrs import competition


def parse_table(table):

    res = pd.DataFrame()
    if not table['divorce_numb']:
        table['divorce_numb'] = 0
    if table['EGE_ID']:
        res = res.append(
            pd.DataFrame(
                [[table['university'], table['curse'], table['admission'], int(table['divorce_numb']), table['FIO'],
                  int(table['EGE_ID']), table['SOGL'], table['state']]],
                columns=['university', 'curse', 'admission', 'divorce_numb', 'FIO', 'EGE_ID',
                         'SOGL', 'state']),
            ignore_index=True)
    else:
        res = res.append(pd.DataFrame(
            [[table['university'], table['curse'], table['admission'], int(table['divorce_numb']), table['FIO'],
              '', table['SOGL'], table['state']]],
            columns=['university', 'curse', 'admission', 'divorce_numb', 'FIO', 'EGE_ID',
                     'SOGL', 'state']),
                         ignore_index=True)
    return (res)
def V(a):
    if a == competition.BVI:
        return 'background-color: %s' % 'red'
    elif a == competition.OK:
        return 'background-color: %s' % 'yellow'
    elif a == competition.CK:
        return 'background-color: %s' % 'orange'
    else:
        return ''


parse = parser()

parse.itmo()
parse.spbgy()

list_of_applicants = parse.list_of_applicants


result = pd.DataFrame()

for i in list_of_applicants:
    res = parse_table(i)
    result = result.append(res, ignore_index=True)

res = result.style.applymap(V)

res.to_excel('all.xlsx', engine='openpyxl')
