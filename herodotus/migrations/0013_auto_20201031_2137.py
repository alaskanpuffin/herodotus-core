# Generated by Django 3.1 on 2020-10-31 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herodotus', '0012_auto_20201031_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('article', 'article'), ('note', 'note')], max_length=30),
        ),
    ]