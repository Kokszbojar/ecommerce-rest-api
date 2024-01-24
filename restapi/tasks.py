from datetime import timedelta

from celery import shared_task

from django.utils import timezone
from django.core.mail import send_mail

from restapi.models import Order

def send_reminder_mails(recipients):
    subject = 'Payment Reminder'
    message = 'This is a reminder mail. You have less than 24 hours to pay for your order.'
    from_email = 'noreply@mysite.com'
    recipient_list = recipients
    send_mail(subject, message, from_email, recipient_list)

@shared_task(name='reminder_mails_task')
def reminder_mails_task():
    time_now = timezone.now()
    orders = Order.objects.filter(payment_date__gte=time_now, payment_date__lte=time_now+timedelta(days=1), cart_confirmed=True)
    recipients = []
    for order in orders:
        recipients.append(order.client.email)
    send_reminder_mails(recipients)
