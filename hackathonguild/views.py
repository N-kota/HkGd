from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Post, Participant
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import random
import string
import datetime


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
    poster_mail = ('taukoman1025@gmail.com',)
    from_address = 'ibguild2021@gmail.com'
    mail_subject = '参加希望が届いています'
    mail_massage = 'participant_nameからの参加希望が届いています。承認はこちらから'

    Participant.objects.create(participant_name=participant_name, participant_mail=participant_mail, enthusiasm=enthusiasm, participate_product_id=participate_product_id, participate_date=participate_date)

    print(poster_mail)
    send_mail(mail_subject, mail_massage, from_address, poster_mail, fail_silently=False)

    return redirect('hackathonguild:index')



def make_random_string(length):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=length))