from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.

# models.Model로부터 상속받은 클래스는 테이블 역할을 한다
class List(models.Model):
    pass

class Item(models.Model): # table 정의
    text = models.TextField(default='') # text 컬럼 정의
    list = models.ForeignKey(List, default=None)
