from bs4 import BeautifulSoup
import requests
from global_parametrs import competition


class parser:

    def __init__(self):
        self.list_of_applicants = []
        self.curses_itmo = [i for i in range(308, 337)]
        self.curses_with_informatics = ['01', '02', '03', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                                        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '35', '38', '44']
        self.curses_priority = ['01.03.02', '09.03.02', '09.03.03', '09.03.04', '10.03.01']
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

    def itmo(self):

        def PARSER(CURSE_ID='308'):

            soup = BeautifulSoup(requests.get('https://abit.itmo.ru/bachelor/rating_rank/all/' + CURSE_ID + "/",
                                              headers=self.headers).text, 'html.parser')

            table = soup.find('table')

            CURSE_NAME = soup.find('ul', {'class': 'crumbs_block'})
            CURSE = CURSE_NAME.text.split()[6]

            if CURSE.split('.')[0] not in self.curses_with_informatics:
                return False
            else:
                print('ИТМО -', CURSE)

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
                    'curse_name': '',
                    'admission': admission,
                    'divorce_numb': a[-13],
                    'FIO': a[-12],
                    'EGE_ID': a[-7],
                    'SOGL': a[-4].upper(),
                    'state': a[-1],
                    'get_sogl':False
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 250 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)

            return True

        def get_itmo_applicants():

            for curse in self.curses_itmo:
                PARSER(str(curse))

        get_itmo_applicants()

    def spbgy(self):

        def get_curses():
            req = requests.get('https://cabinet.spbu.ru/Lists/1k_EntryLists/index_comp_groups.html',
                               headers=self.headers)
            req.encoding = req.apparent_encoding
            soup = BeautifulSoup(req.text, 'html.parser')
            table = soup.find_all('a')
            return ['https://cabinet.spbu.ru/Lists/1k_EntryLists/'+element.attrs['href'] for element in table][1:]

        def PARSER(curse_link):

            req = requests.get(curse_link, headers=self.headers)
            req.encoding = req.apparent_encoding
            soup = BeautifulSoup(req.text, 'html.parser')

            curse_information = soup.find('p')
            curse_information = curse_information.text.split('\n')
            curse_information = [info.split(':')[-1] for info in curse_information]
            information = {'level':curse_information[1].strip(),
                                 'curse':curse_information[3].split()[0],
                                 'curse_info':''.join(curse_information[4].split()[1:]),
                                 'here':curse_information[5].strip(),
                                 'type':curse_information[6].strip(),
                                 'other':''.join(curse_information[7:])}

            if information['type'] == 'Госбюджетная':
                information.update({'places': curse_information[8]})
                information.update({'ok_places': curse_information[9]})
            else:
                information.update({'places': curse_information[8]})

            if information['level'] == 'бакалавриат' and information['curse'].split('.')[0] in self.curses_with_informatics\
                and information['here'] == 'очная' and 'ИКТ' in information['other']:
                print('СПбГУ - ',information['curse'])
            else:
                return False

            table = soup.find('table').find_all('tr')[1:]

            for element in table:
                applicants = element.find_all('td')

                if applicants[2].text == 'Без ВИ':
                    admission = competition.BVI
                elif information['type'] == 'Госбюджетная':
                    admission = competition.general
                elif information['type'] == 'Госбюджетная (Целевая квота)':
                    admission = competition.CK
                elif information['type'] == 'Госбюджетная (Особая квота)':
                    admission = competition.OK
                elif information['type'] == 'Договорная':
                    admission = competition.contract
                else:
                    admission = 'None'

                if information['type'] == 'Госбюджетная':
                    applicant = {
                        'university': 'SPBGY',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': applicants[3].text,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[4].text.split(',')[0],
                        'SOGL':applicants[10].text,
                        'state':applicants[12].text,
                        'get_sogl': False
                    }
                elif information['type'] == 'Договорная':
                    applicant = {
                        'university': 'SPBGY',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': 1,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[3].text.split(',')[0],
                        'SOGL': applicants[9].text.upper(),
                        'state': applicants[11].text,
                        'get_sogl': False
                    }
                else:
                    applicant = {
                        'university': 'SPBGY',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': 1,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[3].text.split(',')[0],
                        'SOGL':'НЕТ',
                        'state':applicants[10].text,
                        'get_sogl': False
                    }
                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 250 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)

            return True

        def get_spbgy_applicants():

            for curse in get_curses():
                PARSER(curse)


        get_spbgy_applicants()

if __name__ == '__main__':
    res = parser()
    res.spbgy()
    # print(res.list_of_applicants)