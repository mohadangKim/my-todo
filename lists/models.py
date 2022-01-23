from django.db import models

# Create your models here.

# models.Model로부터 상속받은 클래스는 테이블 역할을 한다
class Item(models.Model): # table 정의
    text = models.TextField(default='') # text 컬럼 정의