from django.db import models
from django.contrib.auth.models import User

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name='Промокод')
    keys_count = models.IntegerField(verbose_name='Количество ключей')
    is_single_use = models.BooleanField(default=True, verbose_name='Одноразовый промокод')
    activations_left = models.IntegerField(default=1, verbose_name='Количество активаций')
    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'
    def __str__(self):
        return self.code
    
class UsedPromoCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='used_promo_codes', verbose_name='Пользователь')
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE, verbose_name='Использованный промокод')

    class Meta:
        unique_together = ('user', 'promo_code')