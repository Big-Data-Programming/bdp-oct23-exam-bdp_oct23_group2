import re
from .evaluation_services.code_checker import pylint_score

# import unittest
# from django.test import TestCase
# from django.test.runner import DiscoverRunner
# from .test_factorial import TestFactorialFunction
# from .test_smallest_num import TestSmallestNum


# def run_tests():
#     """
#     Run the test suite and return True if all tests pass, False otherwise.
#     """
#     test_runner = DiscoverRunner()
#     result = test_runner.run_tests(['tests.test_factorial', 'tests.test_smallest_num'])
#     return result.wasSuccessful()

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
        exec(answer)
        reversed_string = reverse_string('hello')
        # return [reversed_string == 'olleh', pylint_score(answer)]
        # return [reversed_string == 'olleh',]
        return reversed_string == 'olleh'
    except Exception as e:
        print("error", e)
        return False

def evaluate_palindrome(answer):
    try:
        exec(answer)
        is_palindrome = check_palindrome('radar')
        # return [is_palindrome, pylint_score(answer)]
        # return [is_palindrome,]
        return is_palindrome
    except Exception as e:
        return False

def evaluate_factorial(answer):
    try:
        exec(answer)
        factorial_result = calculate_factorial(5)
        # return [factorial_result == 120, pylint_score(answer)]
        # return [factorial_result == 120,]
        return factorial_result == 120
    except Exception as e:
        return False

def evaluate_submission(submission):
    results = {}
    result_question1 = evaluate_reverse_string(submission.answer1)
    # print("result_question1", result_question1)
    # print("result_question1[0]", result_question1[0])
    # results['question1'] = result_question1[0]
    results['question1'] = result_question1
    # print("result_question1", result_question1)
    result_question2 = evaluate_palindrome(submission.answer2)
    # results['question2'] = result_question2[0]
    results['question2'] = result_question2

    result_question3 = evaluate_factorial(submission.answer3)
    # results['question3'] = result_question3[0]
    results['question3'] = result_question3
    # print("result_question3", result_question3)
    # print("results", results)
    # print("result_question1", result_question1)
    # print("result_question2", result_question2)
    # print("result_question3", result_question3)   
    # scores = [result_question1[1], result_question2[1], result_question3[1]]
    print("results", results)


    # average_score = sum(scores) / len(scores)
    average_score = 12
    # print("average_score", average_score)
    submission.average_score = average_score

    # tests_passed = run_tests()
    # print("tests_passed", tests_passed)

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
    