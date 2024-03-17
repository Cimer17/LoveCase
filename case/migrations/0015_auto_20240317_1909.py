# Generated by Django 3.2 on 2024-03-17 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('case', '0014_auto_20240317_1904'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promocode',
            options={'verbose_name': 'Промокод', 'verbose_name_plural': 'Промкоды'},
        ),
        migrations.CreateModel(
            name='UsedPromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promo_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='case.promocode', verbose_name='Использованный промокод')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used_promo_codes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'unique_together': {('user', 'promo_code')},
            },
        ),
    ]
