import json
import pandas as pd

with open('file.json', 'r') as f:
    list_of_applicants = json.load(f)

# print(list_of_applicants[100])

curses = {'ИТМО 11.03.03': [],
          'ГУАП 09.03.01': [],
          'ГУАП 09.03.03': [],
          'ГУАП 10.03.01': [],
          'Бонч 09.03.02': [],
          'Бонч 10.03.01': []}

curses_names = {'ИТМО 10.03.01': [],
                'ИТМО 11.03.02': [],
                'ИТМО 11.03.03': [],
                'СПбПУ 09.03.03': [],
                'СПбПУ 01.03.02': [],
                'СПбПУ 09.03.02': [],
                'СПбПУ 02.03.03': [],
                'ЛЭТИ 01.03.02': [],
                'ЛЭТИ 09.03.01 ИИ': [],
                'ЛЭТИ 09.03.01 КМиП': [],
                'ЛЭТИ 09.03.02': [],
                'ЛЭТИ 09.03.04': [],
                'ЛЭТИ 10.05.01': [],
                'ЛЭТИ 12.03.01': [],
                'ГУАП 02.03.03': [],
                'ГУАП 09.03.01': [],
                'ГУАП 09.03.03': [],
                'ГУАП 09.03.04': [],
                'ГУАП 10.03.01': [],
                'Бонч 09.03.04': [],
                'Бонч 09.03.02': [],
                'Бонч 10.03.01': []}

curses_names_sogl = {'ИТМО 10.03.01': [],
                     'ИТМО 11.03.02': [],
                     'ИТМО 11.03.03': [],
                     'СПбПУ 09.03.03': [],
                     'СПбПУ 01.03.02': [],
                     'СПбПУ 09.03.02': [],
                     'СПбПУ 02.03.03': [],
                     'ЛЭТИ 01.03.02': [],
                     'ЛЭТИ 09.03.01 ИИ': [],
                     'ЛЭТИ 09.03.01 КМиП': [],
                     'ЛЭТИ 09.03.02': [],
                     'ЛЭТИ 09.03.04': [],
                     'ЛЭТИ 10.05.01': [],
                     'ЛЭТИ 12.03.01': [],
                     'ГУАП 02.03.03': [],
                     'ГУАП 09.03.01': [],
                     'ГУАП 09.03.03': [],
                     'ГУАП 09.03.04': [],
                     'ГУАП 10.03.01': [],
                     'Бонч 09.03.04': [],
                     'Бонч 09.03.02': [],
                     'Бонч 10.03.01': []}

