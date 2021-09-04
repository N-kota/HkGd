from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Participant
from .tasks import send_email,send_slack_message
from django.utils import timezone
from rest_framework import exceptions
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import datetime
import hashlib
import secrets


# Create your views here.
def index(request):
    latest_posts = Post.objects.order_by('-posted_date')

    context = {
        'latest_posts': latest_posts,
    }
    return render(request, 'hackathonguild/index.html', context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post
    }
    return render(request, 'hackathonguild/post_detail.html', context)


def make_post(request):
    return render(request, 'hackathonguild/make_post.html')


def submit_post(request):
    poster_name = request.POST.get('poster_name')
    poster_mail = request.POST.get('poster_mail')
    product_name = request.POST.get('product_name')
    hackathon_date = request.POST.get('hackathon_date')
    recluting_headcount = request.POST.get('recluting_headcount')
    product_brief = request.POST.get('product_brief')
    file = request.POST.get('file')
    
    delete_key = make_random_string(8)
    posted_date = timezone.now()
    #basetime = datetime.time(0,00,00)
    #post_delete_date = datetime.datetime.combine(timezone.now(), basetime) + datetime.timedelta(hours=1)
    post_delete_date = timezone.now() + datetime.timedelta(hours=1)

    post = Post.objects.create(poster_name=poster_name, poster_mail=poster_mail, product_name=product_name, hackathon_date=hackathon_date, recluting_headcount=recluting_headcount, delete_key=delete_key, product_brief=product_brief, file=file, posted_date=posted_date, post_delete_date=post_delete_date)

    return redirect('hackathonguild:index')


def join_to_project(request, post_id):
    participant_name = request.POST.get('participant_name')
    participant_mail = request.POST.get('participant_mail')
    enthusiasm = request.POST.get('enthusiasm')
    participate_product_id = request.POST.get('participate_product_id')
    participate_date = timezone.now()
    queryset = Post.objects.get(id = participate_product_id)

    accept_participant_url = 'http://127.0.0.1:8000/hackathonguild/accept_participant/' + secrets.token_urlsafe(64)
  
    to_mail = (queryset.poster_mail,)
    from_address = 'ibguild2021@gmail.com'
    mail_subject = '参加希望が届いています'
    mail_massage = str(participant_name)+'からの参加希望が届いています。承認はこちらから' + accept_participant_url
    
    Participant.objects.create(participant_name=participant_name, participant_mail=participant_mail, enthusiasm=enthusiasm, participate_product_id=participate_product_id, participate_date=participate_date)
    #print(mail_message)
    #print(to_mail)
    send_slack_message(mail_message)
    send_email(mail_message,to_mail)
    #send_mail(mail_subject, mail_message, from_address, to_mail, fail_silently=False)

    return redirect('hackathonguild:index')


def accept_participant(request, token):
    #token = request.META.get('HTTP_X_AUTH_TOKEN')

    if not token:
        # リクエストヘッダにトークンが含まれない場合はエラー
        raise exceptions.AuthenticationFailed({'message': 'token injustice.'})

    # トークン文字列からトークンを取得する
    token = ExampleToken.get(token_str)
    if token == None:
        # トークンが取得できない場合はエラー
        raise exceptions.AuthenticationFailed({'message': 'Token not found.'})

    # トークンが取得できた場合は、有効期間をチェック
    if not token.check_valid_token():
        # 有効期限切れの場合はエラー
        raise exceptions.AuthenticationFailed({'message': 'Token expired.'})

    return redirect('hackathonguild:index')


def make_random_string(length):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def delete_POST(request,post_id):
    input_key = request.POST.get('delete_key')
    del_POS = Post.objects.get(id = post_id)
    delete_key = del_POS.delete_key
    if delete_key == input_key:
        del_POS.delete()
        return redirect('hackathonguild:index')

    else:
        return redirect('hackathonguild:index')
