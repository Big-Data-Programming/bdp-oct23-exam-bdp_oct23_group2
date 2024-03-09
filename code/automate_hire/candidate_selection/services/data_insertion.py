import sys
import asyncio
from asgiref.sync import sync_to_async
import requests
import time
from config import GITHUB_ACCESS_TOKEN 

from candidate_selection.models import User

from .data_fetching import fetch_github_users, fetch_repository_data, fetch_user_contribution_data,fetch_issue_data, fetch_pull_request_data, fetch_commit_data, fetch_user_contribution_data

from .data_cleaning import clean_github_user_data, clean_repository_data, clean_commit_data, clean_issue_data, clean_pull_request_data, clean_user_contribution_data

sys.path.append('../')  


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
    print("cleaned_data inside the func", cleaned_data)
    contribution = user.githubusercontribution_set.create(**cleaned_data)
    return contribution


async def fetch_data_github():
    """
    Insert data into the database.
    """
    users_data = await fetch_github_users(GITHUB_ACCESS_TOKEN, since_user_id=1250, max_users=100)
 
    for user_data in users_data:
        cleaned_data = clean_github_user_data(user_data)
        if cleaned_data: 
            saved_user = await save_cleaned_user_data(cleaned_data)
            print("Saved user:", saved_user)

            repositories_data = []
            async for page in fetch_repository_data(GITHUB_ACCESS_TOKEN, user_data.login):
                repositories_data.append(page)
            for index, repository_data in enumerate(repositories_data):
                if index == 5:
                    print("Reached 1 repositories for user:", user_data.login)
                    break
                cleaned_data = clean_repository_data(repository_data)
                if cleaned_data:
                    saved_repository = await save_cleaned_repository_data(cleaned_data, saved_user)
                    print("Saved repository for user:", saved_repository, user_data.login)

                    commit_data = await fetch_commit_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data['name'])
                    for commit in commit_data:
                        cleaned_data = clean_commit_data(commit)
                        if cleaned_data:
                            saved_commit = await save_cleaned_commit_data(cleaned_data, saved_repository)
                            print("Saved commit:", saved_commit)

                    issue_data = await fetch_issue_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data['name'])
                    cleaned_data = clean_issue_data(issue_data)
                    if cleaned_data:
                        saved_issue = await asyncio.gather(save_cleaned_issue_data(cleaned_data, saved_repository))
                        print("Saved issue:", saved_issue)

                    pull_request_data = await fetch_pull_request_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data['name'])
                    cleaned_data = clean_pull_request_data(pull_request_data)
                    if cleaned_data:
                        saved_pull_request = await asyncio.gather(save_cleaned_pull_request_data(cleaned_data, saved_repository))
                        print("Saved pull request:", saved_pull_request)

            user_contribution_data = await fetch_user_contribution_data(GITHUB_ACCESS_TOKEN, user_data.login)
            cleaned_data = clean_user_contribution_data(user_contribution_data)
            if cleaned_data:
                saved_user_contribution = await asyncio.gather(save_cleaned_user_contribution_data(cleaned_data, saved_user))
                print("Saved user contribution:", saved_user_contribution)




def fetch_stackoverflow_users(site='stackoverflow', page=1, pagesize=100):
    url = f"https://api.stackexchange.com/2.3/users?site={site}&page={page}&pagesize={pagesize}"
    print("Request URL:", url)  # Debugging statement
    response = requests.get(url)
    print("Response Status Code:", response.status_code)  # Debugging statement
    print("Response Content:", response.content)  # Debugging statement
    if response.status_code == 200:
        data = response.json()
        users = data.get('items', [])
        return users
    elif response.status_code == 429:  # Rate limit exceeded
        retry_after = int(response.headers.get('retry-after', 30))
        print(f"Rate limit exceeded. Waiting for {retry_after} seconds before retrying.")
        time.sleep(retry_after)
        return fetch_stackoverflow_users(site, page, pagesize)
    else:
        print(f"Failed to fetch users. Status code: {response.status_code}")
        return []

def fetch_user_answers(users, site='stackoverflow'):
    answers_dict = {}

    for user in users:
        user_id = user['user_id']
        reputation = user.get('reputation', 'N/A')
        accept_rate = user.get('accept_rate', 'N/A')
        url = f"https://api.stackexchange.com/2.3/users/{user_id}/answers?order=asc&sort=votes&site={site}"
        response = requests.get(url)
        time.sleep(1)
        if response.status_code == 200:
            data = response.json()
            answers = data.get('items', [])
            answers_dict[user_id] = {'reputation': reputation, 'accept_rate': accept_rate, 'answers': answers}
        elif response.status_code == 429:  # Rate limit exceeded
            print("Rate limit exceeded. Please wait before retrying.")
        else:
            print(f"Failed to fetch answers for user ID {user_id}. Status code: {response.status_code}")

    return answers_dict

def fetech_stackoverflow_users():
    users = fetch_stackoverflow_users()
    print(f"Fetched {len(users)} users.")
    # answers_dict = fetch_user_answers(users)
    # time.sleep(2)
    # for user_id, user_data in answers_dict.items():
    #     print(f"User ID: {user_id}")
    #     print(f"Reputation: {user_data['reputation']}")
    #     print(f"Accept Rate: {user_data['accept_rate']}")
    #     print("Answers:")
    #     for answer in user_data['answers']:
    #         print("Answer ID:", answer['answer_id'])
    #         print("Question ID:", answer['question_id'])
    #         print("Answer Body:", answer['body'])
    #         print("-----------------------------")
