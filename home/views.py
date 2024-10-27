from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import datetime
from .models import Page, NewsletterSubscriber, ContactUsMessage
from .forms import SubscribeForm, ContactUsForm
from inventory.models import Product

def index(request):
    return render(request, "home/index.html", {
        'products': Product.objects.order_by('-created_at')[:12]
    })

def about(request):
    about_page = Page.objects.get(title='About')
    return render(request, "home/page.html", {
        'title': about_page.title,
        'content': about_page.content,
    })

def delivery_information(request):
    delivery_information_page = Page.objects.get(title='Delivery Info')
    return render(request, "home/page.html", {
        'title': delivery_information_page.title,
        'content': delivery_information_page.content,
    })

def privacy_policy(request):
    privacy_policy_page = Page.objects.get(title='Privacy Policy')
    return render(request, "home/page.html", {
        'title': privacy_policy_page.title,
        'content': privacy_policy_page.content,
    })

def terms_of_usage(request):
    terms_of_usage_page = Page.objects.get(title='Terms of Usage')
    return render(request, "home/page.html", {
        'title': terms_of_usage_page.title,
        'content': terms_of_usage_page.content,
    })

def contact(request):
    if request.method == "POST":
        form = ContactUsForm(request.POST)

        if form.is_valid():
            ContactUsMessage.objects.create(
                name = form.cleaned_data['name'],
                email = form.cleaned_data['email'],
                body = form.cleaned_data['body'],
            )

            messages.success(request, "Your message was received successfully !")
        else:
            for error in form.errors.keys():
                if error == "name":
                    messages.error(request, "Invalid name !")
                    break
                elif error == "email":
                    messages.error(request, "Invalid email address !")
                    break
                elif error == "body":
                    messages.error(request, "Invalid message !")
                    break

        return redirect(request.META.get('HTTP_REFERER'))    

    return render(request, "home/contact.html", {
        'title': 'Contact Us',
        'open_time': '10:00 AM to 23:00 PM',
    })

def subscribe(request):
    if request.method == "POST":
        form = SubscribeForm(request.POST)

        if form.is_valid():
            NewsletterSubscriber.objects.create(
                email = form.cleaned_data['email'],
                created_at = datetime.datetime.now()
            )

            messages.success(request, "You have subscribed successfully !")
        else:
            for error in form.errors.keys():
                if error == "email":
                    messages.error(request, "Invalid email address !")
                    break

    return redirect(request.META.get('HTTP_REFERER'))
