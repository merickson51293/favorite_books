# Generated by Django 2.2 on 2020-11-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='favorited_by',
            field=models.ManyToManyField(related_name='favorited_books', to='books_app.User'),
        ),
    ]