curses_info = {'ИТМО 10.03.01': ['ИТМО', '10.03.01', 85, 71, None, None, None, 8, 6, 0, 259, 'ИМР'],
               'ИТМО 11.03.02': ['ИТМО', '11.03.02', 80, 76, None, None, None, 0, 3, 1, 259, 'ИМР'],
               'ИТМО 11.03.03': ['ИТМО', '11.03.03', 15, 15, None, None, None, 0, 0, 0, 259, 'ИМР'],
               'СПбПУ 09.03.03': ['СПбПУ', '09.03.03', 30, 17, 1174, 26, -9, 7, 3, 3, 260, 'МИР'],
               'СПбПУ 01.03.02': ['СПбПУ', '01.03.02', 55, 31, 1184, 37, -6, 19, 1, 4, 260, 'МИР'],
               'СПбПУ 09.03.02': ['СПбПУ', '09.03.02', 22, 20, 725, 20, 0, 0, 0, 2, 260, 'МИР'],
               'СПбПУ 02.03.03': ['СПбПУ', '02.03.03', 36, 35, 525, 37, -2, 1, 0, 0, 260, 'МИР'],
               'ЛЭТИ 01.03.02': ['ЛЭТИ', '01.03.02', 58, 49, None, None, None, 3, 2, 4, 251, 'МИР'],
               'ЛЭТИ 09.03.01 ИИ': ['ЛЭТИ', '09.03.01 ИИ', 93, 84, None, None, None, 0, 4, 5, 251, 'МИР'],
               'ЛЭТИ 09.03.01 КМиП': ['ЛЭТИ', '09.03.01 КМиП', 47, 44, None, None, None, 1, 1, 1, 251, 'МИР'],
               'ЛЭТИ 09.03.02': ['ЛЭТИ', '09.03.02', 100, 88, None, None, None, 1, 2, 9, 251, 'МИР'],
               'ЛЭТИ 09.03.04': ['ЛЭТИ', '09.03.04', 40, 30, None, None, None, 4, 2, 4, 251, 'МИР'],
               'ЛЭТИ 10.05.01': ['ЛЭТИ', '10.05.01', 60, 50, None, None, None, 2, 2, 6, 251, 'МИР'],
               'ЛЭТИ 12.03.01': ['ЛЭТИ', '12.03.01', 137, 131, None, None, None, 0, 1, 5, 251, 'МИР'],
               'ГУАП 02.03.03': ['ГУАП', '02.03.03', 25, 24, None, None, None, 1, 0, 0, 260, 'МРИ'],
               'ГУАП 09.03.01': ['ГУАП', '09.03.01', 120, 110, None, None, None, 1, 4, 5, 260, 'МРИ'],
               'ГУАП 09.03.03': ['ГУАП', '09.03.03', 140, 134, None, None, None, 0, 6, 0, 260, 'МРИ'],
               'ГУАП 09.03.04': ['ГУАП', '09.03.04', 50, 45, None, None, None, 1, 2, 2, 260, 'МРИ'],
               'ГУАП 10.03.01': ['ГУАП', '10.03.01', 50, 44, None, None, None, 0, 3, 3, 260, 'МРИ'],
               'Бонч 09.03.04': ['Бонч', '09.03.04', 64, 56, 965, 48, 8, 0, 4, 4, 250, 'МРИ'],
               'Бонч 09.03.02': ['Бонч', '09.03.02', 41, 36, 620, 13, 23, 0, 4, 2, 250, 'МРИ'],
               'Бонч 10.03.01': ['Бонч', '10.03.01', 75, 62, 586, 26, 36, 0, 8, 5, 250, 'МРИ']}

for applicant in list_of_applicants:
    name = applicant['university'] + ' ' + applicant['curse']
    if applicant['admission'] == 'конкрус':
        if name in curses.keys():
            curses[name].append(applicant)

for curse in curses:

    curses[curse] = sorted(curses[curse], key=lambda i: (i['EGE_ID'], i['EGE']), reverse=True)

    for names in curses[curse]:
        curses_names[curse].append(names['FIO'])
        if names['SOGL'] or names['FIO'] in ('Березин Артемий Валерьевич', '138-538-605'):
            curses_names_sogl[curse].append(names['FIO'])

    try:
        print(curse, curses_names[curse].index('Березин Артемий Валерьевич'),
              curses_names_sogl[curse].index('Березин Артемий Валерьевич') + 1)
        curses_info[curse][4] = curses_names[curse].index('Березин Артемий Валерьевич') + 1
        curses_info[curse][5] = curses_names_sogl[curse].index('Березин Артемий Валерьевич') + 1
        curses_info[curse][6] = curses_info[curse][3] - curses_info[curse][5]
    except:

        try:
            print(curse, curses_names[curse].index('138-538-605'),
                  curses_names_sogl[curse].index('138-538-605') + 1)
            curses_info[curse][4] = curses_names[curse].index('138-538-605') + 1
            curses_info[curse][5] = curses_names_sogl[curse].index('138-538-605') + 1
            curses_info[curse][6] = curses_info[curse][3] - curses_info[curse][5]
        except:
            print(curse, 'ERROR')

table_result = pd.DataFrame()

for curse in curses:
    print(curses_info[curse])
    table_result = table_result.append(pd.DataFrame(
        [curses_info[curse]],
        columns=['вуз', 'курс', 'места', 'осталось', 'в списке', 'по заявлению', 'остаток', 'БВИ', 'ОК', 'ЦК', 'ЕГЭ',
                 'ЕГЭ']),
        ignore_index=True)

table_result.to_excel('new.xlsx', engine='openpyxl')