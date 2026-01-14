from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    """Represents a course taught by an instructor."""
    DIFFICULTY_CHOICES = [('Beginner','Beginner'), ('Intermediate','Intermediate'), ('Advanced','Advanced')]
    
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """Tracks student enrollment in courses."""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    progress = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    enrolled_at = models.DateTimeField(auto_now_add=True)


class Assignment(models.Model):
    """Assignments associated with courses."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    max_marks = models.IntegerField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title} ({self.course.name})"


class Sponsorship(models.Model):
    """Sponsors fund students."""
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsorships')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsored_students')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Active','Active'),('Completed','Completed')], default='Active')
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    """Notifications for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    """Payments made by sponsors for students."""
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsored_payments')
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('completed','Completed')], default='pending')

    def __str__(self):
        return f"{self.sponsor.username} → {self.student.username} ({self.amount})"



# base/models.py
