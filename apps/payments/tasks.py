from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_email_for_donor(user_email, amount, collect_title):
    subject = 'Платеж отправлен!'
    message = (
        f'Ваш платеж {amount} успешно отправлен на групповой денежный сбор '
        f'"{collect_title}". Спасибо за участие!'
    )
    from_email = EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list)
