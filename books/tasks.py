from main.celery import app
from django.core.mail import send_mail

@app.task(name='send-email-by-book-task')
def book_email(emails, book):
    send_mail(
        subject = "Info from library.api",
        message = f"Your book {book} have been added in our system",
        from_email = "library@api.com",
        recipient_list = emails,
        fail_silently = False
    )