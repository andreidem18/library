from main.celery import app
from django.core.mail import send_mail

@app.task(name='send-email-task')
def author_email(email):
    print("Email sent")
    send_mail(
        subject = "Info about library.api",
        message = "You have been added in our system!",
        from_email = "library@api.com",
        recipient_list = [email],
        fail_silently = False
    )