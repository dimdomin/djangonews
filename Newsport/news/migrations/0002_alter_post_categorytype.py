# Generated by Django 4.2.7 on 2023-11-27 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categoryType',
            field=models.CharField(choices=[('Nw', 'Новости'), ('Ar', 'Статья')], default='Ar', max_length=2),
        ),
    ]
