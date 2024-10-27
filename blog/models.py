from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    banner = models.FileField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def url(self):
        return '/blog/' + str(self.id) + '/' + self.title.replace(" ", "-")
