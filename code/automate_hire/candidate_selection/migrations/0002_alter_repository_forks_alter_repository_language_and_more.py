# Generated by Django 5.0.1 on 2024-02-21 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_selection', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='forks',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='repository',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='repository',
            name='stars',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
