# Generated by Django 5.2 on 2025-07-31 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_alter_enquirybooking_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='points',
            field=models.TextField(blank=True, null=True),
        ),
    ]
