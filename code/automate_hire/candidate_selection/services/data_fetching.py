import asyncio
import aiohttp
import time
from github import Github
import agithub




async def fetch_github_users(access_token, since_user_id=None, max_users=None, batch_size=100):
    """
    Fetch GitHub users asynchronously using aiohttp.

    Parameters:
        access_token (str): GitHub API access token.
        since_user_id (int): Optional. The ID of the user to start fetching from.
        max_users (int): Optional. Maximum number of users to fetch.
        batch_size (int): Optional. Number of users to fetch in each API request.

    Returns:
        List of user objects fetched from GitHub.
    """
    async with aiohttp.ClientSession() as session:
        g = Github(access_token)
        users = []
        start_time = time.time()
        try:

            for user in g.get_users(since=since_user_id):
                users.append(user)
                if len(users) >= max_users:
                    break
                if len(users) % batch_size == 0:
                    time_elapsed = time.time() - start_time
                    if time_elapsed < 60:  # GitHub API rate limit: 60 requests per minute
                        await asyncio.sleep(60 - time_elapsed)
                        start_time = time.time()
        except Exception as e:
            print("An error occurred:", e)
    return users

async def fetch_repository_data(access_token, username):
    """
    Fetch repository data asynchronously from GitHub.

    Parameters:
        access_token (str): GitHub API access token.
        username (str): GitHub username for which repositories are to be fetched.

    Yields:
        dict: Dictionary containing repository data.
    """
    headers = {
        'Authorization': f'token {access_token}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.github.com/users/{username}/repos', headers=headers, ssl=False) as response:

            if response.status == 200:
                repositories = await response.json()
                for repo in repositories:

                    repository_info = {
                        'name': repo['name'],
                        'language': repo['language'],
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'last_commit_date': repo['updated_at'].split('T')[0]  # Extract date part only
                    }
                    yield repository_info
            else:
                print(f"Failed to fetch repositories for user {username}. Status code: {response.status}")


async def fetch_commit_data(access_token, username, repository_name):
    """
    Fetch commit data asynchronously from GitHub.

    Parameters:
        access_token (str): GitHub API access token.
        username (str): GitHub username for which commits are to be fetched.
        repository_name (str): Repository name for which commits are to be fetched.

    Returns:
        List of dictionaries containing commit data.
    """
    async with aiohttp.ClientSession() as session:
        g = Github(access_token)
        user = g.get_user(username)
        repository = user.get_repo(repository_name)
        commits = repository.get_commits()
        commit_data = []
        async for commit in commits:
            commit_info = {
                'timestamp': commit.commit.author.date,
                'message': commit.commit.message
            }
            commit_data.append(commit_info)
    return commit_data

async def fetch_issue_data(access_token, username, repository_name):
    """
    Fetch issue data asynchronously from GitHub.

    Parameters:
        access_token (str): GitHub API access token.
        username (str): GitHub username for which issues are to be fetched.
        repository_name (str): Repository name for which issues are to be fetched.

    Returns:
        Dictionary containing issue data.
    """
    async with aiohttp.ClientSession() as session:
        g = Github(access_token)
        user = g.get_user(username)
        repository = user.get_repo(repository_name)
        issues = repository.get_issues(state='all')
        issue_data = {
            'open_issues': 0,
            'closed_issues': 0
        }
        async for issue in issues:
            if issue.state == 'open':
                issue_data['open_issues'] += 1
            else:
                issue_data['closed_issues'] += 1
    return issue_data

async def fetch_pull_request_data(access_token, username, repository_name):
    """
    Fetch pull request data asynchronously from GitHub.

    Parameters:
        access_token (str): GitHub API access token.
        username (str): GitHub username for which pull requests are to be fetched.
        repository_name (str): Repository name for which pull requests are to be fetched.

    Returns:
        Dictionary containing pull request data.
    """
    async with aiohttp.ClientSession() as session:
        g = Github(access_token)
        user = g.get_user(username)
        repository = user.get_repo(repository_name)
        pull_requests = repository.get_pulls(state='all')
        pr_data = {
            'open_prs': 0,
            'merged_prs': 0
        }
        async for pr in pull_requests:
            if pr.state == 'open':
                pr_data['open_prs'] += 1
            if pr.merged:
                pr_data['merged_prs'] += 1
    return pr_data

async def fetch_user_contribution_data(access_token, username):
    """
    Fetch user contribution data asynchronously from GitHub.

    Parameters:
        access_token (str): GitHub API access token.
        username (str): GitHub username for which contribution data is to be fetched.

    Returns:
        Dictionary containing user contribution data.
    """
    async with aiohttp.ClientSession() as session:
        g = Github(access_token)
        user = g.get_user(username)
        contributions = user.get_contributions()
        contribution_data = {
            'total_commits': 0,
            'total_pr_opened': 0,
            'total_pr_merged': 0,
            'total_issues_opened': 0,
            'total_issues_closed': 0
        }
        async for contribution in contributions:
            if contribution.type == 'Commit':
                contribution_data['total_commits'] += 1
            if contribution.type == 'PullRequest':
                contribution_data['total_pr_opened'] += 1
                if contribution.payload.get('action') == 'closed' and contribution.payload.get('pull_request', {}).get('merged'):
                    contribution_data['total_pr_merged'] += 1
            if contribution.type == 'Issue':
                contribution_data['total_issues_opened'] += 1
                if contribution.payload.get('action') == 'closed':
                    contribution_data['total_issues_closed'] += 1
    return contribution_data

