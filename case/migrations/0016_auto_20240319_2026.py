# Generated by Django 3.2 on 2024-03-19 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0015_auto_20240317_1909'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='usedpromocode',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='usedpromocode',
            name='promo_code',
        ),
        migrations.RemoveField(
            model_name='usedpromocode',
            name='user',
        ),
        migrations.DeleteModel(
            name='PromoCode',
        ),
        migrations.DeleteModel(
            name='UsedPromoCode',
        ),
    ]
