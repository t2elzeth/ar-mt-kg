# Generated by Django 3.1.2 on 2020-10-28 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ar',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='ar',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]