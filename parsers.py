from bs4 import BeautifulSoup
import requests
from global_parametrs import competition


class parser:

    def __init__(self):
        self.list_of_applicants = []

    def itmo(self):

        def ITMO_PARSER(CURSE_ID='308'):

            soup = BeautifulSoup(requests.get('https://abit.itmo.ru/bachelor/rating_rank/all/' + CURSE_ID + "/").text,
                                 'html.parser')

            table = soup.find('table')

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
                    self.list_of_applicants.append(applicant)

        def get_itmo_applicants():
            curses = [i for i in range(308, 337)]

            for curse in curses:
                ITMO_PARSER(str(curse))

        get_itmo_applicants()




