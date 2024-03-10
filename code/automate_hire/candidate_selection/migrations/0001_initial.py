# Generated by Django 5.0.1 on 2024-03-09 12:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('stars', models.IntegerField(blank=True, null=True)),
                ('forks', models.IntegerField(blank=True, null=True)),
                ('last_commit_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='StackOverflowUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stackoverflow_username', models.CharField(max_length=100, unique=True)),
                ('reputation', models.IntegerField()),
                ('badges', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_username', models.CharField(max_length=100, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_prs', models.IntegerField()),
                ('merged_prs', models.IntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.repository')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_issues', models.IntegerField()),
                ('closed_issues', models.IntegerField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.repository')),
            ],
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('message', models.TextField()),
                ('repository', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.repository')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_questions', models.IntegerField(blank=True, null=True)),
                ('total_answers', models.IntegerField(blank=True, null=True)),
                ('question_upvotes', models.IntegerField(blank=True, null=True)),
                ('question_downvotes', models.IntegerField(blank=True, null=True)),
                ('answer_upvotes', models.IntegerField(blank=True, null=True)),
                ('answer_downvotes', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.stackoverflowuser')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.stackoverflowuser')),
            ],
        ),
        migrations.AddField(
            model_name='repository',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.user'),
        ),
        migrations.CreateModel(
            name='GitHubUserContribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_commits', models.IntegerField()),
                ('total_pr_opened', models.IntegerField()),
                ('total_pr_merged', models.IntegerField()),
                ('total_issues_opened', models.IntegerField()),
                ('total_issues_closed', models.IntegerField()),
                ('daily_date', models.DateField(blank=True, null=True)),
                ('daily_commits', models.IntegerField(blank=True, null=True)),
                ('daily_pr_opened', models.IntegerField(blank=True, null=True)),
                ('daily_pr_merged', models.IntegerField(blank=True, null=True)),
                ('daily_issues_opened', models.IntegerField(blank=True, null=True)),
                ('daily_issues_closed', models.IntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.user')),
            ],
        ),
        migrations.CreateModel(
            name='UserAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer1', models.CharField(blank=True, max_length=100, null=True)),
                ('answer2', models.CharField(blank=True, max_length=100, null=True)),
                ('answer3', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(default='pending', max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='candidate_selection.user')),
            ],
        ),
    ]
