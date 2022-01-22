from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from lists.views import home_page

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') # 장고 내부 함수로 URL을 해석해서 일치하는 뷰 함수를 찾음
        self.assertEqual(found.func, home_page) # home_page 라는 함수 존재 하는지 검증
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request) # home_page 뷰에 전달해서 응답을 취득, 반환값은 HttpResponse 객체
        self.assertTrue(response.content.startswith(b'<html>')) # 응답 내용 검증
        self.assertIn(b'<title>To-Do lists</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))