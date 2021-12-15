import logging

from celery import shared_task
from django.core.mail import EmailMessage
from django.template import loader

logger = logging.getLogger("celery")


@shared_task(bind=True, max_retries=3)
def send_email(self, subject, template, emails, context):
    body = loader.render_to_string(template, context)
    email = EmailMessage(
        subject, body, to=emails
    )

    email.content_subtype = 'html'
    try:
        logger.info(f"Sending email to '{emails}'")
        email.send(fail_silently=False)
        logger.info(f"Email notification sent to {emails}.")
    except ConnectionError as exc:
        self.retry(exc=exc, countdown=180)
        logger.error(f"Email to {emails} timeout error!")
