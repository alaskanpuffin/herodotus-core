# Generated by Django 3.1 on 2020-10-05 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('herodotus', '0007_feedhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('article', 'article'), ('note', 'note')], max_length=30),
        ),
        migrations.AddField(
            model_name='content',
            name='tags',
            field=models.ManyToManyField(to='herodotus.Tag'),
        ),
    ]
