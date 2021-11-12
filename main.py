import pandas as pd
from parsers import parser
from global_parametrs import competition, applicant_information
from time import time
import json

current_time = time()

def parse_table(table):

    table_result = pd.DataFrame()

    if not table['divorce_numb']:
        table['divorce_numb'] = 0

    if table['EGE_ID'] and table['EGE_ID'] != '-':
        table_result = table_result.append(pd.DataFrame(
                [[table['university'], table['curse'], table['curse_name'], table['admission'],
                  int(table['divorce_numb']), table['FIO'], int(table['EGE_ID']), table['SOGL'],
                  table['get_sogl'], table['consent_equals'], table['state']]],
                columns=['университет', 'курс', 'название курса', 'условие поступления', '№ заявления', 'ФИО/СНИЛС',
                         'ЕГЭ+ИД', 'согласие на зачисление', 'consent having', 'consent equals', 'статус']),
            ignore_index=True)
    else:
        table_result = table_result.append(pd.DataFrame(
            [[table['university'], table['curse'], table['curse_name'], table['admission'],
              int(table['divorce_numb']), table['FIO'], table['EGE_ID'], table['SOGL'],
              table['get_sogl'], table['consent_equals'], table['state']]],
            columns=['университет', 'курс', 'название курса', 'условие поступления', '№ заявления', 'ФИО/СНИЛС',
                     'ЕГЭ+ИД', 'согласие на зачисление', 'consent having', 'consent equals', 'статус']),
            ignore_index=True)

    return table_result


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
parse.spbpy()
parse.spbguty()
parse._guap()

list_of_applicants = parse.list_of_applicants

with open('file.json', 'w') as f:
    f.write(json.dumps(list_of_applicants))

for element in list_of_applicants:
    if element[applicant_information.FIO_SNILS] in parse.have_sogl:
        element[applicant_information.have_consent] = True
    if element[applicant_information.have_consent] == element[applicant_information.consent]:
        element[applicant_information.consents_equals] = True

result = pd.DataFrame()

for i in list_of_applicants:
    res = parse_table(i)
    result = result.append(res, ignore_index=True)

res = result.style.applymap(V)

res.to_excel('all.xlsx', engine='openpyxl')

print(parse.counter)
print(int((time()-current_time)//60), int((time()-current_time)%60))

