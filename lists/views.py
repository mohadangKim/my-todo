from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home_page(request):
  return render(request, 'home.html') # template을 이용하여 요청에대한 처리 수행