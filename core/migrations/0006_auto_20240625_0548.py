# Generated by Django 3.2.3 on 2024-06-25 05:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20240625_0516'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='image_banner',
            new_name='image_card',
        ),
        migrations.RenameField(
            model_name='movie',
            old_name='image_poster',
            new_name='image_cover',
        ),
    ]
