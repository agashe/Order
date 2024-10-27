from django.contrib.auth.models import User
from home.models import Setting
from blog.models import Post
from inventory.models import Category, Product

def settings(request):
    settings = {}

    for option in Setting.objects.all():
        settings[option.key] = option.val

    recent_news = Post.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    latest_products = Product.objects.all().order_by('-created_at')

    return {
        'settings_email': settings['email'],
        'settings_phone': settings['phone'],
        'settings_address': settings['address'],
        'settings_facebook_link': settings['facebook_link'],
        'settings_twitter_link': settings['twitter_link'],
        'settings_pintrest_link': settings['pintrest_link'],
        'settings_instgram_link': settings['instgram_link'],
        'recent_news': recent_news[:3],
        'categories': categories,
        'latest_products': latest_products[:5],
    }
    