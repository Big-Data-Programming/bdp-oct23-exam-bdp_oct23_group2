import asyncio
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder

from .models import User, Repository, Commit, Issue, PullRequest, GitHubUserContribution, UserAnswers
from .data_processing import create_user_df, create_user_df_test, create_repository_df, create_commit_df, create_issue_df, create_pull_request_df, cluster_users, select_candidates

from .services.data_insertion import fetch_data_github, insert_stackoverflow_data
from .evaluation_services.code_checker import pylint_score
from .utils import clean_answers



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

def select_candidates_view(request):
    user_df_test = create_user_df_test()
    repository_df = create_repository_df()
    commit_df = create_commit_df()
    issue_df = create_issue_df()
    pull_request_df = create_pull_request_df()

    candidates = select_candidates(user_df_test, repository_df, commit_df, issue_df, pull_request_df)
    print("candidates", candidates)

    candidates_json = candidates.to_dict(orient='records')
    print(len(candidates_json))

    # Serialize the data and return as JSON response
    return JsonResponse({'candidates': candidates_json}, encoder=DjangoJSONEncoder)


def send_emails_to_candidates(request):
    candidate_emails = ['abdullahhanif821@gmail.com',]
    subject = 'Congratulations! You have been selected.'
    from_email = 'engabdullahhanif@gmail.com'  

    for candidate_email in candidate_emails:
        candidate_answers_url = request.build_absolute_uri(reverse('candidate-answers'))


        user_id = 12  # change this to the actual user id


        candidate_answers_url += f'?user_id={user_id}'
        message = f'Dear Candidate, \n\nCongratulations! You have been selected for a potential role at Doodle. Please visit the following link to complete the next steps:\n{candidate_answers_url}\n\nBest regards, \nDoodle Recruitment Team'
        send_mail(subject, message, from_email, [candidate_email])
    return JsonResponse({'message': 'Emails sent successfully'})

def candidate_answers_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        answer1 = request.POST.get('answer1', '')
        answer2 = request.POST.get('answer2', '')
        answer3 = request.POST.get('answer3', '')
        answers = [answer1, answer2, answer3]
        cleaned_answers = clean_answers(answers)
        user = User.objects.get(id=user_id)

        user_answers = UserAnswers(user=user, answer1=cleaned_answers[0], answer2=cleaned_answers[1], answer3=cleaned_answers[2])
        user_answers.save()

        
        return render(request, 'thank_you.html')
    else:
        question1 = "Write a Python function to reverse a string."
        question2 = "Write a Python function to check if a string is a palindrome."
        question3 = "Write a Python function to calculate the factorial of a number."
        user_id = request.GET.get('user_id')

        context = {
            'question1': question1,
            'question2': question2,
            'question3': question3, 
            'user_id': user_id
        }
        return render(request, 'candidate_answers.html', {'context': context})

def evaluate_answers(answers):
    accepted_users = []
    rejected_users = []
    answers = UserAnswers.objects.filter(status='pending')
    if not answers:
        return JsonResponse({'message': 'All answers have been evaluated!'})
    
    for answer in answers:
        print("answer", answer.answer1)
        answer1_score = pylint_score(answer.answer1)
        answer2_score = pylint_score(answer.answer2)
        answer3_score = pylint_score(answer.answer3)
        average_score = answer1_score + answer2_score + answer3_score/3
        if average_score >= 12:
            answer.status = 'accepted'
            accepted_users.append(answer.user)
        else:
            answer.status = 'rejected'
            rejected_users.append(answer.user)
        answer.save()
    users = accepted_users + rejected_users
    return JsonResponse({'message': 'Answers evaluated successfully!'})
    
def fetch_stackoverflow_data(request):
    
    insert_stackoverflow_data()
    
    return HttpResponse('Stackoverflow Data fetched successfully!')


    