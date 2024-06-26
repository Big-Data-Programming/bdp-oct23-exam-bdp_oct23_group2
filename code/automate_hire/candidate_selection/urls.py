
from django.urls import path
from .views import select_features_view, fetch_from_github_view, cluster_users_view, send_emails_to_candidates, candidate_answers_view, fetch_stackoverflow_data, evaluate_answers, select_candidates_view, send_emails_to_final_candidates, final_candidates_view

urlpatterns = [
    path('', select_features_view, name='select-features'),
    path('fetch-from-github', fetch_from_github_view, name='fetch-from-github'),
    path('cluster-users', cluster_users_view, name='cluster-users'),
    path('send-emails', send_emails_to_candidates, name='send-emails'),
    path('candidate-answers', candidate_answers_view, name='candidate-answers'),
    path('stackoverflow', fetch_stackoverflow_data, name='stackoverflow'),
    path('evaluate-answers', evaluate_answers, name='evaluate-answers'),
    path('select-candidates', select_candidates_view, name='select-candidates'),
    path('send-emails-final', send_emails_to_final_candidates, name='send-emails-final'),
    path('final-candidates', final_candidates_view, name='final-candidates'),

]