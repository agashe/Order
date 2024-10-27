from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Post, Tag

def index(request):
    title = 'Blog'
    tags = Tag.objects.all()
    
    breadcrumbs = [
        {'link': "/blog", 'title': 'Blog'},
    ]
    
    if request.GET.get("keyword") is not None:
        posts = Post.objects.filter(title__contains=request.GET.get("keyword"))
        title += ' - Search Results : ' + request.GET.get("keyword")
    if request.GET.get("tag") is not None:
        posts = Post.objects.filter(tags__name=request.GET.get("tag"))
        title = ' Posts about ' + request.GET.get("tag")
    else:
        posts = Post.objects.all()
        breadcrumbs = []

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog/index.html", {
        'title': title,
        'page_obj': page_obj,
        'tags': tags,
        'keyword': request.GET.get("keyword"),
        'breadcrumb_items': breadcrumbs
    })

def show(request, id, title):
    post = Post.objects.get(id=id)
    similar_posts = Post.objects.exclude(id=id).order_by('?')
    tags = Tag.objects.all()

    return render(request, "blog/show.html", {
        'title': post.title,
        'post': post,
        'tags': tags,
        'similar_posts': similar_posts[:3],
        'breadcrumb_items': [
            {'link': "/blog", 'title': 'Blog'},
        ]
    })
