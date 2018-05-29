#获取数据库中前 num 篇文章，这里 num 默认为 5
from ..models import Post,Category,Tag
from django import template
from django.db.models.aggregates import Count
#创建一个全局register变量，它是用来注册你自定义标签和过滤器的，
register=template.Library()
#使用simple_tag的方法，将函数变为标签功能
#打开最新文章的标签
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]
#归档模板标签
@register.simple_tag
def get_Postdates():
    return Post.objects.dates('create_time','month',order='DESC')

#分类标签
@register.simple_tag
def get_Category():
    return Category.objects.annotate(num_posts=Count('post'))

#标签云标签
@register.simple_tag
def get_Tag():
    return Tag.objects.annotate(num_posts=Count('post'))

