import asyncio
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render

from .models import User, Repository, Commit, Issue, PullRequest, GitHubUserContribution
from .data_processing import create_user_df, create_repository_df, create_commit_df, create_issue_df, create_pull_request_df, cluster_users


from .services.data_insertion import fetch_data_github



def fetch_from_github_view(request):
    """
        fetch data from github and insert it into the database.
    """

    asyncio.run(fetch_data_github())
    return HttpResponse('Data fetched and inserted successfully!') 

def read_from_database_view():
    """
    Read data from the database and return it as a dictionary of Pandas DataFrames.

    Returns:
        dict: Dictionary containing data from the database.

    """
    users = User.objects.all()
    repositories = Repository.objects.all()
    commits = Commit.objects.all()
    issues = Issue.objects.all()
    pull_requests = PullRequest.objects.all()
    user_contributions = GitHubUserContribution.objects.all()

    users_df = pd.DataFrame(list(users.values()))
    repositories_df = pd.DataFrame(list(repositories.values()))
    commits_df = pd.DataFrame(list(commits.values()))
    issues_df = pd.DataFrame(list(issues.values()))
    pull_requests_df = pd.DataFrame(list(pull_requests.values()))
    user_contributions_df = pd.DataFrame(list(user_contributions.values()))


    return {
        'users': users_df,
        'repositories': repositories_df,
        'commits': commits_df,
        'issues': issues_df,
        'pull_requests': pull_requests_df,
        'user_contributions': user_contributions_df
    }

def cluster_users_view(request):
    """
    Cluster users based on their contributions to repositories.
    """
    user_df = create_user_df()
    repository_df = create_repository_df()
    commit_df = create_commit_df()
    issue_df = create_issue_df()
    pull_request_df = create_pull_request_df()


    clustered_data = cluster_users(user_df, repository_df, commit_df, issue_df, pull_request_df)

    # return render(request, 'cluseterd_users.html', {'clustered_data': clustered_data})
    return HttpResponse('Data fetched and inserted successfully!')


def run_selection_algorithm(request):
    pass





