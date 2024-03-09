from django.db import models
from django_resized import ResizedImageField

class Case(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название кейса:')
    img_certificates = ResizedImageField(
        verbose_name='Изображение', force_format="WEBP", quality=75, upload_to="case")

    class Meta:
        verbose_name = 'Кейс'
        verbose_name_plural = 'Кейсы'

    def __str__(self):
        return self.name
    

class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование:')
    img = ResizedImageField(
        verbose_name='Изображение', force_format="WEBP", quality=75, upload_to="items")
    quantity = models.IntegerField(verbose_name='Количество:')
    chance = models.FloatField(default=0.0, verbose_name='Шанс выпадения:')
    case = models.ForeignKey(Case, related_name='items', on_delete=models.CASCADE, verbose_name='Из какого кейса:')
    rare = models.IntegerField(choices=[(i, i) for i in range(1, 7)], verbose_name='Редкость', default=1)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.name
