from django.contrib import admin
#导入数据库
from .models import Post,Category,Tag
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'create_time', 'finish_time', 'category', 'author']

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)
# admin.site.register(static)
#Register your models here.
