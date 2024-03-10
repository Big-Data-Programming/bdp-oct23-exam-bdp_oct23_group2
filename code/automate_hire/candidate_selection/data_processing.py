import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.metrics import silhouette_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
import numpy as np

from .models import User, Repository, Commit, Issue, PullRequest

# create a function to return a dataframe for testing starting after user_id 100
def create_user_df_test():
    """
    Create a DataFrame containing user data.

    Returns:
        pd.DataFrame: DataFrame containing user data.

    """
    # limit the number of users to 80
    users = User.objects.all()[:100]
    # users = User.objects.all()
    user_data = {'id': [], 'github_username': [], 'full_name': [], 'email': [], 'location': []}
    for user in users:
        user_data['id'].append(user.id)
        user_data['github_username'].append(user.github_username)
        user_data['full_name'].append(user.full_name)
        user_data['email'].append(user.email)
        user_data['location'].append(user.location)
    return pd.DataFrame(user_data)

def create_user_df():
    """
    Create a DataFrame containing user data.

    Returns:
        pd.DataFrame: DataFrame containing user data.

    """
    # limit the number of users to 80
    users = User.objects.all()[101:]
    # users = User.objects.all()
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

def prepare_new_candidates_df(user_df_test, repository_df, commit_df, issue_df, pull_request_df, languages):
    """
    Prepare a DataFrame containing data of new candidates.

    Args:
        user_df_test (pd.DataFrame): DataFrame containing test user data.
        repository_df_filtered (pd.DataFrame): DataFrame containing filtered repository data.
        commit_df (pd.DataFrame): DataFrame containing commit data.
        issue_df (pd.DataFrame): DataFrame containing issue data.
        pull_request_df (pd.DataFrame): DataFrame containing pull request data.

    Returns:
        pd.DataFrame: DataFrame containing data of new candidates.
    """

    # selected_languages = ['Python', 'Ruby']
    
    repository_df_filtered = repository_df[repository_df['language'].isin(languages)]
    # repository_df_filtered = repository_df[repository_df['language'].isin(selected_languages)]


    merged_df = pd.merge(user_df_test, repository_df_filtered, left_on='id', right_on='user_id')
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

    new_candidates_df = merged_df.groupby('user_id').agg({
        'total_commits': 'sum',
        'total_pr_opened': 'sum',
        'total_pr_merged': 'sum',
        'total_issues_opened': 'sum',
        'total_issues_closed': 'sum'
    }).reset_index()
    return new_candidates_df

def cluster_users(user_df_train, repository_df, commit_df, issue_df, pull_request_df):
    selected_languages = ['Python', 'JavaScript', 'Ruby',]
    repository_df_filtered = repository_df[repository_df['language'].isin(selected_languages)]


    
    merged_df = pd.merge(user_df_train, repository_df, left_on='id', right_on='user_id')
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
  

    #feature sccaling
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(user_features.drop('user_id', axis=1))

     #k means and elbow method to find optimum clusters 
    # inertia = []
    # for n_clusters in range(1, 11):       #range of no. of clusters (1,11) so that it has a suficient range to compare
    #     kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init='auto')
    #     print(kmeans)
    #     kmeans.fit(scaled_features)
    #     inertia.append(kmeans.inertia_)

    # Visualize inertia values
    # plt.plot(range(1, 11), inertia, marker='o')   #commented out the plot 
    # plt.title('Elbow Method')
    # plt.xlabel('Number of Clusters')
    # plt.ylabel('Inertia')
    # plt.show()                 

    #optimal number of clusters is 4 but i forced it to use 2 
    kmeans = KMeans(n_clusters=2, random_state=42, n_init='auto')
    #print(scaled_features)
    kmeans.fit(scaled_features)
    #assign cluster label
    user_features['cluster_label'] = kmeans.labels_


    # print clusters centers
    print("Cluster Centers:")
    print(kmeans.cluster_centers_)

    # Print number of users in each cluster
    print("Number of users in each cluster:")
    print(user_features['cluster_label'].value_counts())

    # Print user features along with cluster labels
    print("User features with cluster labels:")
    print(user_features)

    # pickle the k means
    with open('kmeans_model.pkl', 'wb') as f:
        pickle.dump(kmeans, f)


    #logistic regression.

    X = user_features.drop(columns=['cluster_label'])  # Features excluding the cluster label
    y = user_features['cluster_label'] 
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # print("Shapes of X_train, X_test, y_train, y_test:")
    # print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
    print("NaN values in X_train:", np.isnan(X_train).any())
    print("NaN values in X_test:", np.isnan(X_test).any())
    print("Zero-variance features in X_train:", np.var(X_train, axis=0) == 0)

    # ADDED
    non_zero_variance_features = X_train.columns[X_train.var() != 0]
    X_train = X_train[non_zero_variance_features]
    X_test = X_test[non_zero_variance_features]


    logreg_model = LogisticRegression()
    logreg_model.fit(X_train, y_train)

    accuracy = logreg_model.score(X_test, y_test) 
    print("Accuracy:", accuracy)

    predicted = logreg_model.predict(X_test)
    confusion_matrix = metrics.confusion_matrix(y_test, predicted)
    print(confusion_matrix)

    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    # pickle the logistic regression
    with open('logreg_model.pkl', 'wb') as f:
        pickle.dump(logreg_model, f)

    return user_features

def select_candidates(user_df_test, repository_df, commit_df, issue_df, pull_request_df, languages):
    # load pickled loogistic regression
    with open('logreg_model.pkl', 'rb') as f:
        loaded_logreg  = pickle.load(f)
        
    # load the pickled k means
    with open('kmeans_model.pkl', 'rb') as f:
        loaded_kmeans = pickle.load(f)

    with open('scaler.pkl', 'rb') as f:
        loaded_scaler = pickle.load(f)


    # Assuming you have a DataFrame containing new candidate data called 'new_candidates'
    # new_candidates = []
    new_candidates = prepare_new_candidates_df(user_df_test, repository_df, commit_df, issue_df, pull_request_df, languages)

    # Preprocess new candidate data (scaling, encoding, etc.)
    scaled_new_candidates = loaded_scaler.transform(new_candidates.drop('user_id', axis=1))


    # Predict clusters using K-means
    new_cluster_labels = loaded_kmeans.predict(scaled_new_candidates)

    # Assign cluster labels to new candidate data
    new_candidates['cluster_label'] = new_cluster_labels

    # Filter candidates belonging to the "good" cluster (assuming cluster_label 1 represents "good" candidates)
    good_candidates = new_candidates[new_candidates['cluster_label'] == 1]

    if not good_candidates.empty:
        # Remove 'total_issues_closed' feature before prediction
        good_candidates = good_candidates.drop(columns=['total_issues_closed'])

        # Use logistic regression to validate the "good" candidates and filter out the ones predicted as "bad"
        predicted_labels = loaded_logreg.predict(good_candidates.drop(columns=['cluster_label']))

        # Filter out candidates predicted as "bad"
        final_good_candidates = good_candidates[predicted_labels == 1]  # Assuming 1 represents "good" predictions
        print("final_good_candidates", final_good_candidates.to_dict(orient='records'))
        # print("len(final_good_candidates)", len(final_good_candidates))

        # fetch final_users from the database
        final_users = User.objects.filter(id__in=final_good_candidates['user_id'].values)
        print("final_users", final_users.values())

        return final_users
    else:
        # If there are no good candidates, return an empty DataFrame
        return pd.DataFrame()

    # # !ADDED
    # good_candidates = good_candidates.drop(columns=['total_issues_closed'])


    # # Use logistic regression to validate the "good" candidates and filter out the ones predicted as "bad"
    # X_good_candidates = good_candidates.drop(columns=['cluster_label'])  # Features excluding the cluster label
    # predicted_labels = loaded_logreg.predict(X_good_candidates)

    # # Filter out candidates predicted as "bad"
    # final_good_candidates = good_candidates[predicted_labels == 1]  # Assuming 0 represents "good" predictions

    # # Now final_good_candidates contains the list of good candidates

    # return final_good_candidates


