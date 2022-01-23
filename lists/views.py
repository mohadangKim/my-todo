from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item
from lists.models import List

# Create your views here.

def home_page(request):
    return render(request, 'home.html') # template을 이용하여 요청에대한 처리 수행

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list' : list_}) # template을 이용하여 요청에대한 처리 수행

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{}/'.format(list_.id,))

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/{}/'.format(list_.id,))