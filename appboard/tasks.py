from datetime import timedelta

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from board import settings
from appboard.models import Comment, Article, User


@shared_task
def comment_created_task(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    email = comment.commentPost.author.email

    subject = f'На Ваше объявление оставили отклик'

    text_content = (
        f'Объявление: {comment.commentPost}\n'
        f'Описание: {comment.text}\n\n'
        f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
    )
    html_content = (
        f'Объявление: {comment.commentPost}<br>'
        f'Описание: {comment.text}<br><br>'
        f'<a href="http://127.0.0.1:8000/{comment.get_absolute_url()}">'
        f'Ссылка на объявление</a>'
    )

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def confirm_comment_task(comment_id):
    comment = Comment.objects.get(pk=comment_id)
    email = comment.commentPost.author.email

    if comment.status == 'accepted':
        subject = f'Ваш отклик приняли'

        text_content = (
            f'Объявление: {comment.commentPost}\n'
            f'Описание: {comment.text}\n\n'
            f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
            f'Принят автором объявления: {comment.commentPost.author.username}'
        )
        html_content = (
            f'Объявление: {comment.commentPost}<br>'
            f'Описание: {comment.text}<br><br>'
            f'<a href="http://127.0.0.1:8000/{comment.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
            f'Принят автором объявления: {comment.commentPost.author.username}'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    elif comment.status == 'rejected':
        subject = f'Ваш отклик отклонили'
        text_content = (
            f'Объявление: {comment.commentPost}\n'
            f'Описание: {comment.text}\n\n'
            f'Ссылка на объявление: http://127.0.0.1:8000{comment.get_absolute_url()}'
            f'Отклонён автором объявления: {comment.commentPost.author.username}'
        )
        html_content = (
            f'Объявление: {comment.commentPost}<br>'
            f'Описание: {comment.text}<br><br>'
            f'<a href="http://127.0.0.1:8000/{comment.get_absolute_url()}">'
            f'Ссылка на объявление</a>'
            f'Отклонён автором объявления: {comment.commentPost.author.username}'
        )
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_notification():
    today = timezone.now()
    last_week = today - timedelta(days=7)
    posts = Article.objects.filter(dateCreation__gte=last_week)
    emails = set(User.objects.all().values_list('email', flat=True))

    subject = f'Новые публикации за последнюю неделю:'

    html_content = render_to_string(
        'email/weekly_email.html',
        {
            'posts': posts,
            'link': settings.SITE_URL,
        },
    )

    for email in emails:
        msg = EmailMultiAlternatives(
            subject=subject,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()