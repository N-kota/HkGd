# Generated by Django 3.2.7 on 2021-09-04 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackathonguild', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=200, verbose_name='Token')),
            ],
        ),
    ]
