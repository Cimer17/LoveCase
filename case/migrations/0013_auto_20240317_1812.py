# Generated by Django 3.2 on 2024-03-17 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('case', '0012_alter_useritem_received_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useritem',
            options={'verbose_name': 'Вывод пользователей', 'verbose_name_plural': 'Выводы пользователей'},
        ),
        migrations.AddField(
            model_name='userprofile',
            name='keys_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='conclusion',
            field=models.BooleanField(default=False, verbose_name='Выведено'),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.item', verbose_name='Предмет'),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='received_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата получения'),
        ),
        migrations.AlterField(
            model_name='useritem',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]