# Generated by Django 3.1 on 2020-08-23 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herodotus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('article', 'article'), ('note', 'note')], max_length=30)),
                ('url', models.CharField(blank=True, max_length=500, null=True)),
                ('author', models.CharField(blank=True, max_length=300, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=500)),
                ('content', models.TextField()),
            ],
        ),
    ]
