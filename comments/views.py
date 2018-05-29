from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comments
from .forms import CommentForm
# Create your views here.
"""
获取被评论的文章，把评论和文章关联起来
确认用户请求为：POST
构造CommentsForm的实例，生成表单
检查表单的数据是否符合要求
合法时：调用表单的save方法暂存，先不保存在数据库
将评论和被评论的的文章关联
将评论数据保存到数据库
重定向到post详情页
不合法时：
重新渲染详情页，渲染表单的错误
反向查询全部评论
重新显示文章详情页和评论
"""

def comments(request,pk):
    #获取被评论的文章，把评论和文章关联起来
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect(post)

        else:
            comment_list=post.comments_set.all()
            context={
                'post':post,
                'form':form,
                'comment_list':comment_list
            }
            return render(request,'blog/detail.html',context=context)
    return redirect(post)