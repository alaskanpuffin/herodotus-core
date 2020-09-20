# Generated by Django 3.1 on 2020-09-20 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herodotus', '0004_auto_20200910_0116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=500)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
