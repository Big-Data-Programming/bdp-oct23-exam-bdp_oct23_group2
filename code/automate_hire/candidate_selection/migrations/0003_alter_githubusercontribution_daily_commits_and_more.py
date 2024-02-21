# Generated by Django 5.0.1 on 2024-02-21 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidate_selection', '0002_alter_repository_forks_alter_repository_language_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_commits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_issues_closed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_issues_opened',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_pr_merged',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='githubusercontribution',
            name='daily_pr_opened',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]