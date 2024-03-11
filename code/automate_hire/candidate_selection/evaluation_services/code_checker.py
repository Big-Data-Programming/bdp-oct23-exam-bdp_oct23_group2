import subprocess
import re
import textwrap


def pylint_score(b):
    try:

        #Storing code in variable
        a = textwrap.dedent(b)

        # Temporary file for storing code
        filename = "code.py"
        with open(filename, "w") as file:
            file.write(a)

        # Run pylint on the temporary file
        try:

            result = subprocess.run(['pylint', filename], capture_output=True, text=True)
            # check if it is not returing not defined
            if result.stderr:
                print(result.stderr)
                return 0
        except Exception as e:
            print("Error in pylint_score: ", e)
            return 0
        # print(result.stdout)

        # # Find the pylint score using a regular expression
        try:
            pattern_to_search = r"Your code has been rated at ([\d.]+)/10"
            matches = re.search(pattern_to_search, result.stdout)
        except Exception as e:
            print("Error in pylint_score 2: ", e)
            return 0

        # storing pylint score in database
        if matches:
            score = matches.group(1)
            # convert score to float if not none, if none return 0
            if score:
                score = float(score)
            else:
                score = 0

            # print(f"pylint score: {score}/10")
            return score
        else:
            print("Score not found in pylint output")
    except Exception as e:
        print("Error in pylint_score 3: ", e)
        return 0

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