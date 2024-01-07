from django.db import models
from spacetravel.models import TimeModel


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.TextField(unique=True)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_category'
        app_label = 'spacetravel'


class Sentiment(models.Model):
    sentiment_id = models.AutoField(primary_key=True)
    score = models.DecimalField(max_digits=10, decimal_places=2, unique=True)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_sentiment'
        app_label = 'spacetravel'


class Source(models.Model):
    source_id = models.AutoField(primary_key=True)
    source_name = models.TextField(unique=True)

    objects = models.Manager()

    class Meta:
        db_table = 'dim_source'
        app_label = 'spacetravel'


class NewsDetail(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.TextField()
    summary = models.TextField()
    url = models.TextField()
    img_url = models.TextField()

    objects = models.Manager()

    class Meta:
        db_table = 'dim_news_detail'
        app_label = 'spacetravel'


class NewsSheet(models.Model):
    fact_sheet_id = models.AutoField(primary_key=True)
    news_id = models.ForeignKey(NewsDetail, on_delete=models.CASCADE, db_column='news_id')
    time_id = models.ForeignKey(TimeModel, on_delete=models.CASCADE, db_column='time_id')
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE, db_column='source_id')
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    sentiment_id = models.ForeignKey(Sentiment, on_delete=models.CASCADE, db_column='sentiment_id')

    objects = models.Manager()

    class Meta:
        db_table = 'fact_news'
        app_label = 'spacetravel'
