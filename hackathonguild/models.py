from datetime import datetime
from django.db import models
from django.db.models.base import Model
from django.utils import timezone

# Create your models here.


class Post(models.Model):
    poster_name = models.CharField('投稿者名', max_length=50)
    poster_mail = models.EmailField('投稿者メールアドレス', max_length=50)
    webhookURL = models.TextField('投稿者slackwebhookURL', max_length=100, null=True)
    product_name = models.CharField('プロダクト名', max_length=50)
    hackathon_date = models.DateField('ハッカソン開催日')
    recluting_headcount = models.IntegerField('募集人数')
    delete_key = models.CharField('削除キー', max_length=8)
    product_brief = models.TextField('プロダクト概要', max_length=500, blank=True)
    file = models.FileField('説明資料', blank=True)
    posted_date = models.DateTimeField('投稿日', default=timezone.now)
    post_delete_date = models.DateTimeField('投稿削除日', blank=True)

    def __str__(self):
        return self.poster_name


class Participant(models.Model):
    participant_name = models.CharField('参加者名', max_length=50)
    participant_mail = models.EmailField('参加者メールアドレス', max_length=50)
    enthusiasm = models.TextField('意気込み', max_length=200, blank=True)
    participate_product_id = models.IntegerField('参加プロダクトid')
    participate_date = models.DateField('参加日', default=timezone.now)
    token = models.CharField('トークン', default='', max_length=200)
    token_delete_date = models.DateTimeField('トークン削除日',  default=timezone.now)

    def __str__(self):
        return self.participant_name
