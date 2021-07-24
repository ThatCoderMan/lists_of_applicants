from bs4 import BeautifulSoup
import requests
from global_parametrs import competition, applicant_information


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
                print('ИТМО -', CURSE)

            PLACES = soup.find('section', {'class': 'static-page-rule'}).text.split()
            curse_ind = PLACES.index(CURSE)
            free_ind = PLACES.index('бюджетных')
            cont_ind = PLACES.index('контрактных')
            free_pl = ' '.join(PLACES[curse_ind + 1:free_ind]).split('»')
            trs = table.find_all('tr')[2:]
            admission = ''
            for item in trs:
                self.counter += 1

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

                if a[-4] == 'Да':
                    sogl = True
                else:
                    sogl = False

                applicant = {
                    'university': 'ИТМО',
                    'curse': CURSE,
                    'curse_name': CURSE_NAME,
                    'admission': admission,
                    'divorce_numb': a[-13],
                    'FIO': a[-12],
                    'EGE_ID': a[-7],
                    'SOGL': sogl,
                    'state': a[-1],
                    'get_sogl': False,
                    'consent_equals': False
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 250 or
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

            if information['type'] == 'Госбюджетная':
                information.update({'places': curse_information[8]})
                information.update({'ok_places': curse_information[9]})
            else:
                information.update({'places': curse_information[8]})

            if information['level'] == 'бакалавриат' and \
                    information['curse'].split('.')[0] in self.curses_with_informatics \
                    and information['here'] == 'очная' \
                    and 'ИКТ' in information['other']:
                print('СПбГУ - ', information['curse'])
            else:
                return False

            table = soup.find('table').find_all('tr')[1:]

            for element in table:
                self.counter += 1
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

                    if applicants[10].text == 'Да':
                        sogl = True
                    else:
                        sogl = False

                    applicant = {
                        'university': 'СПбГУ',
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
                elif information['type'] == 'Договорная':

                    if applicants[9].text == 'Да':
                        sogl = True
                    else:
                        sogl = False

                    applicant = {
                        'university': 'СПбГУ',
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
                        'university': 'СПбГУ',
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
                        (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 250 or
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
            report_option = '25f848f5-daa1-11eb-8040-0050569f980a'
            scenario = 'e816affc-5f19-11eb-803a-0050569f980a'
            scenarioN = 'Списки%20поступающих%20по%20программам%20бакалавриата/' \
                        'специалитета%20в%202021%20году%20для%20граждан%20РФ'
            form_education = 'a5ae897b-5972-11eb-803a-0050569f980a'

            basis_admissions = {"Бюджетная основа": "a5ae8977-5972-11eb-803a-0050569f980a",
                               "Контракт": "a5ae8978-5972-11eb-803a-0050569f980a",
                               "Льготная основа": "a5ae897e-5972-11eb-803a-0050569f980a",
                               "Целевой прием": "a5ae8979-5972-11eb-803a-0050569f980a"}

            faculty = '21916fb8-5ef2-11eb-803a-0050569f980a'
            directions = {'02.03.01 Математика и компьютерные науки':
                              'fe0a43fc-5f1a-11eb-803a-0050569f980a',
                          "02.03.02 Фундаментальная информатика и информационные технологии":
                              'fe0a43fd-5f1a-11eb-803a-0050569f980a',
                          "02.03.03 Математическое обеспечение и администрирование информационных систем":
                              '041285e7-5f1b-11eb-803a-0050569f980a',
                          "09.03.01 Информатика и вычислительная техника":
                              "0ddbe522-5f1b-11eb-803a-0050569f980a",
                          "09.03.02 Информационные системы и технологии":
                              "0ddbe523-5f1b-11eb-803a-0050569f980a",
                          "09.03.03 Прикладная информатика":
                              "13ff1805-5f1b-11eb-803a-0050569f980a",
                          "09.03.04 Программная инженерия":
                              "13ff1806-5f1b-11eb-803a-0050569f980a",
                          "27.03.01 Стандартизация и метрология":
                              "104b85b4-9c5e-11eb-803c-0050569f980a",
                          "27.03.02 Управление качеством":
                              "4f707e3c-5f1b-11eb-803a-0050569f980a",
                          "27.03.03 Системный анализ и управление":
                              "57918c96-5f1b-11eb-803a-0050569f980a",
                          "27.03.04 Управление в технических системах":
                              "57918c97-5f1b-11eb-803a-0050569f980a",
                          "27.03.05 Инноватика":
                              '57918c98-5f1b-11eb-803a-0050569f980a'}

            for curse_name, direction in directions.items():
                curse_id = curse_name.split()[0]
                curse = ' '.join(curse_name.split()[1:])
                for basis_admission_name ,basis_admission in basis_admissions.items():
                    links.update({'&'.join([curse_id,curse,basis_admission_name]):
                            f'https://enroll.spbstu.ru/ajax/interactive_detail?report_option={report_option}'
                                    f'&scenario={scenario}&scenarioN={scenarioN}&level_education={level_education}'
                                    f'&form_education={form_education}&basis_admission={basis_admission}'
                                    f'|false&faculty={faculty}&direction={direction}&'
                                    f'profile=00000000-0000-0000-0000-000000000000&actions=list_applicants'})

            faculty = "5c353740-5ef2-11eb-803a-0050569f980a"
            directions = {"01.03.02 Прикладная математика и информатика":
                              "fe0a43f9-5f1a-11eb-803a-0050569f980a",
                          "01.03.03 Механика и математическое моделирование":
                              "fe0a43fa-5f1a-11eb-803a-0050569f980a",
                          "15.03.03 Прикладная механика":
                              "2ae852e1-5f1b-11eb-803a-0050569f980a"}

            for curse_name, direction in directions.items():
                curse_id = curse_name.split()[0]
                curse = ' '.join(curse_name.split()[1:])
                for basis_admission_name, basis_admission in basis_admissions.items():
                    links.update({'&'.join([curse_id,curse,basis_admission_name]):
                            f'https://enroll.spbstu.ru/ajax/interactive_detail?report_option={report_option}'
                            f'&scenario={scenario}&scenarioN={scenarioN}&level_education={level_education}'
                            f'&form_education={form_education}&basis_admission={basis_admission}'
                            f'|false&faculty={faculty}&direction={direction}&'
                            f'profile=00000000-0000-0000-0000-000000000000&actions=list_applicants'})

            return links

        def PARSER(curse_link, url):

            print('СПбПУ -',curse_link[0])
            req = requests.get(url, headers=self.headers).json()

            applicants = req['data']['list_applicants']

            for applicant in applicants:
                self.counter += 1

                if applicant['КатегорияПриема'] == 'Без вступительных испытаний':
                    admission = competition.BVI
                elif applicant['КатегорияПриема'] == 'На общих основаниях':
                    if curse_link[2] == 'Контракт':
                        admission = competition.contract
                    elif curse_link[2] == 'Целевой прием':
                        admission = competition.CK
                    elif curse_link[2] == 'Бюджетная основа':
                        admission = competition.general
                    else:
                        admission = 'None'
                elif applicant['КатегорияПриема'] == 'Имеющие особое право':
                    admission = competition.OK
                else:
                    admission = 'None'

                if applicant['СогласиеНаЗачисление'] == 'Да':
                    sogl = True
                else:
                    sogl = False

                if applicant['УникальныйКод']:
                    applicant = {
                        'university': 'СПбПУ',
                        'curse': curse_link[0],
                        'curse_name': curse_link[1],
                        'admission': admission,
                        'divorce_numb': 1,
                        'FIO': applicant['УникальныйКод'].split()[0],
                        'EGE_ID': applicant['СуммаБаллов'],
                        'SOGL': sogl,
                        'state': applicant['Состояние'],
                        'get_sogl': False,
                        'consent_equals': False
                    }

                    if (applicant['admission'] != competition.contract and
                            (applicant['EGE_ID'] and int(applicant['EGE_ID']) > 250 or
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
            types = ['byudzhet']#, 'kontrakt']
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

            return [main_link+type_+'/'+link for type_ in types for link in links]

        def PARSER(url):

            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'html.parser')

            information = soup.find('span', {'class': 'B_currentCrumb'})

            curse_id = information.text.split()[0]
            curse = ' '.join(information.text.split()[1:])

            table = soup.find('table').find_all('tr')[2:]

            print('ЛЭТИ -', curse_id)

            for element in table:
                self.counter += 1
                applicant_information = element.find_all('td')
                applicant = []
                for applicant_info in applicant_information:
                    applicant.append(applicant_info.text)

                if applicant[3] == 'БВИ':
                    admission = competition.BVI
                elif applicant[3] == 'ВК':
                    admission = competition.OK
                elif applicant[3] == 'ОК':
                    admission = competition.general
                elif applicant[3] == 'К':
                    admission = competition.contract
                elif applicant[3] == 'ЦК':
                    admission = competition.CK
                else:
                    admission = 'None'

                if applicant[-1] == 'Да':
                    sogl = True
                else:
                    sogl = False

                applicant = {
                    'university': 'ЛЭТИ',
                    'curse': curse_id,
                    'curse_name': curse,
                    'admission': admission,
                    'divorce_numb': applicant[2],
                    'FIO': applicant[1].split()[0],
                    'EGE_ID': applicant[4],
                    'SOGL': sogl,
                    'state': 'преимущественное право - '+applicant[9],
                    'get_sogl': False,
                    'consent_equals': False
                }

                if (applicant['admission'] != competition.contract and
                        (applicant['EGE_ID'] != '-' and int(applicant['EGE_ID']) > 250 or
                         applicant['admission'] != competition.general)):
                    self.list_of_applicants.append(applicant)
                    if applicant['SOGL']:
                        self.have_sogl.append(applicant['FIO'])
            return True

        def get_spbgy_applicants():

            for url in get_curses():
                PARSER(url)

        return get_spbgy_applicants()


if __name__ == '__main__':
    res = parser()
    req = res.spbguty()

