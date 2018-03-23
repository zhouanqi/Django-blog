# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myblog.settings")

#判断Django版本，大于1.7需要使用setup
import django
if django.VERSION>1.7:
    django.setup()

def bath():
    import codecs
    from blog.models import Post ,Category ,Tag #可以先批量导入分类和标签之后再导入文章
    f=codecs.open('blogimf.txt','r','utf-8')  #以防内容中有中文

    for line in f.readlines():
        # tag1=line.encode('utf-8')
        # Tag.objects.create(name=tag1)
        # category = line.encode('utf-8')
        # Category.objects.create(name=category)
        post = line.encode('utf-8')
        # Post.objects.get_or_create(title=title)
        # Post.objects.create(creat_time=creat_time)
        # Post.objects.create(belongfor=belongfor)
        # Post.objects.create(tag=tag)
        # Post.objects.create(readnum=readnum)
        # Post.objects.create(author=author)
        # Post.objects.create(post=post)
        # Post.objects.create(comment=comment)
    f.close() 

if __name__=='__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Myblog.settings")
    bath()
    print('Done!')