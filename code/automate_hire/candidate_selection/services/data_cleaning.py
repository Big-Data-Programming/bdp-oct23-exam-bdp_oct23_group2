from datetime import datetime
import pytz
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
    print('clean data', user_data)
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
        'last_commit_date': repository_data.get('last_commit_date', None)  
    }

    if cleaned_data['last_commit_date'] is not None:
        try:
            cleaned_data['last_commit_date'] = datetime.strptime(cleaned_data['last_commit_date'], '%Y-%m-%d').date()
        except ValueError:
            cleaned_data['last_commit_date'] = None  

    return cleaned_data

def clean_commit_data(commit_data):
    """
    Clean fetched commit data before saving to the database.

    Parameters:
        commit_data (dict): Dictionary containing commit data fetched from GitHub.

    Returns:
        dict: Cleaned commit data.
    """
    timestamp_str = commit_data.get('timestamp')
    timestamp = None
    if timestamp_str:
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%SZ')
            timestamp = pytz.utc.localize(timestamp)
        except ValueError:
            pass
    cleaned_data = {
        'timestamp': timestamp,
        'message': commit_data.get('message', ''),
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
