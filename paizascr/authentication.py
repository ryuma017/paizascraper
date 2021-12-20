import requests

from bs4 import BeautifulSoup
from .exceptions import LoginFailureError, LogoutFailureError, AuthenticationError


class PaizaAuthentication:

    PAIZA_URL = 'https://paiza.jp'
    TARGET_URL = PAIZA_URL + '/challenges/ranks/'
    ranks = ('s', 'a', 'b', 'c', 'd')

    def __init__(self, email, password, url=PAIZA_URL):
        self.__login_data = {
            'email': email,
            'password': password
        }

        self.__logout_data = {
            '_method': 'delete'
        }

        self.is_logged_in = False
        self.all_submmited_problems = []
        self.cleared_problems = []
        self.uncleared_problems = []

        self.session = requests.session()

        # Get a authenticity token.
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        authenticity_token = soup.find(attrs={'name': 'csrf-token'}).get('content')
        self.__login_data['authenticity_token'] = authenticity_token
        self.__logout_data['authenticity_token'] = authenticity_token

    def login(self):
        login_url = 'https://paiza.jp/user_sessions'
        login_response = self.session.post(login_url, data=self.__login_data)

        is_status_code_200 = login_response.status_code == 200

        if is_status_code_200 and 'profile' in login_response.text:
            self.is_logged_in = True
            return True
        else:
            raise LoginFailureError('failed to login. review your credentials.')

    def logout(self):
        if not self.is_logged_in:
            raise AuthenticationError('run "self.login()" before running the "self.logout()".')

        logout_url = 'https://paiza.jp/logout'
        logout_response = self.session.post(logout_url, data=self.__logout_data)

        is_status_code_200 = logout_response.status_code == 200

        if is_status_code_200 and 'profile' not in logout_response.text:
            return True
        else:
            raise LogoutFailureError('failed to logout')

    def scrape_results(self, rank, shoud_display_log=False, paiza_url=PAIZA_URL, target_url=TARGET_URL):
        if not self.is_logged_in:
            raise AuthenticationError('you need to run "self.login()" before running this method.')

        if rank in self.ranks:
            target_url += rank.lower()
        else:
            raise ValueError('choose only one from (s, a, b, c, d)')

        response = self.session.get(target_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        submitted_probrem_boxes = soup.find_all(name='div', attrs={'class': 'problem-box problem-box--submitted'})
        data_len = len(submitted_probrem_boxes)
        count = 1
        self.all_submmited_problems = []
        self.cleared_problems = []
        self.uncleared_problems = []

        for box in submitted_probrem_boxes:
            problem_url = box.a.get('href')
            detail_response = self.session.get(paiza_url+problem_url)
            soup = BeautifulSoup(detail_response.text, 'html.parser')

            summary_box = soup.find(name='div', attrs={'class': 'summary-box__result'})
            result_box = summary_box.div.find_all('span')

            title = summary_box.find(name='p', attrs={'class': 'summary-box__problem-name'}).contents[0].strip()[3:]
            langage = result_box[3].get_text(strip=True)
            time = result_box[5].get_text(strip=True)
            byte_count = result_box[7].get_text(strip=True).replace(' ', '')
            score = result_box[9].get_text(strip=True)

            self.all_submmited_problems.append((
                title, langage, time, byte_count, score
            ))

            if shoud_display_log == True:
                print(f'{count}/{data_len}')
                count += 1

            if score[:-1] == '100':
                self.cleared_problems.append((
                    title, langage, time, byte_count, score
                ))
            else:
                self.uncleared_problems.append((
                    title, langage, time, byte_count, score
                ))
