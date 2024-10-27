from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.CharField(max_length=200)
    created_at = models.DateTimeField("date published")

class ContactUsMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    body = models.TextField()

class Page(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class Setting(models.Model):
    key = models.CharField(max_length=200)
    val = models.CharField(max_length=200)
