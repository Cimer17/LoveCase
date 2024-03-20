from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import User

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
    case = models.ForeignKey(Case, on_delete=models.CASCADE, verbose_name='Кейс')
    conclusion = models.BooleanField(default=False, verbose_name='Выведено')
    received_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата получения')
    client_seed = models.CharField(max_length=255, verbose_name='Client Seed')
    server_seed = models.CharField(max_length=255, verbose_name='Server Seed')
    nonce = models.IntegerField(default=0, verbose_name='Nonce')
    hash_seed = models.CharField(max_length=255, verbose_name='hash')
    
    def __str__(self):
        return f"{self.user.username} - {self.item.name}"
    
    class Meta:
        verbose_name = 'Live лента'
        verbose_name_plural = 'Live лента'