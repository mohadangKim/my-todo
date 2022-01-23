from django.core.urlresolvers import resolve
from django.http import HttpRequest, request, response
from django.test import TestCase
from django.template.loader import render_to_string
from lists.views import home_page
from lists.views import new_list
from lists.models import Item

# Create your tests here.
class HomePageTest(TestCase):
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') # 장고 내부 함수로 URL을 해석해서 일치하는 뷰 함수를 찾음
        self.assertEqual(found.func, home_page) # home_page 라는 함수 존재 하는지 검증
    
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request) # home_page 뷰에 전달해서 응답을 취득, 반환값은 HttpResponse 객체
        html = response.content.decode('utf8') # home_page 함수가 template을 이용하여 구현 되었는지 검증
        expected_html = render_to_string('home.html')
        self.assertEqual(html, expected_html)

class ItemModelTest(TestCase):
  
    def test_saving_and_retrieving_items(self):
        first_item = Item() # django orm
        first_item.text = '첫 번째 아이템' # 속성 생성(column)
        first_item.save() # DB에 저장

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.save()

        saved_items = Item.objects.all() # object : DB 조회, all() : 테이블에 있는 모든 레코드를 추출
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(second_saved_item.text, '두 번째 아이템')

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html') # reponse가 list.html 템플릿을 이용하여 만들어 졌는지 검증

    def test_displays_all_list_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())

class NewListTest(TestCase):
    def test_saving_a_POST_request(self):
        # self.client.post(
        #     '/lists/new', data={'item_text': '신규 작업 아이템'})
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'
        new_list(request)

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, '신규 작업 아이템')

    def test_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = '신규 작업 아이템'
        response = new_list(request)        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')