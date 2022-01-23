
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retriev_it_later(self):
        # 사이트 접속
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        inputbox.send_keys('공작깃털 사기') # inputboxdp에에 '공작깃털 사기' 문자열 입력
        inputbox.send_keys(Keys.ENTER) # inputboxdp에 ENTER 키 입력 이벤트 전달
        time.sleep(1)

        self.check_for_row_in_list_table('1: 공작깃털 사기')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # 첫번째 사용자가 사이트 접속
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 공작깃털 사기')

        # 추가 REST API url 변경 되었는지 검증
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/list/.+')

        # 두번째 사용자가 사이트 접속
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 첫번째 사용자의 To-Do 리스트가 없는지 확인
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 우유 사기')

        # 두번째 사용자 추가 REST API URL이 첫번째 사용자의 추가 REST API URL과 다른지 거믖ㅇ
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 다시, 첫번째 사용자의 To-Do 리스트가 없는지 확인
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)