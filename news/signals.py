from django.conf import settings
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, User, PostCategory

# def send_post_notification(post, subscribers):
#     pass
#     for user in subscribers:
#         # Получаем наш html с учетом пользователя
#         html_content = render_to_string(
#             'post_created.html',
#             {
#                 'post': post,
#                 'user': user,
#             }
#         )
#
#         # Отправка письма
#         msg = EmailMultiAlternatives(
#             subject=f'{post.title} | {post.date_add.strftime("%Y-%m-%d")}',
#             body=post.text,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             to=[user.email],
#         )
#         msg.attach_alternative(html_content, "text/html")  # добавляем html
#         print(f'DEBUG: Sended email - {user.email}')
#         msg.send()  # отсылаем
#
#
# @receiver(m2m_changed, sender=Post)
# def new_post_notifier(sender, instance, **kwargs):
#     if kwargs['action'] == 'post_add':
#         categories = instance.category.all()
#         subscribers = []
#         for category in categories:
#             subscribers += category.subscribers.all()
#
#         subscribers = [s.email for s in subscribers]
#
#         send_post_notification(instance.preview(), instance.pk, instance.title, subscribers)

