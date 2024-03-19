from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, keys_count=0)

class UserProfile(models.Model):

    def default_avatar_path():
        return 'profile/default.jpg'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    image_profiles = ResizedImageField(
        verbose_name='Аватар', force_format="WEBP", quality=75, upload_to="profiles/avatars", default=default_avatar_path)
    keys_count = models.IntegerField(default=0, verbose_name='Количество ключей')

    def add_key(self, count=1):
        self.keys_count += count
        self.save()

    def remove_key(self, count=1):
        if self.keys_count > 0:
            self.keys_count -= count
            self.save()

    class Meta:
        verbose_name = 'Игровой профиль'
        verbose_name_plural = 'Игровые профили'
