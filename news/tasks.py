from celery import shared_task

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone


from .models import Post, Category

import logging
logger = logging.getLogger(__name__)

@shared_task
def send_post_notification(post, subscribers):
    pass
    for user in subscribers:
        # Получаем наш html с учетом пользователя
        html_content = render_to_string(
            'post_created.html',
            {
                'post': post,
                'user': user,
            }
        )

        # Отправка письма
        msg = EmailMultiAlternatives(
            subject=f'{post.title} | {post.date_add.strftime("%Y-%m-%d")}',
            body=post.text,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        print(f'DEBUG: Sended email - {user.email}')
        msg.send()  # отсылаем


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