from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_for_collect_author(user_email, collect_title):
    subject = 'Групповой денежный сбор создан!'
    message = (f'Ваш групповой денежный сбор "{collect_title}" успешно создан.'
               f'Желаем удачи!')
    from_email = EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
