# Generated by Django 3.2.10 on 2022-01-11 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=256)),
                ('password', models.CharField(max_length=256)),
            ],
        ),
    ]
