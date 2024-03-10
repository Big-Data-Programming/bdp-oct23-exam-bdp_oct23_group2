from candidate_selection.models import User
from datetime import datetime
import pytz
from asgiref.sync import sync_to_async
import re



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
    print("cleaned_data inside the func", cleaned_data)
    contribution = user.githubusercontribution_set.create(**cleaned_data)
    return contribution


# Stackoverflow data cleaning
def clean_answers_data(answers_dict):
    cleaned_answers_dict = {}
    for user_id, user_data in answers_dict.items():
        cleaned_answers = []
        for answer in user_data['answers']:
            clean_answer_body = re.sub('<[^<]+?>', '', answer['body'])
            clean_answer_body = clean_answer_body.strip()
            cleaned_answers.append({
                'answer_id': answer['answer_id'],
                'question_id': answer['question_id'],
                'body': clean_answer_body
            })
        cleaned_user_data = {
            'reputation': user_data['reputation'],
            'accept_rate': user_data['accept_rate'],
            'answers': cleaned_answers
        }
        cleaned_answers_dict[user_id] = cleaned_user_data
    return cleaned_answers_dict



def clean_user_data(user):
    badges_dict = user.get('badge_counts', 0)
    badges = badges_dict['bronze'] + badges_dict['silver'] + badges_dict['gold']

    cleaned_user = {
        'user_id': user['user_id'],
        'reputation': user.get('reputation', 0),
        'badges': badges
        # Add more fields to clean as needed
    }
    return cleaned_user
def clean_answers_data(answers_dict):
    cleaned_answers_dict = {}
    for user_id, user_data in answers_dict.items():
        cleaned_answers = []
        for answer in user_data['answers']:
            cleaned_answer_body = answer['body'].strip()  # Remove leading/trailing whitespace
            cleaned_answers.append({
                'answer_id': answer['answer_id'],
                'question_id': answer['question_id'],
                'body': cleaned_answer_body
            })
        cleaned_answers_dict[user_id] = {
            'reputation': user_data['reputation'],
            'accept_rate': user_data['accept_rate'],
            'answers': cleaned_answers
        }
    return cleaned_answers_dict

def clean_questions_and_answers_data(user_data):
    cleaned_data = {
        'total_questions': user_data.get('total_questions', 0),
        'total_answers': user_data.get('total_answers', 0),
        'question_upvotes': user_data.get('question_upvotes', 0),
        'question_downvotes': user_data.get('question_downvotes', 0),
        'answer_upvotes': user_data.get('answer_upvotes', 0),
        'answer_downvotes': user_data.get('answer_downvotes', 0)
    }
    return cleaned_data