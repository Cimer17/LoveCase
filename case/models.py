from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, keys_count=0)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    keys_count = models.IntegerField(default=0, verbose_name='Количество ключей')

    def add_key(self, count=1):
        self.keys_count += count
        self.save()

    def remove_key(self, count=1):
        if self.keys_count > 0:
            self.keys_count -= count
            self.save()

    class Meta:
        verbose_name = 'Ключ'
        verbose_name_plural = 'Ключи'

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    title = models.CharField(max_length=200, verbose_name='Описание(тег)')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Case(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название кейса')
    img_certificates = ResizedImageField(
        verbose_name='Изображение', force_format="WEBP", quality=75, upload_to="case")
    categories = models.ManyToManyField(Category, related_name='cases', verbose_name='Категории')

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'

    def delete(self, *args, **kwargs):
        storage, path = self.img_certificates.storage, self.img_certificates.path
        super(Case, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.name
    

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    img = ResizedImageField(
        verbose_name='Изображение', force_format="WEBP", quality=75, upload_to="items")
    quantity = models.IntegerField(verbose_name='Количество')
    chance = models.FloatField(default=0.0, verbose_name='Шанс выпадения')
    cases = models.ManyToManyField(Case, related_name='items', verbose_name='Кейсы')
    rare = models.IntegerField(choices=[(i, i) for i in range(1, 7)], verbose_name='Редкость', default=1)
    users = models.ManyToManyField(User, through='UserItem')


    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def delete(self, *args, **kwargs):
        storage, path = self.img.storage, self.img.path
        super(Item, self).delete(*args, **kwargs)
        storage.delete(path)

    def __str__(self):
        return self.name
    

class UserItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Предмет')
    conclusion = models.BooleanField(default=False, verbose_name='Выведено')
    received_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения') 

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
    
    class Meta:
        verbose_name = 'Вывод пользователей'
        verbose_name_plural = 'Выводы пользователей'


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Пользователь, сделавший выбор
    chosen_item_id = models.IntegerField()  # Идентификатор выбранного предмета
    case_id = models.IntegerField()  # Идентификатор кейса
    hash_value = models.CharField(max_length=32)  # Хеш для проверки справедливости

    def __str__(self):
        return f"Игра пользователя {self.user.username}, Выпавший предмет: {self.chosen_item_id}, ID кейса: {self.case_id}"
    

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Промокод')
    keys_count = models.IntegerField(verbose_name='Количество ключей')
    is_single_use = models.BooleanField(default=True, verbose_name='Одноразовый промокод')
    activations_left = models.IntegerField(default=1, verbose_name='Количество активаций')
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промкоды'
    def __str__(self):
        return self.code
    
class UsedPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='used_promo_codes', verbose_name='Пользователь')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, verbose_name='Использованный промокод')

    class Meta:
        unique_together = ('user', 'promo_code')