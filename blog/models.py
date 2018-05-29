from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible

# 数据库
@python_2_unicode_compatible
class Category(models.Model):
    """
    #文章分类表
    """
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    """
    文章标签表
    """
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    """
    #文章表
    """
    #文章标题
    title=models.CharField(max_length=100)
    #文章分类
    #文章->分类一对多,不可以为空
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    #文章标签
    #文章<->标签多对多，可以不填写
    tags=models.ManyToManyField(Tag,blank=True)
    # 文章摘要
    summary=models.TextField(max_length=200,blank=True)
    #文章内容
    body=models.TextField()
    #文章创建时间
    create_time=models.DateTimeField()
    #文章最后修改时间
    finish_time=models.DateTimeField()
    #文章作者
    author=models.CharField(User,max_length=100)
    #文章点击量
    clicks=models.PositiveIntegerField(blank=True)
    def __str__(self):
        """
        #返回一个字符串
        :return:
        """
        return self.title
    def pagesclicks(self):
        """
        将文章的点击量+1，更新views字段
        :return:
        """
        self.clicks+=1
        self.save(update_fields=['clicks'])
#為了能夠在文章中随处可以进入到另一个url中，需要有一个可以重定像的url
#在这里使用url的反向解析，反过来找到url
    def get_absolute_url(self):
        """
        #reverse(viewname[, urlconf=None, args=None, kwargs=None, current_app=None])[source]¶
        #viewname可以是包含视图对象，URL pattern name或可调用视图对象的Python路径的字符串。
        :return:
        """
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta(object):
        ordering=['-create_time','title']