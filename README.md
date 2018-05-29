该博客是学习来自：[追梦人物Django博客教程](https://note.youdao.com/)，
[GitHub地址](https://github.com/zmrenwu/django-blog-tutorial)

数据库使用：Django内置数据库数据库：SQLite3。  

博客包含：首页、文章详情页两个基本页面。

- 首页：根据发布时间分页展示文章列表、使用侧边栏显示：最新文章、文章分类、时间归档、标签云，支持RSS订阅。
- 文章详情页：支持Markdown语法和代码高亮、自动生成文章目录，记录阅读量、评论。

博客支持全文检索，关键词高亮。（django-haystack、Whoosh、jieba）
