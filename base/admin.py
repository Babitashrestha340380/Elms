from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Enrollment, Assignment, Sponsorship, Notification

admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(Assignment)
admin.site.register(Sponsorship)
admin.site.register(Notification)
