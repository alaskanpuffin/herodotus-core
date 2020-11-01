# Generated by Django 3.1 on 2020-10-05 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herodotus', '0009_auto_20201005_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('note', 'note'), ('article', 'article')], max_length=30),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
