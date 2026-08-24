from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string


@shared_task
def add(x, y):
    return x + y


@shared_task
def send_email_task(subject, message, from_email, recipient_list):
    send_mail(subject, message, from_email, recipient_list)


@shared_task
def send_test_email_task(recipient_email, task_id):
    context = {'task_id': task_id}
    html_content = render_to_string('acount/test_task.html', context)

    email = EmailMessage(
        subject='Test de tâche Celery',
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.content_subtype = 'html'
    email.send(fail_silently=False)
    return {
        'status': 'email_sent',
        'recipient': recipient_email,
        'task_id': task_id,
    }