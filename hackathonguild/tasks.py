import json
import requests
from django.core.mail import send_mail
from django.template.loader import get_template
import config.settings as settings


# メール送信
def send_email(message,toaddress):
    subject = '参加希望が届いています'
    from_address = 'ibguild2021@gmail.com'
    to_address = toaddress
    send_mail(subject, message, from_address, to_address)


# Slack投稿(Incoming Webhook 使用)
def send_slack_message(message):
    requests.post(settings.SLACK_WEBHOOK_ENDPOINT,
                  data=json.dumps({
                      'text': message,  # 投稿するテキスト
                      'username': u'me',  # 投稿のユーザー名
                      'icon_emoji': u':ghost:',  # 投稿のプロフィール画像に入れる絵文字
                      'link_names': 1,  # メンションを有効にする
                  }))

# メールの本文を作成する
def get_message(item, action):
    template = get_template('hackthonguild/message.txt')
    context = {
        "item": item, "action": action,
    }
    message = template.render(context)
    return message