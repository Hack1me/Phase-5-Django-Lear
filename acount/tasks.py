from LENOXDEV.celery import sharetask
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



@sharetask
def sentemail(subject, message, fromemail, toemail)