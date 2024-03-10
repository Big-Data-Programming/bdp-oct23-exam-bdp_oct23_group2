import re
from .evaluation_services.code_checker import pylint_score


def reverse_string(s):
    return s[::-1]

def check_palindrome(s):
    s = s.replace(" ", "").lower()
    return s == s[::-1]

def calculate_factorial(n):
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n-1)

def evaluate_reverse_string(answer):
    try:
        # exec(answer)
        exec(answer, globals())

        reversed_string = reverse_string('hello')
        return [reversed_string == 'olleh', pylint_score(answer)]
    except Exception as e:
        print("error", e)
        return False


def evaluate_palindrome(answer):
    try:
        exec(answer)
        is_palindrome = check_palindrome('radar')
        return [is_palindrome, pylint_score(answer)]
    except Exception as e:
        return False

def evaluate_factorial(answer):
    try:
        exec(answer)
        factorial_result = calculate_factorial(5)
        return [factorial_result == 120, pylint_score(answer)]
    except Exception as e:
        return False

def evaluate_submission(submission):
    results = {}
    result_question1 = evaluate_reverse_string(submission.answer1)
    results['question1'] = result_question1[0]

    result_question2 = evaluate_palindrome(submission.answer2)
    results['question2'] = result_question2[0]

    result_question3 = evaluate_factorial(submission.answer3)
    results['question3'] = result_question3[0]
    print("results", results)
    print("result_question1", result_question1)
    print("result_question2", result_question2)
    print("result_question3", result_question3)   
    scores = [result_question1[1], result_question2[1], result_question3[1]]
    print("scores", scores)
    average_score = sum(scores) / len(scores)
    print("average_score", average_score)
    submission.average_score = average_score
    submission.save()


    if all(results.values()):
        submission.status = 'accepted'
    else:
        submission.status = 'rejected'

    submission.save()

    return all(results.values())


def clean_answers(answers):
    cleaned_answers = []
    pattern = re.compile(r'[;\'"]')
    for value in answers:
        cleaned_value = re.sub(pattern, '', value)
        cleaned_answers.append(cleaned_value)
    return cleaned_answers
    