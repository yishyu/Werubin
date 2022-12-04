# Generated by Django 4.1.2 on 2022-12-04 11:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('travels', '0006_alter_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='Commentlikes', to=settings.AUTH_USER_MODEL, verbose_name='Likes'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
    ]