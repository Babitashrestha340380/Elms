from django.core.mail import send_mail

def send_student_deadline_email(email, course_name, deadline):
    send_mail(
        subject='Course Deadline Reminder',
        message=f'Your course "{course_name}" has a deadline on {deadline}.',
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

def send_sponsor_progress_email(email, student_name, progress):
    send_mail(
        subject='Student Progress Report',
        message=f'Student {student_name} has completed {progress}% of the course.',
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )
