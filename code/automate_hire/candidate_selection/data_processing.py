import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


from .models import User, Repository, Commit, Issue, PullRequest


def create_user_df():
    """
    Create a DataFrame containing user data.

    Returns:
        pd.DataFrame: DataFrame containing user data.

    """
    users = User.objects.all()
    user_data = {'id': [], 'github_username': [], 'full_name': [], 'email': [], 'location': []}
    for user in users:
        user_data['id'].append(user.id)
        user_data['github_username'].append(user.github_username)
        user_data['full_name'].append(user.full_name)
        user_data['email'].append(user.email)
        user_data['location'].append(user.location)
    return pd.DataFrame(user_data)

def create_repository_df():
    """
    Create a DataFrame containing repository data.

    Returns:
        pd.DataFrame: DataFrame containing repository data.

    """
    repositories = Repository.objects.all()
    repository_data = {'id': [], 'user_id': [], 'name': [], 'language': [], 'stars': [], 'forks': [], 'last_commit_date': []}
    for repository in repositories:
        repository_data['id'].append(repository.id)
        repository_data['user_id'].append(repository.user_id)
        repository_data['name'].append(repository.name)
        repository_data['language'].append(repository.language)
        repository_data['stars'].append(repository.stars)
        repository_data['forks'].append(repository.forks)
        repository_data['last_commit_date'].append(repository.last_commit_date)
    return pd.DataFrame(repository_data)

def create_commit_df():
    """
    Create a DataFrame containing commit data.

    Returns:
        pd.DataFrame: DataFrame containing commit data.

    """
    commits = Commit.objects.all()
    commit_data = {'id': [], 'repository_id': [], 'timestamp': [], 'message': []}
    for commit in commits:
        commit_data['id'].append(commit.id)
        commit_data['repository_id'].append(commit.repository_id)
        commit_data['timestamp'].append(commit.timestamp)
        commit_data['message'].append(commit.message)
    return pd.DataFrame(commit_data)

def create_issue_df():
    """
    Create a DataFrame containing issue data.

    Returns:
        pd.DataFrame: DataFrame containing issue data.

    """
    issues = Issue.objects.all()
    issue_data = {'id': [], 'repository_id': [], 'open_issues': [], 'closed_issues': []}
    for issue in issues:
        issue_data['id'].append(issue.id)
        issue_data['repository_id'].append(issue.repository_id)
        issue_data['open_issues'].append(issue.open_issues)
        issue_data['closed_issues'].append(issue.closed_issues)
    return pd.DataFrame(issue_data)

def create_pull_request_df():
    """
    Create a DataFrame containing pull request data.

    Returns:
        pd.DataFrame: DataFrame containing pull request data.

    """
    pull_requests = PullRequest.objects.all()
    pr_data = {'id': [], 'repository_id': [], 'open_prs': [], 'merged_prs': []}
    for pr in pull_requests:
        pr_data['id'].append(pr.id)
        pr_data['repository_id'].append(pr.repository_id)
        pr_data['open_prs'].append(pr.open_prs)
        pr_data['merged_prs'].append(pr.merged_prs)
    return pd.DataFrame(pr_data)

def cluster_users(user_df, repository_df, commit_df, issue_df, pull_request_df, n_clusters=3):
    """
    Cluster users based on their GitHub contributions.

    Parameters:
        user_df (pd.DataFrame): DataFrame containing user data.
        repository_df (pd.DataFrame): DataFrame containing repository data.
        commit_df (pd.DataFrame): DataFrame containing commit data.
        issue_df (pd.DataFrame): DataFrame containing issue data.
        pull_request_df (pd.DataFrame): DataFrame containing pull request data.
        n_clusters (int): Number of clusters to create.

    Returns:
        pd.DataFrame: DataFrame containing user data with cluster labels.

    """
    merged_df = pd.merge(user_df, repository_df, left_on='id', right_on='user_id')
    merged_df = merged_df.rename(columns={'id_y': 'repository_id'})
    merged_df = merged_df.drop('id_x', axis=1)

    commit_metrics = commit_df.groupby('repository_id').size().reset_index(name='total_commits')
    issue_metrics = issue_df.groupby('repository_id').agg({'closed_issues': 'sum', 'open_issues': 'sum'}).reset_index()
    issue_metrics.rename(columns={'open_issues': 'total_issues_opened'}, inplace=True)
    issue_metrics.rename(columns={'closed_issues': 'total_issues_closed'}, inplace=True)

    pr_metrics = pull_request_df.groupby('repository_id').agg({'merged_prs': 'sum', 'open_prs': 'sum'}).reset_index()
    pr_metrics.rename(columns={'open_prs': 'total_pr_opened'}, inplace=True)
    pr_metrics.rename(columns={'merged_prs': 'total_pr_merged'}, inplace=True)

    merged_df = pd.merge(merged_df, commit_metrics, on='repository_id', how='left')
    merged_df = pd.merge(merged_df, issue_metrics, on='repository_id', how='left')
    merged_df = pd.merge(merged_df, pr_metrics, on='repository_id', how='left')

    user_features = merged_df.groupby('user_id').agg({
        'total_commits': 'sum',
        'total_pr_opened': 'sum',
        'total_pr_merged': 'sum',
        'total_issues_opened': 'sum',
        'total_issues_closed': 'sum'
    }).reset_index()
    print("user_features", user_features.head())
    print("user_features", user_features.columns)

    # Scale the features and fit KMeans clustering model

    # scaler = StandardScaler()
    # scaled_features = scaler.fit_transform(user_features.drop('user_id', axis=1))


    # kmeans = KMeans(n_clusters=n_clusters)
    # kmeans.fit(scaled_features)


    # user_features['cluster'] = kmeans.labels_
    # # print("user_features", user_features.head())

    # return user_features



