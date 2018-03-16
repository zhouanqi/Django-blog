# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myblog.settings")

#判断Django版本，大于1.7需要使用setup
import django
if django.VERSION>1.7:

    django.setup()

def bath():
    from blog.models import Category
    f=open('blogimf.txt')
    for line in f:
        category=line.split('****')
        Category.objects.create(category=category)
    f.close()

if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myblog.settings")
    bath()
    print('Done!')