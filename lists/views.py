from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item

# Create your views here.

def home_page(request):
    return render(request, 'home.html') # template을 이용하여 요청에대한 처리 수행

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items' : items}) # template을 이용하여 요청에대한 처리 수행

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')