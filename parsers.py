from bs4 import BeautifulSoup
import requests
from global_parametrs import competition, applicant_information
from time import sleep
from os import system

class parser:

    def __init__(self):
        self.list_of_applicants = []
        self.curses_itmo = [i for i in range(308, 337)]
        self.curses_with_informatics = ['01', '02', '03', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                                        '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '35', '38', '44']
        self.curses_priority = ['01.03.02', '09.03.02', '09.03.03', '09.03.04', '10.03.01']
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/91.0.4472.164 Safari/537.36'}
        self.have_sogl = []
        self.counter = 0

    def current(self):

        for i in range(100000):

            link = 'https://abit.itmo.ru/bachelor/competitive/315/'

            soup = BeautifulSoup(requests.get('https://abit.itmo.ru/bachelor/competitive/315/').text, 'html.parser')
            table = soup.find('div', {'class':'table-page__wrapper'}).find_all('tr')

            time = soup.find('div',{'class':'main page table-page'}).find('p', {'style':'padding-top: 20px; font-weight: bold;'}).text
            
            for ind,tr in enumerate(table[5:6+14]):
                if ind == 0:
                    a = [b.text.strip() for b in tr.find_all('td')][1:]
                else:
                    a = [b.text.strip() for b in tr.find_all('td')]
                if a[1] == '138-538-605 88':
                    print(ind+1,'ME',*a[1:], sep = '\t')
                else:
                    print(ind+1,*a, sep = '\t')
            print(time)
            sleep(60)
            system('cls')

            
    def itmo(self):

        def PARSER(CURSE_ID='308'):

            soup = BeautifulSoup(requests.get('https://abit.itmo.ru/bachelor/rating_rank/all/' + CURSE_ID + "/",
                                              headers=self.headers).text, 'html.parser')

            table = soup.find('table')

            CURSE_NAME = soup.find('ul', {'class': 'crumbs_block'})
            CURSE = CURSE_NAME.text.split()[6]
            CURSE_NAME = ' '.join(CURSE_NAME.text.split()[7:-2])[1:-1]
            if CURSE.split('.')[0] not in self.curses_with_informatics:
                return False
            else:
                print('???????? -', CURSE)

            PLACES = soup.find('section', {'class': 'static-page-rule'}).text.split()
            curse_ind = PLACES.index(CURSE)
            free_ind = PLACES.index('??????????????????')
            cont_ind = PLACES.index('??????????????????????')
            free_pl = ' '.join(PLACES[curse_ind + 1:free_ind]).split('??')
            trs = table.find_all('tr')[2:]
            admission = ''
            for item in trs:
                self.counter += 1

                abit_info = item.find_all()
                a = []
                for index, abit in enumerate(abit_info):
                    if index == 0 and ' ' in abit.text:
                        if abit.text == '?????? ?????????????????????????? ??????????????????':
                            admission = competition.BVI
                        elif abit.text == '???? ?????????????????? ?????????? ?? ???????????????? ???????????? ??????????':
                            admission = competition.OK
                        elif abit.text == '???? ?????????????????? ?????????? ?? ???????????????? ?????????????? ??????????':
                            admission = competition.CK
                        elif abit.text == '???? ???????????? ????????????????':
                            admission = competition.general
                        elif abit.text == '???? ?????????????????????? ????????????':
                            admission = competition.contract
                    else:
                        a.append(abit.text)

                if a[-4] == '????':
                    sogl = True
                else:
                    sogl = False

                if not a[4]:
                    a[4] = 0

                if not a[5]:
                    a[5] = 0

                if not a[6]:
                    a[6] = 0

                applicant = {
                    'university': '????????',
                    'curse': CURSE,
                    'curse_name': CURSE_NAME,
                    'admission': admission,
                    'divorce_numb': a[-13],
                    'FIO': a[-12],
                    'EGE_ID': a[-7],
                    'SOGL': sogl,
                    'state': a[-1],
                    'get_sogl': False,
                    'consent_equals': False,
                    'EGE': [int(a[4]), int(a[5]), int(a[6])]
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 249 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])

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
            return ['https://cabinet.spbu.ru/Lists/1k_EntryLists/' + element.attrs['href'] for element in table][1:]

        def PARSER(curse_link):

            req = requests.get(curse_link, headers=self.headers)
            req.encoding = req.apparent_encoding
            soup = BeautifulSoup(req.text, 'html.parser')

            curse_information = soup.find('p')
            curse_information = curse_information.text.split('\n')
            curse_information = [info.split(':')[-1] for info in curse_information]
            information = {'level': curse_information[1].strip(),
                           'curse': curse_information[3].split()[0],
                           'curse_info': ''.join(curse_information[4].split()[1:]),
                           'here': curse_information[5].strip(),
                           'type': curse_information[6].strip(),
                           'other': ''.join(curse_information[7:])}

            if information['type'] == '????????????????????????':
                information.update({'places': curse_information[8]})
                information.update({'ok_places': curse_information[9]})
            else:
                information.update({'places': curse_information[8]})

            if information['level'] == '??????????????????????' and \
                    information['curse'].split('.')[0] in self.curses_with_informatics \
                    and information['here'] == '??????????' \
                    and '??????' in information['other']:
                print('?????????? - ', information['curse'])
            else:
                return False

            table = soup.find('table').find_all('tr')[1:]

            for element in table:
                self.counter += 1
                applicants = element.find_all('td')

                if applicants[2].text == '?????? ????':
                    admission = competition.BVI
                elif information['type'] == '????????????????????????':
                    admission = competition.general
                elif information['type'] == '???????????????????????? (?????????????? ??????????)':
                    admission = competition.CK
                elif information['type'] == '???????????????????????? (???????????? ??????????)':
                    admission = competition.OK
                elif information['type'] == '????????????????????':
                    admission = competition.contract
                else:
                    admission = 'None'

                if information['type'] == '????????????????????????':

                    if applicants[10].text == '????':
                        sogl = True
                    else:
                        sogl = False

                    applicant = {
                        'university': '??????????',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': applicants[3].text,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[4].text.split(',')[0],
                        'SOGL': sogl,
                        'state': applicants[12].text,
                        'get_sogl': False,
                        'consent_equals': False
                    }
                elif information['type'] == '????????????????????':

                    if applicants[9].text == '????':
                        sogl = True
                    else:
                        sogl = False

                    applicant = {
                        'university': '??????????',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': 1,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[3].text.split(',')[0],
                        'SOGL': sogl,
                        'state': applicants[11].text,
                        'get_sogl': False,
                        'consent_equals': False
                    }
                else:
                    applicant = {
                        'university': '??????????',
                        'curse': information['curse'],
                        'curse_name': information['curse_info'],
                        'admission': admission,
                        'divorce_numb': 1,
                        'FIO': applicants[1].text.split()[0],
                        'EGE_ID': applicants[3].text.split(',')[0],
                        'SOGL': False,
                        'state': applicants[10].text,
                        'get_sogl': False,
                        'consent_equals': False
                    }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 249 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])

            return True

        def get_spbgy_applicants():

            for curse in get_curses():
                PARSER(curse)

        get_spbgy_applicants()

    def spbpy(self):

        def get_curses():
            links = {}

            level_education = 'b7af2da3-5972-11eb-803a-0050569f980a'
            report_option = '25c3ee87-ef95-11eb-8045-0050569f980a'
            scenario = 'e816affc-5f19-11eb-803a-0050569f980a'
            scenarioN = '????????????%20??????????????????????%20????%20????????????????????%20????????????????????????/' \
                        '????????????????????????%20??%202021%20????????%20??????%20??????????????%20????'
            form_education = 'a5ae897b-5972-11eb-803a-0050569f980a'

            basis_admissions = {"?????????????????? ????????????": "a5ae8977-5972-11eb-803a-0050569f980a",
                                "????????????????": "a5ae8978-5972-11eb-803a-0050569f980a",
                                "???????????????? ????????????": "a5ae897e-5972-11eb-803a-0050569f980a",
                                "?????????????? ??????????": "a5ae8979-5972-11eb-803a-0050569f980a"}

            faculty = '21916fb8-5ef2-11eb-803a-0050569f980a'
            directions = {'02.03.01 ???????????????????? ?? ???????????????????????? ??????????':
                              'fe0a43fc-5f1a-11eb-803a-0050569f980a',
                          "02.03.02 ?????????????????????????????? ?????????????????????? ?? ???????????????????????????? ????????????????????":
                              'fe0a43fd-5f1a-11eb-803a-0050569f980a',
                          "02.03.03 ???????????????????????????? ?????????????????????? ?? ?????????????????????????????????? ???????????????????????????? ????????????":
                              '041285e7-5f1b-11eb-803a-0050569f980a',
                          "09.03.01 ?????????????????????? ?? ???????????????????????????? ??????????????":
                              "0ddbe522-5f1b-11eb-803a-0050569f980a",
                          "09.03.02 ???????????????????????????? ?????????????? ?? ????????????????????":
                              "0ddbe523-5f1b-11eb-803a-0050569f980a",
                          "09.03.03 ???????????????????? ??????????????????????":
                              "13ff1805-5f1b-11eb-803a-0050569f980a",
                          "09.03.04 ?????????????????????? ??????????????????":
                              "13ff1806-5f1b-11eb-803a-0050569f980a",
                          "27.03.01 ???????????????????????????? ?? ????????????????????":
                              "104b85b4-9c5e-11eb-803c-0050569f980a",
                          "27.03.02 ???????????????????? ??????????????????":
                              "4f707e3c-5f1b-11eb-803a-0050569f980a",
                          "27.03.03 ?????????????????? ???????????? ?? ????????????????????":
                              "57918c96-5f1b-11eb-803a-0050569f980a",
                          "27.03.04 ???????????????????? ?? ?????????????????????? ????????????????":
                              "57918c97-5f1b-11eb-803a-0050569f980a",
                          "27.03.05 ????????????????????":
                              '57918c98-5f1b-11eb-803a-0050569f980a'}

            for curse_name, direction in directions.items():
                curse_id = curse_name.split()[0]
                curse = ' '.join(curse_name.split()[1:])
                for basis_admission_name, basis_admission in basis_admissions.items():
                    links.update({'&'.join([curse_id, curse, basis_admission_name]):
                                      f'https://enroll.spbstu.ru/ajax/interactive_detail?report_option={report_option}'
                                      f'&scenario={scenario}&scenarioN={scenarioN}&level_education={level_education}'
                                      f'&form_education={form_education}&basis_admission={basis_admission}'
                                      f'|false&faculty={faculty}&direction={direction}&'
                                      f'profile=00000000-0000-0000-0000-000000000000&actions=list_applicants'})

            faculty = "5c353740-5ef2-11eb-803a-0050569f980a"
            directions = {"01.03.02 ???????????????????? ???????????????????? ?? ??????????????????????":
                              "fe0a43f9-5f1a-11eb-803a-0050569f980a",
                          "01.03.03 ???????????????? ?? ???????????????????????????? ??????????????????????????":
                              "fe0a43fa-5f1a-11eb-803a-0050569f980a",
                          "15.03.03 ???????????????????? ????????????????":
                              "2ae852e1-5f1b-11eb-803a-0050569f980a"}

            for curse_name, direction in directions.items():
                curse_id = curse_name.split()[0]
                curse = ' '.join(curse_name.split()[1:])
                for basis_admission_name, basis_admission in basis_admissions.items():
                    links.update({'&'.join([curse_id, curse, basis_admission_name]):
                                      f'https://enroll.spbstu.ru/ajax/interactive_detail?report_option={report_option}'
                                      f'&scenario={scenario}&scenarioN={scenarioN}&level_education={level_education}'
                                      f'&form_education={form_education}&basis_admission={basis_admission}'
                                      f'|false&faculty={faculty}&direction={direction}&'
                                      f'profile=00000000-0000-0000-0000-000000000000&actions=list_applicants'})

            links.update({
                             '10.03.01&???????????????????????????? ????????????????????????&?????????????????? ????????????': "https://enroll.spbstu.ru/ajax/interactive_detail?report_option=25c3ee87-ef95-11eb-8045-0050569f980a&scenario=e816affc-5f19-11eb-803a-0050569f980a&scenarioN=%D0%A1%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%20%D0%BF%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%D1%8E%D1%89%D0%B8%D1%85%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D0%BC%20%D0%B1%D0%B0%D0%BA%D0%B0%D0%BB%D0%B0%D0%B2%D1%80%D0%B8%D0%B0%D1%82%D0%B0/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%82%D0%B5%D1%82%D0%B0%20%D0%B2%202021%20%D0%B3%D0%BE%D0%B4%D1%83%20%D0%B4%D0%BB%D1%8F%20%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%20%D0%A0%D0%A4&level_education=b7af2da3-5972-11eb-803a-0050569f980a&form_education=a5ae897b-5972-11eb-803a-0050569f980a&basis_admission=a5ae8977-5972-11eb-803a-0050569f980a|false&faculty=78a189ab-5ef2-11eb-803a-0050569f980a&direction=6c00ac84-986f-11eb-803c-0050569f980a&profile=00000000-0000-0000-0000-000000000000&actions=list_applicants"})
            links.update({
                '10.03.01&???????????????????????????? ????????????????????????&???????????????? ????????????': "https://enroll.spbstu.ru/ajax/interactive_detail?report_option=25c3ee87-ef95-11eb-8045-0050569f980a&scenario=e816affc-5f19-11eb-803a-0050569f980a&scenarioN=%D0%A1%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%20%D0%BF%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%D1%8E%D1%89%D0%B8%D1%85%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D0%BC%20%D0%B1%D0%B0%D0%BA%D0%B0%D0%BB%D0%B0%D0%B2%D1%80%D0%B8%D0%B0%D1%82%D0%B0/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%82%D0%B5%D1%82%D0%B0%20%D0%B2%202021%20%D0%B3%D0%BE%D0%B4%D1%83%20%D0%B4%D0%BB%D1%8F%20%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%20%D0%A0%D0%A4&level_education=b7af2da3-5972-11eb-803a-0050569f980a&form_education=a5ae897b-5972-11eb-803a-0050569f980a&basis_admission=a5ae897e-5972-11eb-803a-0050569f980a|true&faculty=78a189ab-5ef2-11eb-803a-0050569f980a&direction=6c00ac84-986f-11eb-803c-0050569f980a&profile=00000000-0000-0000-0000-000000000000&actions=list_applicants"})
            links.update({
                '10.03.01&???????????????????????????? ????????????????????????&?????????????? ??????????': "https://enroll.spbstu.ru/ajax/interactive_detail?report_option=25c3ee87-ef95-11eb-8045-0050569f980a&scenario=e816affc-5f19-11eb-803a-0050569f980a&scenarioN=%D0%A1%D0%BF%D0%B8%D1%81%D0%BA%D0%B8%20%D0%BF%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0%D1%8E%D1%89%D0%B8%D1%85%20%D0%BF%D0%BE%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D0%BC%20%D0%B1%D0%B0%D0%BA%D0%B0%D0%BB%D0%B0%D0%B2%D1%80%D0%B8%D0%B0%D1%82%D0%B0/%D1%81%D0%BF%D0%B5%D1%86%D0%B8%D0%B0%D0%BB%D0%B8%D1%82%D0%B5%D1%82%D0%B0%20%D0%B2%202021%20%D0%B3%D0%BE%D0%B4%D1%83%20%D0%B4%D0%BB%D1%8F%20%D0%B3%D1%80%D0%B0%D0%B6%D0%B4%D0%B0%D0%BD%20%D0%A0%D0%A4&level_education=b7af2da3-5972-11eb-803a-0050569f980a&form_education=a5ae897b-5972-11eb-803a-0050569f980a&basis_admission=a5ae8979-5972-11eb-803a-0050569f980a|false&faculty=78a189ab-5ef2-11eb-803a-0050569f980a&direction=6c00ac84-986f-11eb-803c-0050569f980a&profile=00000000-0000-0000-0000-000000000000&actions=list_applicants"})

            return links

        def PARSER(curse_link, url):

            print('?????????? -', curse_link[0])
            req = requests.get(url, headers=self.headers).json()

            if req['data']:
                applicants = req['data']['list_applicants']

                for applicant in applicants:
                    self.counter += 1

                    if applicant['??????????????????????????????'] == '?????? ?????????????????????????? ??????????????????':
                        admission = competition.BVI
                    elif applicant['??????????????????????????????'] == '???? ?????????? ????????????????????':
                        if curse_link[2] == '????????????????':
                            admission = competition.contract
                        elif curse_link[2] == '?????????????? ??????????':
                            admission = competition.CK
                        elif curse_link[2] == '?????????????????? ????????????':
                            admission = competition.general
                        else:
                            admission = 'None'
                    elif applicant['??????????????????????????????'] == '????????, ?????????????? ???????????? ??????????':
                        admission = competition.OK
                    else:
                        admission = 'None'

                    if applicant['????????????????????????????????????????'] == '????':
                        sogl = True
                    else:
                        sogl = False

                    if '??????????????1' not in applicant or not applicant['??????????????1']:
                        applicant['??????????????1'] = 0

                    if '??????????????2' not in applicant or not applicant['??????????????2']:
                        applicant['??????????????2'] = 0

                    if '??????????????3' not in applicant or not applicant['??????????????3']:
                        applicant['??????????????3'] = 0

                    if applicant['??????????????????????????']:
                        applicant = {
                            'university': '??????????',
                            'curse': curse_link[0],
                            'curse_name': curse_link[1],
                            'admission': admission,
                            'divorce_numb': 1,
                            'FIO': applicant['??????????????????????????'].split()[0],
                            'EGE_ID': applicant['??????????????????????'],
                            'SOGL': sogl,
                            'state': applicant['??????????????????'],
                            'get_sogl': False,
                            'consent_equals': False,
                            'EGE': [int(applicant['??????????????1']), int(applicant['??????????????2']), int(applicant['??????????????3'])]
                        }

                        if (applicant['admission'] != competition.contract and
                                (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 249 or
                                 applicant['admission'] != competition.general)):
                            self.list_of_applicants.append(applicant)
                            if applicant['SOGL']:
                                self.have_sogl.append(applicant['FIO'])

                return True

        def get_spbgy_applicants():

            for curse, url in get_curses().items():
                PARSER(curse.split('&'), url)

        return get_spbgy_applicants()

    def spbguty(self):

        def get_curses():

            main_link = 'https://etu.ru/ru/abiturientam/priyom-na-1-y-kurs/podavshie-zayavlenie/ochnaya/'
            types = ['byudzhet']  # , 'kontrakt']
            links = ['radiotehnika-sistemy-kompyuternogo-zreniya',
                     'radiotehnika',
                     'infokommunikacionnye-tehnologii-i-sistemy-svyazi',
                     'konstruirovanie-i-tehnologiya-elektronnyh-sredstv',
                     'elektronika-i-nanoelektronika-ee',
                     'elektronika-i-nanoelektronika-oif',
                     'elektronika-i-nanoelektronika-epiu',
                     'elektronika-i-nanoelektronika-te',
                     'nanotehnologii-i-mikrosistemnaya-tehnika',
                     'prikladnaya-matematika-i-informatika',
                     'informatika-i-vychislitelnaya-tehnika-ii',
                     'informatika-i-vychislitelnaya-tehnika-kmip',
                     'informacionnye-sistemy-i-tehnologii',
                     'programmnaya-inzheneriya',
                     'kompyuternaya-bezopasnost',
                     'sistemnyy-analiz-i-upravlenie',
                     'upravlenie-v-tehnicheskih-sistemah',
                     'upravlenie-v-tehnicheskih-sistemah-fea',
                     'elektroenergetika-i-elektrotehnika',
                     'priborostroenie',
                     'biotehnicheskie-sistemy-i-tehnologii',
                     'tehnosfernaya-bezopasnost',
                     'tehnosfernaya-bezopasnost',
                     'upravlenie-kachestvom',
                     'innovatika',
                     'lingvistika']

            return [main_link + type_ + '/' + link for type_ in types for link in links]

        def PARSER(url):

            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'html.parser')

            information = soup.find('span', {'class': 'B_currentCrumb'})

            curse_id = information.text.split()[0]
            curse = ' '.join(information.text.split()[1:])

            table = soup.find('table').find_all('tr')[2:]

            print('???????? -', curse_id)

            for element in table:
                self.counter += 1
                applicant_information = element.find_all('td')
                applicant = []
                for applicant_info in applicant_information:
                    applicant.append(applicant_info.text)

                if applicant[3] == '??????':
                    admission = competition.BVI
                elif applicant[3] == '????':
                    admission = competition.OK
                elif applicant[3] == '????':
                    admission = competition.general
                elif applicant[3] == '??':
                    admission = competition.contract
                elif applicant[3] == '????':
                    admission = competition.CK
                else:
                    admission = 'None'

                if applicant[-1] == '????':
                    sogl = True
                else:
                    sogl = False

                if not applicant[5]:
                    applicant[5] = 0

                if not applicant[6]:
                    applicant[6] = 0

                if not applicant[7]:
                    applicant[7] = 0

                applicant = {
                    'university': '????????',
                    'curse': curse_id,
                    'curse_name': curse,
                    'admission': admission,
                    'divorce_numb': applicant[2],
                    'FIO': applicant[1].split()[0],
                    'EGE_ID': applicant[4],
                    'SOGL': sogl,
                    'state': '???????????????????????????????? ?????????? - ' + applicant[9],
                    'get_sogl': False,
                    'consent_equals': False,
                    'EGE': [int(applicant[5]), int(applicant[6]), int(applicant[7])]
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] != '-' and int(applicant['EGE_ID']) > 249 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])
            return True

        def get_spbgy_applicants():

            for url in get_curses():
                PARSER(url)

        return get_spbgy_applicants()

    def _guap(self):

        def get_curses():

            links = ['https://priem.guap.ru/lists/List_Main_6_70_30',
                     'https://priem.guap.ru/lists/List_Main_6_71_30',
                     'https://priem.guap.ru/lists/List_Main_6_74_30',
                     'https://priem.guap.ru/lists/List_Main_6_75_30',
                     'https://priem.guap.ru/lists/List_Main_6_76_30',
                     'https://priem.guap.ru/lists/List_Main_6_78_30',
                     'https://priem.guap.ru/lists/List_Main_6_79_30',
                     'https://priem.guap.ru/lists/List_Main_6_80_30',
                     'https://priem.guap.ru/lists/List_Main_6_81_30',
                     'https://priem.guap.ru/lists/List_Main_6_82_30',
                     'https://priem.guap.ru/lists/List_Main_6_83_30',
                     'https://priem.guap.ru/lists/List_Main_6_84_30',
                     'https://priem.guap.ru/lists/List_Main_6_85_30',
                     'https://priem.guap.ru/lists/List_Main_6_86_30',
                     'https://priem.guap.ru/lists/List_Main_6_87_30',
                     'https://priem.guap.ru/lists/List_Main_6_91_30',
                     'https://priem.guap.ru/lists/List_Main_6_92_30',
                     'https://priem.guap.ru/lists/List_Main_6_93_30',
                     'https://priem.guap.ru/lists/List_Main_6_95_30',
                     'https://priem.guap.ru/lists/List_Main_6_96_30']

            return links

        def PARSER(url):

            req = requests.get(url, headers=self.headers)

            req.encoding = req.apparent_encoding

            soup = BeautifulSoup(req.text, 'html.parser')
            information = soup.find_all('div', {'class': 'container'})[2].find('div').find('h3')

            curse_id = information.text.split()[0]
            curse = ' '.join(information.text.split()[1:])
            print('???????? -', curse_id)

            table = soup.find('table', {'class': 'table table_stat'}).find_all('tr')
            for item in table[1:]:
                i = [j.text for j in item]

                admission = competition.general

                if i[-2] == '????':
                    sogl = True
                else:
                    sogl = False

                ege = i[2].split('\n')[:3]
                for j in range(3):
                    ege[j] = ege[j].split()[-1]
                    if ege[j]:
                        ege[j] = int(ege[j])
                    else:
                        ege[j] = 0

                applicant = {
                    'university': '????????',
                    'curse': curse_id,
                    'curse_name': curse,
                    'admission': admission,
                    'divorce_numb': 1,
                    'FIO': i[1].split()[0],
                    'EGE_ID': i[int(5)],
                    'SOGL': sogl,
                    'state': '',
                    'get_sogl': False,
                    'consent_equals': False,
                    'EGE': [ege]
                }

                if (applicant['EGE_ID'] != '-' and int(applicant['EGE_ID']) > 249 or
                        applicant['admission'] != competition.general):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])
            return True

        def get_spbgy_applicants():

            for url in get_curses():
                PARSER(url)

        return get_spbgy_applicants()

    def bonch(self):

        def PARSER(CURSE_ID='308'):

            soup = BeautifulSoup(requests.get('https://abit.itmo.ru/bachelor/rating_rank/all/' + CURSE_ID + "/",
                                              headers=self.headers).text, 'html.parser')

            table = soup.find('table')

            CURSE_NAME = soup.find('ul', {'class': 'crumbs_block'})
            CURSE = CURSE_NAME.text.split()[6]
            CURSE_NAME = ' '.join(CURSE_NAME.text.split()[7:-2])[1:-1]
            if CURSE.split('.')[0] not in self.curses_with_informatics:
                return False
            else:
                print('???????? -', CURSE)

            PLACES = soup.find('section', {'class': 'static-page-rule'}).text.split()
            curse_ind = PLACES.index(CURSE)
            free_ind = PLACES.index('??????????????????')
            cont_ind = PLACES.index('??????????????????????')
            free_pl = ' '.join(PLACES[curse_ind + 1:free_ind]).split('??')
            trs = table.find_all('tr')[2:]
            admission = ''
            for item in trs:
                self.counter += 1

                abit_info = item.find_all()
                a = []
                for index, abit in enumerate(abit_info):
                    if index == 0 and ' ' in abit.text:
                        if abit.text == '?????? ?????????????????????????? ??????????????????':
                            admission = competition.BVI
                        elif abit.text == '???? ?????????????????? ?????????? ?? ???????????????? ???????????? ??????????':
                            admission = competition.OK
                        elif abit.text == '???? ?????????????????? ?????????? ?? ???????????????? ?????????????? ??????????':
                            admission = competition.CK
                        elif abit.text == '???? ???????????? ????????????????':
                            admission = competition.general
                        elif abit.text == '???? ?????????????????????? ????????????':
                            admission = competition.contract
                    else:
                        a.append(abit.text)

                if a[-4] == '????':
                    sogl = True
                else:
                    sogl = False

                if not a[4]:
                    a[4] = 0

                if not a[5]:
                    a[5] = 0

                if not a[6]:
                    a[6] = 0

                applicant = {
                    'university': '????????',
                    'curse': CURSE,
                    'curse_name': CURSE_NAME,
                    'admission': admission,
                    'divorce_numb': a[-13],
                    'FIO': a[-12],
                    'EGE_ID': a[-7],
                    'SOGL': sogl,
                    'state': a[-1],
                    'get_sogl': False,
                    'consent_equals': False,
                    'EGE': [int(a[4]), int(a[5]), int(a[6])]
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 249 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])

            return True

        def get_itmo_applicants():

            for curse in self.curses_itmo:
                PARSER(str(curse))

        get_itmo_applicants()

if __name__ == '__main__':
    res = parser()
    req = res.current()
