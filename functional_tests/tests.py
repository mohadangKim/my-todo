
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

    def check_for_row_in_list_table(self, row_text): # row_text 항목이 To-Do 리스트에 존재 하는지 검증하는 테스트
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retriev_it_later(self): # 페이지 UI 구성 & To-Do 리스트에 항목 추가 검증
        self.browser.get(self.live_server_url) # 사이트 접속

        self.assertIn('To-Do', self.browser.title) # 타이틀이 'To-Do' 표시하는지 검증

        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text) # 헤더가 'To-Do' 표시하는지 검증

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        ) # 입력창 placeholder 속성이 '작업 아이템 입력'인지 검증

        inputbox.send_keys('공작깃털 사기') # inputboxdp에에 '공작깃털 사기' 문자열 입력
        inputbox.send_keys(Keys.ENTER) # inputboxdp에 ENTER 키 입력 이벤트 전달, '공작깃털 사기'를 To-Do 리스트에 추가
        time.sleep(1)

        self.check_for_row_in_list_table('1: 공작깃털 사기') # '1: 공작깃털 사기' 항목이 To-Do 리스트에 있는지 검증

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        

    def test_multiple_users_can_start_lists_at_different_urls(self): # 다중 사용자 입력 검증
        # 첫번째 사용자가 사이트 접속하여 항목 추가
        self.browser.get(self.live_server_url) 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 브라우저 URL이 '추가 REST API' URL로 변경 되었는지 검증
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 두번째 사용자가 사이트 접속
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # 첫번째 사용자의 To-Do 리스트가 없는지 검증
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)
        
        # 두번째 사용자가 항목 추가
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 두번째 사용자 추가 REST API URL이 첫번째 사용자의 추가 REST API URL과 다른지 검증
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 다시, 첫번째 사용자의 To-Do 리스트가 없는지 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

    def test_layout_and_styling(self): # 레이아웃, css 검사
        # 페이지 방문
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768) # 창 크기 고정

        # 입력 상자가 가운데 배치된 것을 확인
        inputbox = self.browser.find_element_by_id("id_new_item")
        self.assertAlmostEqual( # 반올림 처리, 계산 결과가 +/- 10픽셀 내에 있도록 처리
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )