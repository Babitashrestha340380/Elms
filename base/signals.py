from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Create default roles for the system."""
    groups = ['Admin', 'Instructor', 'Student', 'Sponsor']
    for group in groups:
        Group.objects.get_or_create(name=group)
