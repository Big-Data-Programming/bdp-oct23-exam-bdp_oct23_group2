from django.db import models


# Github Data Models
class User(models.Model):
    github_username = models.CharField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100)

class Repository(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100, null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    forks = models.IntegerField(null=True, blank=True)
    last_commit_date = models.DateField()

class Commit(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    message = models.TextField()

class Issue(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    open_issues = models.IntegerField()
    closed_issues = models.IntegerField()

class PullRequest(models.Model):
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    open_prs = models.IntegerField()
    merged_prs = models.IntegerField()

class GitHubUserContribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_commits = models.IntegerField()
    total_pr_opened = models.IntegerField()
    total_pr_merged = models.IntegerField()
    total_issues_opened = models.IntegerField()
    total_issues_closed = models.IntegerField()
    daily_date = models.DateField()
    daily_commits = models.IntegerField()
    daily_pr_opened = models.IntegerField()
    daily_pr_merged = models.IntegerField()
    daily_issues_opened = models.IntegerField()
    daily_issues_closed = models.IntegerField()


# StackOverflow Data Models
class StackOverflowUser(models.Model):
    stackoverflow_username = models.CharField(max_length=100, unique=True)
    reputation = models.IntegerField()
    badges = models.IntegerField()

class QuestionAnswer(models.Model):
    user = models.ForeignKey(StackOverflowUser, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    total_answers = models.IntegerField()
    question_upvotes = models.IntegerField()
    question_downvotes = models.IntegerField()
    answer_upvotes = models.IntegerField()
    answer_downvotes = models.IntegerField()

class Tags(models.Model):
    user = models.ForeignKey(StackOverflowUser, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=100)



