# Generated by Django 3.2 on 2024-03-17 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0011_useritem_received_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useritem',
            name='received_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
