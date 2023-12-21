from django.db import models


# Create your models here.
class News(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    news_site = models.CharField(max_length=255)
    summary = models.TextField()
    published_at = models.DateTimeField()
    category = models.CharField(max_length=255)
