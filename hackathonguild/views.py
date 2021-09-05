from django.db.models import query
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from rest_framework import exceptions
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Participant
from .tasks import send_email, send_slack_message
import random
import string
import datetime
import secrets


# ページネーション用に、Pageオブジェクトを返す。
def paginate_query(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginatot.page(paginator.num_pages)
    return page_obj


def index(request):
    latest_posts = Post.objects.order_by('-posted_date')
    page_obj = paginate_query(request, latest_posts, settings.PAGE_PER_ITEM)  # ページネーション

    context = {
        'latest_posts': latest_posts,
        'page_obj': page_obj,
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
    webhookURL = request.POST.get('webhookURL')
    product_name = request.POST.get('product_name')
    hackathon_date = request.POST.get('hackathon_date')
    recluting_headcount = request.POST.get('recluting_headcount')
    product_brief = request.POST.get('product_brief')
    file = request.POST.get('file')

    delete_key = make_random_string(8)
    posted_date = timezone.datetime.now()
    post_delete_date = timezone.datetime.now() + datetime.timedelta(hours=1)

    post_to_DB = Post.objects.create(poster_name=poster_name, poster_mail=poster_mail, webhookURL=webhookURL, product_name=product_name, hackathon_date=hackathon_date,
                                     recluting_headcount=recluting_headcount, delete_key=delete_key, product_brief=product_brief, file=file, posted_date=posted_date, post_delete_date=post_delete_date)

    to_mail = (poster_mail,)
    mail_message = '投稿が完了しました．\n投稿の削除キーは' + delete_key + 'です．'
    send_email(mail_message, to_mail)

    return redirect('hackathonguild:index')


def join_to_project(request, post_id):
    participant_name = request.POST.get('participant_name')
    participant_mail = request.POST.get('participant_mail')
    enthusiasm = request.POST.get('enthusiasm')
    participate_product_id = request.POST.get('participate_product_id')
    participate_date = timezone.datetime.now()
    queryset = Post.objects.get(id=participate_product_id)

    endpoint = queryset.webhookURL
    to_mail = (queryset.poster_mail,)

    token = secrets.token_urlsafe(64)
    token_delete_date = timezone.datetime.now() + timezone.timedelta(days=1)
    accept_participant_url = 'http://127.0.0.1:8000/hackathonguild/jump_to_accept_participant/' + token

    mail_message = str(participant_name)+'からの参加希望が届いています。承認はこちらから' + accept_participant_url

    Participant.objects.create(participant_name=participant_name, participant_mail=participant_mail, enthusiasm=enthusiasm,
                               participate_product_id=participate_product_id, participate_date=participate_date, token=token, token_delete_date=token_delete_date)

    if endpoint is not '':
        send_slack_message(mail_message, endpoint)
    send_email(mail_message, to_mail)

    return redirect('hackathonguild:index')


def jump_to_accept_participant(request, token):
    if not token:
        # リクエストヘッダにトークンが含まれない場合はエラー
        raise exceptions.AuthenticationFailed({'message': 'リンクにトークンが含まれていませんでした．'})

    if Participant.objects.filter(token=token).exists():
        participant_query_set = Participant.objects.get(token=token)
        if timezone.datetime.now() < participant_query_set.token_delete_date:
            context = {
                'token': token
            }
            return render(request, 'hackathonguild/accept_participant.html', context)
    else:
        return HttpResponse('有効なトークンではありませんでした．')


def accept_participant(request):
    token = request.POST.get('token')
    print(token)
    participant_query_set = Participant.objects.get(token=token)
    if timezone.datetime.now() < participant_query_set.token_delete_date:
        to_mail = (participant_query_set.participant_mail,)
        poster_queryset = Post.objects.get(id=participant_query_set.participate_product_id)
        mail_message = str(poster_queryset.product_name)+'への参加が受諾されました！'
        send_email(mail_message, to_mail)
        participant_query_set.token = ''
        participant_query_set.save()

        poster_queryset.joining_headcount += 1
        poster_queryset.save()

        return redirect('hackathonguild:index')
    else:
        return HttpResponse('有効なトークンではありませんでした．')


def make_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def delete_POST(request, post_id):
    input_key = request.POST.get('delete_key')
    del_POS = Post.objects.get(id=post_id)
    delete_key = del_POS.delete_key
    if delete_key == input_key:
        del_POS.delete()
        return redirect('hackathonguild:index')

    else:
        return redirect('hackathonguild:index')
