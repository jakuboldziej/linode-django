# Generated by Django 4.0.5 on 2022-07-08 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_image_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='title',
            field=models.CharField(blank=True, default='image', max_length=100, null=True),
        ),
    ]
