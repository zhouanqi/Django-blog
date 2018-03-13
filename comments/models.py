from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Comments(models.Model):
    # email=models.EmailField(max_length=255)
    create_time=models.DateField(auto_now=True)
    name=models.CharField(max_length=100)
    content=models.TextField()
    post=models.ForeignKey('blog.Post',on_delete=models.CASCADE,null=True)
    def __str__(self):
        """
        #返回一个字符串
        :return:
        """
        return self.content[:20]


# Create your models here.
