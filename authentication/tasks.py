import logging

from billiard.exceptions import SoftTimeLimitExceeded
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.template.loader import render_to_string
from mailjet_rest import Client
from rest_framework import status

from django.conf import settings

logger = logging.getLogger("celery")


@shared_task(bind=True, max_retries=3)
def send_email(self, subject, template, recipients, context):
    mailjet = Client(auth=(settings.MAILJET_PUBLIC_KEY, settings.MAILJET_SECRET_KEY),
                     version=settings.MAILJET_API_VERSION)
    recipients = [{'Email': recipient} for recipient in recipients]
    message = render_to_string(template, context)
    data = {
        'Messages': [
            {
                'From': {
                    'Email': settings.MAILJET_USER,
                    'Name': settings.MAILJET_NAME
                },
                'To': recipients,
                'Subject': subject,
                'HTMLPart': message
            }
        ]
    }

    try:
        logger.info(f"Sending email to '{recipients}'")
        result = mailjet.send.create(data=data)
        logger.info(f"Email notification sent to {recipients}.")
    except SoftTimeLimitExceeded as e:
        logger.error(e)
        return
    if result.status_code != status.HTTP_200_OK:
        error = result.json()
        logger.error(f"Something went wrong while send email, Error: {error}")
        try:
            self.retry(countdown=30)
        except MaxRetriesExceededError as e:
            logger.error(e)
