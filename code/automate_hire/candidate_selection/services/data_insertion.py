import sys
import asyncio
from asgiref.sync import sync_to_async
import requests
import time
from config import GITHUB_ACCESS_TOKEN 

from candidate_selection.models import User, StackOverflowUser, QuestionAnswer

from .data_fetching import fetch_github_users, fetch_repository_data, fetch_user_contribution_data,fetch_issue_data, fetch_pull_request_data, fetch_commit_data, fetch_user_contribution_data, fetch_stackoverflow_users, fetch_user_answers, fetch_user_questions

from .data_cleaning import clean_github_user_data, clean_repository_data, clean_commit_data, clean_issue_data, clean_pull_request_data, clean_user_contribution_data 
# clean_user_data, clean_questions_and_answers_data


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
    users_data = await fetch_github_users(GITHUB_ACCESS_TOKEN, since_user_id=2200, max_users=100)
 
    for user_data in users_data:
        cleaned_data = clean_github_user_data(user_data)
        if cleaned_data: 
            saved_user = await save_cleaned_user_data(cleaned_data)
            print("Saved user:", saved_user)

            repositories_data = []
            async for page in fetch_repository_data(GITHUB_ACCESS_TOKEN, user_data.login):
                repositories_data.append(page)
            for index, repository_data in enumerate(repositories_data):
                if index == 10:
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

# write save into db functions here 
def save_cleaned_user_data_sof():
    pass


# def insert_stackoverflow_data():
#     # 1 - fetch users 
#     # 2 - clean fetched user
#     # 3 - save user into the db
#     # 4 - fetch user quesiions
#     # 5 - clean questions
#     # 6 - save questions into db
#     # 7 - fetch user answers
#     # 8 - clean user answers
#     # 9 - save user answers into db

    pass

def insert_user_into_database(cleaned_user_data):
    # Create a new StackOverflowUser object with the cleaned data and save it to the database
    try:
        user, created = StackOverflowUser.objects.get_or_create(
            stackoverflow_username=cleaned_user_data['user_id'],
            reputation=cleaned_user_data['reputation'],
            badges=cleaned_user_data['badges']
        )
        print(f"User '{user.stackoverflow_username}' inserted into the database.")
    except Exception as e:
        print(f"Failed to insert user into the database: {e}")

def insert_answers_into_database(user_id, user_data):
    try:
        # Create a new QuestionAnswer object
        question_answer = QuestionAnswer.objects.create(
            user=StackOverflowUser.objects.get(pk=user_id),  # Get the user object using the user_id
            total_questions=user_data.get('total_questions', 0),  # Assuming total_questions is part of user_data
            total_answers=user_data.get('total_answers', 0),  # Assuming total_answers is part of user_data
            question_upvotes=user_data.get('question_upvotes', 0),  # Assuming question_upvotes is part of user_data
            question_downvotes=user_data.get('question_downvotes', 0),  # Assuming question_downvotes is part of user_data
            answer_upvotes=user_data.get('answer_upvotes', 0),  # Assuming answer_upvotes is part of user_data
            answer_downvotes=user_data.get('answer_downvotes', 0)  # Assuming answer_downvotes is part of user_data
        )
        print(f"QuestionAnswer for user ID {user_id} inserted into the database.")
    except Exception as e:
        print(f"Failed to insert QuestionAnswer for user ID {user_id}: {e}")

def combine_answers_and_questions(user_answers, user_questions):

    #  work on it later
    # question_upvotes = sum(question.get('upvotes', 0) for question in user_questions)
    # question_downvotes = sum(question.get('downvotes', 0) for question in user_questions)
    # answer_upvotes = sum(answer.get('upvotes', 0) for answer in user_answers)
    # answer_downvotes = sum(answer.get('downvotes', 0) for answer in user_answers)

    # combined_data = {
    #     'total_questions': len(user_questions),  # Get the total number of questions
    #     'total_answers': len(user_answers),  # Get the total number of answers
    #     'question_upvotes': question_upvotes,
    #     'question_downvotes': question_downvotes,
    #     'answer_upvotes': answer_upvotes,
    #     'answer_downvotes': answer_downvotes
    # }

    combined_data = {
        'total_questions': user_questions,  # Get the total number of questions
        'total_answers': user_answers,  # Get the total number of answers
        'question_upvotes': 5,
        'question_downvotes': 5,
        'answer_upvotes': 5,
        'answer_downvotes': 5
    }
    return combined_data

def insert_questions_into_database(user_id, cleaned_questions):
    try:
        print("cleaned_questions", cleaned_questions)
        question_answer = QuestionAnswer.objects.create(
            user=StackOverflowUser.objects.get(stackoverflow_username=user_id), 
            total_questions=cleaned_questions['total_questions'],
            total_answers=cleaned_questions['total_answers'],
            question_upvotes=cleaned_questions['question_upvotes'],
            question_downvotes=cleaned_questions['question_downvotes'],
            answer_upvotes=cleaned_questions['answer_upvotes'],
            answer_downvotes=cleaned_questions['answer_downvotes']
        )
        print(f"QuestionAnswer for user ID {user_id} inserted into the database.")
    except Exception as e:
        print(f"Failed to insert QuestionAnswer for user ID {user_id}: {e}")


def insert_stackoverflow_data():
    # users = fetch_stackoverflow_users()
    # print('users', len(users))

    # for user in users:
    #     cleaned_user = clean_user_data(user) 

    #     insert_user_into_database(cleaned_user)
    
    #     user_answers = fetch_user_answers(user)

    #     user_questions = fetch_user_questions(user['user_id'])
    #     questions_and_answers = combine_answers_and_questions(user_answers, user_questions)
    #     cleaned_questions_answers_data = clean_questions_and_answers_data(questions_and_answers)
    #     insert_questions_into_database(user['user_id'], cleaned_questions_answers_data)

    pass

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
