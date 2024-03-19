from django.db import models
from django.contrib.auth.models import User


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