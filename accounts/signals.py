from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def add_user_to_group(sender, instance, created, **kwargs):
    print("Signal triggered")  # This will print when the signal is triggered
    if created and instance.role:
        group, _ = Group.objects.get_or_create(name=instance.role)
        print("Group:", group)  # This will print the group
        instance.groups.add(group)
