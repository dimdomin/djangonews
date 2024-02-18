from .models import Post, Category
from django.conf import settings
import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


@shared_task
def post_created(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/post/{pk}'  # http://127.0.0.1:8000/post/pk
        }
    )

    msg = EmailMultiAlternatives(subject=title, body='', from_email=settings.DEFAULT_FROM_EMAIL, to=subscribers)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_send_emails():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(data_creation__gte=last_week)
    categories = set(posts.values_list('category__title', flat=True))
    subscribers = set(Category.objects.filter(title__in=categories).values_list('subscribers', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'Новые статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[],
        bcc=subscribers,  # скрывает адреса получателей
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()