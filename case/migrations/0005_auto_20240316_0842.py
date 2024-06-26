# Generated by Django 3.2 on 2024-03-16 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0004_auto_20240309_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.AlterField(
            model_name='case',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название кейса'),
        ),
        migrations.AddField(
            model_name='case',
            name='categories',
            field=models.ManyToManyField(related_name='cases', to='case.Category', verbose_name='Категории'),
        ),
    ]
