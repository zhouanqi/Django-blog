import markdown
from django.shortcuts import render,get_object_or_404
from comments.forms import CommentForm
from .models import Post,Category,Tag
from django.views.generic import ListView,DetailView
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from django.db.models import Q

#文章列表页
# def index(request):
#     post_list=Post.objects.all()
#     return render(request,'blog/index.html',context={'post_list':post_list})
class Indexview(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by =2


    def get_context_data(self, **kwargs):
        """
        在视图函数中将模板变量传递给模板是通过给 render 函数的 context 参数传递一个字典实现的，
        例如 render(request, 'blog/index.html', context={'post_list': post_list})，
        这里传递了一个 {'post_list': post_list} 字典给模板。
        在类视图中，这个需要传递的模板变量字典是通过 get_context_data 获得的，
        所以我们复写该方法，以便我们能够自己再插入一些我们自定义的模板变量进去。
        """

        # 首先获得父类生成的传递给模板的字典。
        context = super().get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        # paginator 是 Paginator 的一个实例，
        # page_obj 是 Page 的一个实例，
        # is_paginated 是一个布尔变量，用于指示是否已分页。
        # 例如如果规定每页 10 个数据，而本身只有 5 个数据，其实就用不着分页，此时 is_paginated=False。
        # 关于什么是 Paginator，Page 类在 Django Pagination 简单分页：http://zmrenwu.com/post/34/ 中已有详细说明。
        # 由于 context 是一个字典，所以调用 get 方法从中取出某个键对应的值。
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见下方。
        pagination_data = self.pagination_data(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        print(type(pagination_data))
        context.update(pagination_data)

        # 将更新后的 context 返回，以便 ListView 使用这个字典中的模板变量去渲染模板。
        # 注意此时 context 字典中已有了显示分页导航条所需的数据。
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range
        right = page_range[page_number:page_number + 2]
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        if right:
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        if left:
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        data = {
                'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last,
            }

        return data
#详情页
def detail(request ,pk):
    post=get_object_or_404(Post,pk=pk)
    #文章阅读量+1
    post.pagesclicks()
    #引入markdown模块
    # post.body=markdown.Markdown(post.body,
    #                             extensions=[
    #                             'fenced_code',
    #                             'codehilite(css_class=highlight)',
    #                             'markdown.extensions.tables',
    #                             'toc',
    #                             'sane_lists',
    #                             ])
    post.body=mistune.markdown(post.body)
    form=CommentForm()
    comment_list=post.comments_set.all()
    comment_num=post.comments_set.count()
    context={
        'post':post,
        'form':form,
        'comment_list':comment_list,
        'comment_num':comment_num,
    }
    return render(request,'blog/detail.html',context=context)
#时间归档
# def getPostdate(request,year,month):
#     post_list=Post.objects.filter(create_time__year=year,
#                                   create_time__month=month)
#     return render(request,'blog/index.html',context={'post_list':post_list})
class Postdetailview(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        #阅读量+1
        #获得self.object 其值未Post的实例
        response=super().get(request,*args,**kwargs)
        self.object.pagesclicks()
        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md= markdown.Markdown(
                                      extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          'markdown.extensions.toc',
                                          'markdown.extensions.tables',
                                          TocExtension(slugify=slugify),
                                      ])
        post.body=md.convert(post.body)
        post.toc=md.toc
        return post
    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        form = CommentForm()
        comment_list = self.object.comments_set.all()
        comment_num = self.object.comments_set.count()
        context.update( {
            'post': self.object,
            'form': form,
            'comment_list': comment_list,
            'comment_num': comment_num,
        })
        return context

class Postdateview(Indexview):
    def get_queryset(self):
        """
        获取全部数据的函数
        官方解释：返回用来获取本视图显示对象的queryset。默认的，如果设置了queryset属性，
        get_queryset()返回它的值，否则该方法构造一个QuerySet通过调用model属性的默认管理器的all()方法。（我看不懂...）
        :return:
        """
        year=self.kwargs.get('year')
        month=self.kwargs.get('month')
        return super(Postdateview,self).get_queryset().filter(create_time__year=year,create_time__month=month)
        # post_list = Post.objects.filter(create_time__year=year,create_time__month=month)
#分类
# def getCategory(request,pk):
#     category=get_object_or_404(Category,pk=pk)
#     post_list=Post.objects.filter(category=category).order_by('-create_time')
#     return render(request,'blog/index.html',context={'post_list':post_list})
class Categoryviews(Indexview):
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        category = get_object_or_404(Category, pk=pk)
        return super().get_queryset().filter(category=category).order_by('-create_time')
# #标签云
# Create your views here.
class Tagviews(Indexview):
    def get_queryset(self):
        pk=self.kwargs.get('pk')
        tag = get_object_or_404(Tag, pk=pk)
        return super().get_queryset().filter(tags=tag)

# class Seachviews(Indexview):
#     def get_queryset(self):
#         q=self.kwargs.get('q')
#         if not q:
#             return super().get_queryset()
#         return super().get_queryset().filter(Q(title__icontains=q) | Q(body__icontains=q))
def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg':error_msg ,'post_list': post_list})
# }