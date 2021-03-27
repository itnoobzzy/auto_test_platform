from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserInfo

@receiver(post_save, sender=UserInfo)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        instance.user_password = UserInfo.objects.get_md5(instance.user_password)
        instance.save()