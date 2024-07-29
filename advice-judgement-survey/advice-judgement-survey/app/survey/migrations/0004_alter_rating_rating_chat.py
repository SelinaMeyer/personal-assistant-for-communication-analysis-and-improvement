# Generated by Django 3.2.25 on 2024-06-28 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0003_rating_rating_chat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='rating_chat',
            field=models.CharField(choices=[('mistreated', 'I would feel mistreated'), ('wrong', 'I would feel like I might have done something wrong'), ('neutral', 'I would feel neutral, there is nothing wrong with this conversation')], max_length=255),
        ),
    ]
