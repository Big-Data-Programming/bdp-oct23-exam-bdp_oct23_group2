import asyncio
from .data_fetching import fetch_github_users, fetch_repository_data, fetch_user_contribution_data,fetch_issue_data, fetch_pull_request_data, fetch_commit_data, fetch_user_contribution_data

from .data_cleaning import clean_github_user_data, save_cleaned_user_data, save_cleaned_repository_data, save_cleaned_commit_data, save_cleaned_issue_data, save_cleaned_pull_request_data, save_cleaned_user_contribution_data, clean_repository_data, clean_commit_data, clean_issue_data, clean_pull_request_data, clean_user_contribution_data


# import tracemalloc

# tracemalloc.start()

import sys
sys.path.append('../')  

from config import GITHUB_ACCESS_TOKEN  

async def insert_data():
    """
    Insert data into the database.
    """
    users_data = await fetch_github_users(GITHUB_ACCESS_TOKEN, since_user_id=120, max_users=40)
 
    for user_data in users_data:
        cleaned_data = clean_github_user_data(user_data)
        if cleaned_data: 
            saved_user = await save_cleaned_user_data(cleaned_data)
            print("Saved user:", saved_user)
            repositories_data = []
            async for page in fetch_repository_data(GITHUB_ACCESS_TOKEN, user_data.login):
                print("Page:", page)
                repositories_data.append(page)
            
            
            print("Repositories data:", repositories_data)
            for repository_data in repositories_data:
                cleaned_data = clean_repository_data(repository_data)
                if cleaned_data:
                    saved_repository = await save_cleaned_repository_data(cleaned_data, saved_user)
                    print("Saved repository:", saved_repository)



                    
                    # commit_data = fetch_commit_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data.name)
            #         for commit in commit_data:
            #             cleaned_data = clean_commit_data(commit)
            #             if cleaned_data:
            #                 saved_commit = save_cleaned_commit_data(cleaned_data, saved_repository)
            #                 print("Saved commit:", saved_commit)
            #         issue_data = fetch_issue_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data.name)
            #         cleaned_data = clean_issue_data(issue_data)
            #         if cleaned_data:
            #             saved_issue = save_cleaned_issue_data(cleaned_data, saved_repository)
            #             print("Saved issue:", saved_issue)
            #         pull_request_data = fetch_pull_request_data(GITHUB_ACCESS_TOKEN, user_data.login, repository_data.name)
            #         cleaned_data = clean_pull_request_data(pull_request_data)
            #         if cleaned_data:
            #             saved_pull_request = save_cleaned_pull_request_data(cleaned_data, saved_repository)
            #             print("Saved pull request:", saved_pull_request)
            #         user_contribution_data = fetch_user_contribution_data(GITHUB_ACCESS_TOKEN, user_data.login)
            #         cleaned_data = clean_user_contribution_data(user_contribution_data)
            #         if cleaned_data:
            #             saved_user_contribution = save_cleaned_user_contribution_data(cleaned_data, saved_user)
            #             print("Saved user contribution:", saved_user_contribution)




