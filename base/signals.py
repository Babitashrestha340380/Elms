# base/signals.py

from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group

from base.models import Assignment, Enrollment, Notification
from base.utils.email_utils import (
    send_student_deadline_email,
    send_sponsor_progress_email,
    send_instructor_progress_email
)

# ---------------------------------
# Create default user groups after migrations
# ---------------------------------
@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Create default roles for the system after migrations."""
    groups = ['Admin', 'Instructor', 'Student', 'Sponsor']
    for group in groups:
        Group.objects.get_or_create(name=group)


# ---------------------------------
# Notify students when a new assignment is created
# ---------------------------------
@receiver(post_save, sender=Assignment)
def notify_students_new_assignment(sender, instance, created, **kwargs):
    """
    Sends notification and email to all students enrolled in the course
    when a new assignment is created.
    """
    if not created:
        return

    enrollments = Enrollment.objects.filter(course=instance.course).select_related('student')

    for enrollment in enrollments:
        student = enrollment.student

        # Create Notification in DB
        message = (
            f"New assignment '{instance.title}' in course '{instance.course.name}' "
            f"due on {instance.due_date.strftime('%Y-%m-%d %H:%M')}."
        )
        Notification.objects.create(user=student, message=message)

        # Send email if student has email
        if student.email:
            send_student_deadline_email(
                student_name=student.username,
                course_name=instance.course.name,
                deadline=instance.due_date,
                recipient_list=[student.email]
            )


# ---------------------------------
# Notify sponsors about student progress
# ---------------------------------
@receiver(post_save, sender=Enrollment)
def notify_sponsor_progress(sender, instance, **kwargs):
    """
    Sends notification and email to sponsors about the progress
    of their sponsored students.
    """
    student = instance.student
    # related_name of Sponsorship model: sponsored_students
    sponsorships = student.sponsored_students.select_related("sponsor")

    for sponsorship in sponsorships:
        sponsor = sponsorship.sponsor

        # Create Notification in DB
        Notification.objects.create(
            user=sponsor,
            message=(
                f"Student '{student.username}' has completed {instance.progress}% "
                f"of course '{instance.course.name}'."
            )
        )

        # Send email if sponsor has email
        if sponsor.email:
            send_sponsor_progress_email(
                sponsor_name=sponsor.username,
                student_name=student.username,
                progress=instance.progress,
                recipient_list=[sponsor.email]
            )


# ---------------------------------
# Notify instructors about student course progress
# ---------------------------------
@receiver(post_save, sender=Enrollment)
def notify_instructor_course_progress(sender, instance, **kwargs):
    """
    Sends notification and email to the instructor of the course
    whenever a student's progress is updated.
    """
    instructor = instance.course.instructor

    # Create Notification in DB
    Notification.objects.create(
        user=instructor,
        message=(
            f"Student '{instance.student.username}' has completed {instance.progress}% "
            f"of course '{instance.course.name}'."
        )
    )

    # Send email if instructor has email
    if instructor.email:
        send_instructor_progress_email(
            student_name=instance.student.username,
            instructor_name=instructor.username,
            progress=instance.progress,
            recipient_list=[instructor.email]
        )
