# Generated by Django 3.2 on 2024-03-19 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0019_auto_20240319_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='useritem',
            name='hash_seed',
            field=models.CharField(default=1, max_length=255, verbose_name='hash'),
            preserve_default=False,
        ),
    ]