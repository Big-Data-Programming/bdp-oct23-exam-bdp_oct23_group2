from candidate_selection.models import User
from datetime import datetime

from asgiref.sync import sync_to_async



def clean_github_user_data(user_data):
    """
    Clean fetched GitHub user data before saving to the database.

    Parameters:
        user_data (dict): Dictionary containing user data fetched from GitHub.

    Returns:
        dict: Cleaned user data.
    """
    cleaned_data = {}
    if not user_data.login or not user_data.name or not user_data.email or not user_data.location:
        return None
    else:
        cleaned_data['github_username'] = user_data.login
        cleaned_data['full_name'] = user_data.name
        cleaned_data['email'] = user_data.email
        cleaned_data['location'] = user_data.location
    return cleaned_data

def clean_repository_data(repository_data):
    """
    Clean fetched repository data before saving to the database.

    Parameters:
        repository_data (dict): Dictionary containing repository data fetched from GitHub.

    Returns:
        dict: Cleaned repository data.
    """
    if not repository_data.get('name', ''):
        return None
    cleaned_data = {
        'name': repository_data.get('name', ''),
        'language': repository_data.get('language', None),
        'stars': repository_data.get('stars', 0),
        'forks': repository_data.get('forks', 0),
        'last_commit_date': repository_data.get('last_commit_date', None)  # Set to None if missing
    }

    if cleaned_data['last_commit_date'] is not None:
        try:
            cleaned_data['last_commit_date'] = datetime.strptime(cleaned_data['last_commit_date'], '%Y-%m-%d').date()
        except ValueError:
            cleaned_data['last_commit_date'] = None  # Invalid date format

    return cleaned_data

def clean_commit_data(commit_data):
    """
    Clean fetched commit data before saving to the database.

    Parameters:
        commit_data (dict): Dictionary containing commit data fetched from GitHub.

    Returns:
        dict: Cleaned commit data.
    """
    cleaned_data = {
        'timestamp': commit_data.get('commit', {}).get('author', {}).get('date', None),
        'message': commit_data.get('commit', {}).get('message', ''),
    }
    return cleaned_data

def clean_issue_data(issue_data):
    """
    Clean fetched issue data before saving to the database.

    Parameters:
        issue_data (dict): Dictionary containing issue data fetched from GitHub.

    Returns:
        dict: Cleaned issue data.
    """
    cleaned_data = {
        'open_issues': issue_data.get('open_issues', 0),
        'closed_issues': issue_data.get('closed_issues', 0),
    }
    return cleaned_data

def clean_pull_request_data(pr_data):
    """
    Clean fetched pull request data before saving to the database.

    Parameters:
        pr_data (dict): Dictionary containing pull request data fetched from GitHub.

    Returns:
        dict: Cleaned pull request data.
    """
    cleaned_data = {
        'open_prs': pr_data.get('open_prs', 0),
        'merged_prs': pr_data.get('merged_prs', 0),
    }
    return cleaned_data

def clean_user_contribution_data(contribution_data):
    """
    Clean fetched user contribution data before saving to the database.

    Parameters:
        contribution_data (dict): Dictionary containing user contribution data fetched from GitHub.

    Returns:
        dict: Cleaned user contribution data.
    """
    cleaned_data = {
        'total_commits': contribution_data.get('total_commits', 0),
        'total_pr_opened': contribution_data.get('total_pr_opened', 0),
        'total_pr_merged': contribution_data.get('total_pr_merged', 0),
        'total_issues_opened': contribution_data.get('total_issues_opened', 0),
        'total_issues_closed': contribution_data.get('total_issues_closed', 0),
        'daily_date': contribution_data.get('daily_date', None),
        'daily_commits': contribution_data.get('daily_commits', 0),
        'daily_pr_opened': contribution_data.get('daily_pr_opened', 0),
        'daily_pr_merged': contribution_data.get('daily_pr_merged', 0),
        'daily_issues_opened': contribution_data.get('daily_issues_opened', 0),
        'daily_issues_closed': contribution_data.get('daily_issues_closed', 0),
    }
    return cleaned_data

@sync_to_async
def save_cleaned_user_data(cleaned_data):
    """
    Save cleaned GitHub user data into the database.

    Parameters:
        cleaned_data (dict): Cleaned user data.

    Returns:
        User: Saved User model instance.
    """
    user, created = User.objects.get_or_create(
        github_username=cleaned_data['github_username'],
        defaults={'full_name': cleaned_data['full_name'], 'email': cleaned_data['email'], 'location': cleaned_data['location']}
    )
    # Update user data if already exists
    if not created:
        user.full_name = cleaned_data['full_name']
        user.email = cleaned_data['email']
        user.location = cleaned_data['location']
        user.save()
    return user

@sync_to_async
def save_cleaned_repository_data(cleaned_data, user):
    """
    Save cleaned repository data into the database.

    Parameters:
        cleaned_data (dict): Cleaned repository data.
        user (User): User model instance to which the repository belongs.

    Returns:
        Repository: Saved Repository model instance.
    """
    repository, created = user.repository_set.get_or_create(
        name=cleaned_data['name'],
        defaults={'language': cleaned_data['language'], 'stars': cleaned_data['stars'], 'forks': cleaned_data['forks'], 'last_commit_date': cleaned_data['last_commit_date']}
    )
    # Update repository data if already exists
    if not created:
        repository.language = cleaned_data['language']
        repository.stars = cleaned_data['stars']
        repository.forks = cleaned_data['forks']
        repository.last_commit_date = cleaned_data['last_commit_date']
        repository.save()
    return repository

@sync_to_async
def save_cleaned_commit_data(cleaned_data, repository):
    """
    Save cleaned commit data into the database.

    Parameters:
        cleaned_data (dict): Cleaned commit data.
        repository (Repository): Repository model instance to which the commit belongs.

    Returns:
        Commit: Saved Commit model instance.
    """
    commit = repository.commit_set.create(timestamp=cleaned_data['timestamp'], message=cleaned_data['message'])
    return commit

@sync_to_async
def save_cleaned_issue_data(cleaned_data, repository):
    """
    Save cleaned issue data into the database.

    Parameters:
        cleaned_data (dict): Cleaned issue data.
        repository (Repository): Repository model instance to which the issue belongs.

    Returns:
        Issue: Saved Issue model instance.
    """
    issue = repository.issue_set.create(open_issues=cleaned_data['open_issues'], closed_issues=cleaned_data['closed_issues'])
    return issue

@sync_to_async
def save_cleaned_pull_request_data(cleaned_data, repository):
    """
    Save cleaned pull request data into the database.

    Parameters:
        cleaned_data (dict): Cleaned pull request data.
        repository (Repository): Repository model instance to which the pull request belongs.

    Returns:
        PullRequest: Saved PullRequest model instance.
    """
    pr = repository.pullrequest_set.create(open_prs=cleaned_data['open_prs'], merged_prs=cleaned_data['merged_prs'])
    return pr

@sync_to_async
def save_cleaned_user_contribution_data(cleaned_data, user):
    """
    Save cleaned user contribution data into the database.

    Parameters:
        cleaned_data (dict): Cleaned user contribution data.
        user (User): User model instance to which the contribution belongs.

    Returns:
        GitHubUserContribution: Saved GitHubUserContribution model instance.
    """
    contribution = user.githubusercontribution_set.create(**cleaned_data)
    return contribution

