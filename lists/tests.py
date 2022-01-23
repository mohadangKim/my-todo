from django.core.urlresolvers import resolve
from django.http import HttpRequest, request, response
from django.test import TestCase
from django.template.loader import render_to_string
from lists.views import home_page, new_list, add_item
from lists.models import Item, List

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

class ListAndItemModelTest(TestCase):
    
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item() # django orm
        first_item.text = '첫 번째 아이템' # 속성 생성(column)
        first_item.list =list_
        first_item.save()

        second_item = Item()
        second_item.text = '두 번째 아이템'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all() # object : DB 조회, all() : 테이블에 있는 모든 레코드를 추출
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '첫 번째 아이템')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, '두 번째 아이템')
        self.assertEqual(second_saved_item.list, list_)

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/{}/'.format(list_.id,)) # url에 list id를 넣어야 요청 가능
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item1', list=other_list)
        Item.objects.create(text='other list item2', list=other_list)

        response = self.client.get('/lists/{}/'.format(correct_list.id))

        self.assertContains(response, 'itemey 1') # 각자 고유의 item을 가지는지 검증
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item1')
        self.assertNotContains(response, 'other list item2')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get('/lists/{}/'.format(correct_list.id))
        self.assertEqual(response.context['list'], correct_list) # response.context : 렌더링 함수에 전달할 context

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

        first_list = List.objects.first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/{}/'.format(first_list.id,))


class NewItemTest(TestCase):
    
    def test_can_save_a_POST_request_to_an_existing_list(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new item for an existing list'
        response = add_item(request, correct_list.id)        

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_redirects_to_list_view(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new item for an existing list'
        response = add_item(request, correct_list.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/{}/'.format(correct_list.id,))