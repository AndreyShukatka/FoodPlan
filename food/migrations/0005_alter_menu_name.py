# Generated by Django 4.1.7 on 2023-03-16 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0004_menu_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Тип меню'),
        ),
    ]