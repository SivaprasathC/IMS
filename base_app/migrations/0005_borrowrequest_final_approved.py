# Generated by Django 5.2.1 on 2025-06-21 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0004_borrowrequest_borrow_made_date_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowrequest',
            name='final_approved',
            field=models.BooleanField(default=False),
        ),
    ]
