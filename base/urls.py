from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import sponsor_khalti_init, sponsor_khalti_verify

from .views import (
    CourseViewSet,
    EnrollmentViewSet,
    AssignmentViewSet,
    RegisterStudentView,
    SponsorshipViewSet,
    NotificationViewSet,
    admin_dashboard_list,
    sponsor_dashboard,
    send_student_deadline_email,
    send_sponsor_progress_email,
    LoginView,
    make_payment,
    send_email_api,
)

# -------------------------
# DRF ROUTER
# -------------------------
router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'sponsorships', SponsorshipViewSet, basename='sponsorship')
router.register(r'notifications', NotificationViewSet, basename='notification')

# -------------------------
# URL PATTERNS
# -------------------------
urlpatterns = [
    # Router URLs
    path('', include(router.urls)),

    # Auth & Registration
      path('register/student/', RegisterStudentView.as_view(), name='register-student'),
    path('login/', LoginView.as_view(), name='login'),  # ← note the .as_view()
    # Dashboards
    path('admin/dashboard/', admin_dashboard_list, name='admin-dashboard'),
    path('sponsor/dashboard/', sponsor_dashboard, name='sponsor-dashboard'),

    # Email Triggers (Admin only)
    path('notify/students/', send_student_deadline_email, name='notify-students'),
    path('notify/sponsors/', send_sponsor_progress_email, name='notify-sponsors'),
    path('make-payment/', make_payment),
    path("email/send/", send_email_api),
     path("payment/sponsor/init/", sponsor_khalti_init),
    path("payment/sponsor/verify/", sponsor_khalti_verify),


]



