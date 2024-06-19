from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail, EmailMultiAlternatives
from .models import Article, Comment
from .tasks import comment_created_task, confirm_comment_task


# Сигнал создания комментария
@receiver(post_save, sender=Comment)
def comment_created(instance, created, **kwargs):
    if created:
        comment_created_task.delay(instance.pk)


# Сигнал подтверждения комментария
@receiver(post_save, sender=Comment)
def confirm_comment(instance, created, **kwargs):
    if not created:
        confirm_comment_task.delay(instance.pk)