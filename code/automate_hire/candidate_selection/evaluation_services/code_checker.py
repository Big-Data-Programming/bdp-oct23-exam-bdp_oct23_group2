import subprocess
import re
import textwrap


def pylint_score(b):
     #Storing code in variable
    a = textwrap.dedent(b)

    # Temporary file for storing code
    filename = "code.py"
    with open(filename, "w") as file:
        file.write(a)

    # Run pylint on the temporary file
    result = subprocess.run(['pylint', filename], capture_output=True, text=True)
    # print(result.stdout)

    # # Find the pylint score using a regular expression
    pattern_to_search = r"Your code has been rated at ([\d.]+)/10"
    matches = re.search(pattern_to_search, result.stdout)

    # storing pylint score in database
    if matches:
        score = matches.group(1)
        # convert score to float
        score = float(score)

        # print(f"pylint score: {score}/10")
        return score
    else:
        print("Score not found in pylint output")

bay="""
def smallest_num(a,b,c):
    num1=a
    num2=b
    num3=c
    smallest = 0
    if num1 <= num2 and num1 <= num3:
        smallest = num1
    if num2 <= num1 and num2 <= num3:
        smallest = num2
    if num3 <= num1 and num3 <= num2:
        smallest = num3
    print(f"{smallest} is the smallest of three numbers.")
    return smallest
"""

# read questions from db

# pylint_score(bay)