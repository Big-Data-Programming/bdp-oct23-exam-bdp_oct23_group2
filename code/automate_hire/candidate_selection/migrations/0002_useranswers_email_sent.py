# Generated by Django 5.0.1 on 2024-03-10 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_selection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswers',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]