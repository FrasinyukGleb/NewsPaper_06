from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from .models import Post, Category, PostCategory

import logging
logger = logging.getLogger(__name__)

@shared_task
def send_post_notification(pk):
    post = Post.objects.get(pk=pk)
    categories = post.category.all()
    subscribers_emails = []

    for cat in categories:
        subscribers = cat.subscribers.all()
        subscribers_emails += [s.email for s in subscribers]


    html_content = render_to_string(
        'post_created_celery.html',
        {
            'text': post.preview,
            'link': f'http://127.0.0.1:8000/news/{pk}',

        }
    )

    msg = EmailMultiAlternatives(
        subject=post.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()



@shared_task
def weekly_update():
    last_week = timezone.now() - timezone.timedelta(days=7)
    categories = Category.objects.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if not subscribers:
            continue

        new_posts = Post.objects.filter(
            category=category,
            date_add__gte=last_week
        )

        if new_posts.exists():
            subject = f'Новые статьи в категории {category.name} за неделю'
            from_email = settings.DEFAULT_FROM_EMAIL

            for subscriber in subscribers:
                html_content = render_to_string('weekly_newsletter.html', {
                    'category': category,
                    'posts': new_posts
                })
                text_content = f'Новые статьи в категории {category.name} за неделю:\n\n' + \
                               '\n'.join([post.title for post in new_posts])

                msg = EmailMultiAlternatives(subject, text_content, from_email, [subscriber.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()